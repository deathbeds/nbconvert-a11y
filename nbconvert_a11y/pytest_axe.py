"""report axe violations in html content

* an axe fixture to use in pytest
* a command line application for auditing files.

"""

# requires node and axe
# requires playwright
import dataclasses
from collections import defaultdict
from functools import lru_cache, partial
from json import dumps, loads
from pathlib import Path
from shlex import quote, split
from subprocess import CalledProcessError, check_output
from typing import Any

import exceptiongroup
from pytest import fixture

# selectors for regions of the notebook
MATHJAX = "[id^=MathJax]"
JUPYTER_WIDGETS = ".jupyter-widgets"
OUTPUTS = ".jp-OutputArea-output"
NO_ALT = "img:not([alt])"
PYGMENTS = ".highlight"
SA11Y = "sa11y-control-panel"

# axe test tags
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


# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#api-name-axeconfigure
class AxeConfigure(Base):
    """axe configuration model"""

    branding: str = None
    reporter: str = None
    checks: list = None
    rules: list = None
    standards: list = None
    disableOtherRules: bool = None
    local: str = None
    axeVersion: str = None
    noHtml: bool = False
    allowedOrigins: list = dataclasses.field(default_factory=["<same_origin>"].copy)


# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#options-parameter
class AxeOptions(Base):
    """axe options model"""

    runOnly: list = dataclasses.field(default_factory=TEST_TAGS.copy)
    rules: list = None
    reporter: str = None
    resultTypes: Any = None
    selectors: bool = None
    ancestry: bool = None
    xpath: bool = None
    absolutePaths: bool = None
    iframes: bool = True
    elementRef: bool = None
    frameWaitTime: int = None
    preload: bool = None
    performanceTimer: bool = None
    pingWaitTime: int = None


def get_npm_directory(package, data=False):
    """Get the path of an npm package in the environment"""
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))


@dataclasses.dataclass
class Collector(Base):
    """the Axe class is a fluent api for configuring and running accessibility tests."""

    url: str = None
    results: Any = None

    def configure(self):
        return self

    def exception(self):
        return self.results.exception()

    def raises(self):
        exc = self.exception()
        if exc:
            raise exc


class Results(Base):
    data: Any

    def raises(self):
        exc = self.exception()
        if exc:
            raise exc


@dataclasses.dataclass
class Axe(Collector):
    """the Axe class is a fluent api for configuring and running accessibility tests."""

    page: Any = None

    def __post_init__(self):
        self.page.goto(self.url)
        self.page.evaluate(get_axe())

    def configure(self, **config):
        self.page.evaluate(f"window.axe.configure({AxeConfigure(**config).dump()})")
        return self

    def run(self, test=None, options=None):
        self.results = AxeResults(
            self.page.evaluate(
                f"""window.axe.run({test and dumps(test) or "document"}, {AxeOptions(**options or {}).dump()})"""
            )
        )
        return self


class Violation(Exception, Base):
    map = {}

    def __class_getitem__(cls, id):
        bases = (cls,)
        if isinstance(id, tuple):
            id, bases = id
        if id in cls.map:
            return cls.map[id]
        return cls.map.setdefault(id, type(id, bases, {}))

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

    def __str__(self):
        return repr(self)


class AxeViolation(Violation):
    id: str = dataclasses.field(repr=False)
    impact: str | None = dataclasses.field(repr=False)
    tags: list = dataclasses.field(default=None, repr=False)
    description: str = ""
    help: str = ""
    helpUrl: str = ""
    nodes: list = dataclasses.field(default=None, repr=False)
    elements: dict = dataclasses.field(default_factory=partial(defaultdict, list))
    map = {}

    @classmethod
    def cast(cls, data):
        object = {"__doc__": f"""{data.get("help")} {data.get("helpUrl")}"""}
        name = "-".join((data["impact"], data["id"]))
        if name in cls.map:
            return cls.map.get(name)
        bases = ()
        # these generate types primitves
        if data["impact"]:
            bases += (AxeViolation[data["impact"]],)
        for tag in data["tags"]:
            bases += (AxeViolation[tag],)
        return cls.map.setdefault(name, type(name, bases, object))

    def get_elements(self, N=150):
        for node in self.nodes:
            key = node["html"]
            if len(key) > N:
                key = key[:N] + "..."
            self.elements[key].extend(node["target"])

    def __str__(self):
        try:
            self.get_elements()
            return repr(self)
        except BaseException as e:
            raise e

    @classmethod
    def from_violations(cls, data):
        out = []
        for violation in (violations := data.get("violations")):
            out.append(AxeViolation(**violation))

        return exceptiongroup.ExceptionGroup(f"{len(violations)} accessibility violations", out)


class AxeResults(Results):
    def exception(self):
        if self.data["violations"]:
            return AxeViolation.from_violations(self.data)


@lru_cache(1)
def get_axe():
    return (get_npm_directory("axe-core") / "axe.js").read_text()


@fixture()
def axe(page):
    def go(url, **axe_config):
        axe = Axe(page=page, url=url)
        axe.configure(**axe_config)
        return axe

    return go
