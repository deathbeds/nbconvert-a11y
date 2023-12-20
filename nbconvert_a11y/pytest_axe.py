"""fine-grained axe accessibility testing.

this module contains tooling to run headless browsers that assess the accessibility of web pages. 
the tooling can be used interactively in notebooks or as pytest fixtures

* an axe fixture to use in pytest
* a command line application for auditing files.

"""

# requires node and axe
# requires playwright
import asyncio
from contextlib import AsyncExitStack
import dataclasses
from collections import defaultdict
from functools import lru_cache, partial
from json import dumps, loads
from pathlib import Path
from shlex import quote, split
from subprocess import CalledProcessError, check_output
from time import sleep, time
from typing import Any

import exceptiongroup
from pytest import fixture


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


# axe configuration should be a fixture.
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


# axe options should be a fixture
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


@dataclasses.dataclass
class Collector(Base):
    """the base collector class for accessibility and bulk testing batteries."""

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

    def __post_init__(self):
        self.add_note(f"{self.impact}: {self.description}")
        self.add_note(self.helpUrl)
        self.get_elements()
        if len(self.elements) > 1:
            self.add_note(f"affects {len(self.elements)} elements")
        for element in self.elements or "":
            self.add_note(element)

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

    def xfail(self, matches=None):
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


class AxeViolations(Violations):
    exception = AxeViolation

    @classmethod
    def from_violations(cls, data):
        if data["violations"]:
            exceptions = []
            for violation in (violations := data.get("violations")):
                exceptions.append(cls.exception(**violation))

            return cls("axe violations", exceptions)


@dataclasses.dataclass
class Axe(Collector):
    """the Axe class is a fluent api for configuring and running accessibility tests."""

    page: Any = None
    configured: bool = False
    exception = AxeViolation

    def __post_init__(self):
        url = self.url
        if isinstance(url, Path):
            url = url.absolute().as_uri()
        self.page.goto(url)
        self.page.evaluate(get_axe())

    def configure(self, **config):
        self.page.evaluate(f"window.axe.configure({AxeConfigure(**config).dump()})")
        self.configured = True
        return self

    def run(self, test=None, options=None, wait=None):
        if not self.configured:
            self.configure()
        if wait is not None:
            sleep(wait)
        self.results = AxeResults(
            self.page.evaluate(
                f"""window.axe.run({test and dumps(test) or "document"}, {AxeOptions(**options or {}).dump()})"""
            )
        )
        return self

    def screenshot(self, *args, **kwargs):
        if not self.snapshots:
            self.snapshots = []
        self.snapshots.append(self.page.screenshot(*args, **kwargs))
        return self.snapshots[-1]

    def raises(self, xfail=None):
        exception = self.results.exception()
        if exception:
            exception = exception.xfail(xfail)
            if exception:
                raise exception


@dataclasses.dataclass
class AsyncAxe(Axe, AsyncExitStack):
    """an axe collector that works with async playwright

    we need to run playwright in sync mode for tests, but
    we can't run playwright in sync mode in a notebook because
    it is executed in an event loop. this class adds
    compatability for async playwright usage for debugging.
    """

    playwright: Any = None
    browser: Any = None
    snapshots: list = None

    def __post_init__(self):
        AsyncExitStack.__init__(self)

    async def configure(self, **config):
        await self.page.evaluate(f"window.axe.configure({AxeConfigure(**config).dump()})")
        self.configured = True
        return self

    async def __aenter__(self):
        import playwright.async_api

        self.playwright = await self.enter_async_context(playwright.async_api.async_playwright())
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()
        await self.setup()

        return self

    async def __aexit__(self, *e):
        await self.browser.close()

    async def setup(self):
        url = self.url
        if isinstance(url, Path):
            url = url.absolute().as_uri()
        await self.page.goto(url)
        await self.page.evaluate(get_axe())
        return self

    async def run(self, test=None, options=None, wait=None):
        if not self.configured:
            await self.configure()
        if wait is not None:
            await asyncio.sleep(wait)
        self.results = AxeResults(
            await self.page.evaluate(
                f"""window.axe.run({test and dumps(test) or "document"}, {AxeOptions(**options or {}).dump()})"""
            )
        )
        return self

    async def screenshot(self, *args, **kwargs):
        if not self.snapshots:
            self.snapshots = []
        self.snapshots.append(await self.page.screenshot(*args, **kwargs))
        return self.snapshots[-1]


class AxeResults(Results):
    def exception(self):
        return AxeViolations.from_violations(self.data)


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


def get_npm_directory(package, data=False):
    """Get the path of an npm package in the environment"""
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))
