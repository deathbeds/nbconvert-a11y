"""fine-grained axe accessibility testing.

this module contains tooling to run headless browsers that assess the accessibility of web pages. 
the tooling can be used interactively in notebooks or as pytest fixtures

* an axe fixture to use in pytest
* a command line application for auditing files.

"""

# requires node and axe
# requires playwright
import dataclasses
from json import dumps
from exceptiongroup import ExceptionGroup

# selectors for regions of the notebook
class SELECTORS:
    """ "selectors for notebook and third party components in notebooks."""

    # these should be moved to a config test.
    MATHJAX = "[id^=MathJax]"
    JUPYTER_WIDGETS = ".jupyter-widgets"
    OUTPUTS = ".jp-OutputArea-output"
    NO_ALT = "img:not([alt])"
    PYGMENTS = ".highlight"
    SA11Y = "sa11y-control-panel"


# the default test tags start with the most strict conditions.
# end-users can refine the TEST_TAGS they choose in their axe configuration.
# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#axe-core-tags
TEST_TAGS = [
    "ACT",
    "best-practice",
    "experimental",
    "wcag2a",
    "wcag2aa",
    "wcag2aaa",
    "wcag21a",
    "wcag21aa",
    "wcag22aa",
    "TTv5",
]


class Base:
    """base class for exceptions and models"""

    def __init_subclass__(cls) -> None:
        dataclasses.dataclass(cls)

    def dict(self):
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}

    def dump(self):
        return dumps(self.dict())


class Violation(Exception, Base):
    """an exception class that generates exceptions based on data payloads."""

    map = {}

    @classmethod
    def new_type(cls, id):
        bases = (cls,)
        if isinstance(id, tuple):
            id, bases = id
        if id in cls.map:
            return cls.map[id]
        return cls.map.setdefault(id, type(id, bases, {}))

    def __class_getitem__(cls, id):
        return cls.new_type(id)

    @classmethod
    def cast(cls, data):
        return cls

    def __new__(cls, **kwargs):
        target = cls.cast(kwargs)
        if cls is not target:
            return target(**kwargs)
        self = super().__new__(cls, **kwargs)
        self.__init__(**kwargs)
        return self


# we make extra refinements to way that we right tests.
# using expected/unexpected passes/failures allows us to map
# out what we do and do not know about complex systems.
# we can use expected failures to isolate known inaccessibilities.
# capturing these known conditions makes it possible to creates issues
# and solutions to these violations.
# sometimes, combinations of failure conditions might indicate http failures
# and an inability to assess content.
# unexpacted passes are situations where an upstream might have been fixed
# and work is required on the test harness to remove a once identified inaccessibility.
# these combinations of tests scenarios can be useful retrofitting inaccessible systems.
class ExpectedFail(ExceptionGroup):
    """raised when a collection of expected failures are matched"""


# expected to fail, but not raised
class UnexpectedPass(Exception):
    """raised when expected failure is NOT matched"""


# raised, but not known to raise
class UnexpectedFail(ExceptionGroup):
    """raised when an unmatched failure is encountered"""


class Violations(ExceptionGroup):
    exception = Violation

    def xfail(self, *matches):
        exceptions = []
        expected_fail, unexpected_fail = self.split(matches or tuple())
        unexpected_pass = set()
        if expected_fail:
            unexpected_pass.update(map(type, expected_fail.exceptions))
            unexpected_pass = set(matches) - unexpected_pass
            if unexpected_pass:
                exceptions.append(UnexpectedPass(tuple(unexpected_pass)))
        if unexpected_fail:
            exceptions.append(UnexpectedFail(unexpected_fail.message, unexpected_fail.exceptions))
        if (unexpected_fail or unexpected_pass) and expected_fail:
            exceptions.append(expected_fail)
        if not exceptions:
            if expected_fail:
                return ExpectedFail("all expected failures found", expected_fail.exceptions)
            return
        if len(exceptions) == 1:
            return exceptions[0]
        return Violations("unexpected passes and failures", tuple(exceptions))

    @classmethod
    def from_violations(cls, data):
        return NotImplementedError()

    # __repr__ = __str__ = ExceptionGroup.__str__
