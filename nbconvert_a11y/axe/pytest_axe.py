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
from playwright.sync_api import Page
from typing import Any

from pytest import fixture

from .async_axe import JS
from .base_axe_exceptions import AxeExceptions
from ..exceptions import Violation, Violations
from .types import AxeConfigure, AxeOptions, Base


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
            if isinstance(xfail, type):
                xfail = (xfail,)
            exception = exception.xfail(*xfail)
            if exception:
                raise exception


class AxeResults(Results):
    def exception(self):
        return AxeViolations.from_violations(self.data)


@fixture()
def axe(page):
    def go(url, **axe_config):
        axe = Axe(page=page, url=url)
        axe.configure(**axe_config)
        return axe

    return go


@lru_cache(1)
def get_axe():
    return (get_npm_directory("axe-core") / "axe.js").read_text()


def get_npm_directory(package, data=False):
    """Get the path of an npm package in the environment"""
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))


def pw_axe(page, include=None, exclude=None, **config):
    if not page.evaluate(JS.CHECK_FOR_AXE):
        page.evaluate(get_axe())

    if include:
        if exclude:
            ctx = dumps(dict(include=include, exclude=exclude))
        else:
            ctx = dumps(include)
    elif exclude:
        ctx = dumps(dict(exclude=exclude))
    else:
        ctx = "document"

    return page.evaluate(JS.RUN_AXE.format(ctx, dumps(AxeOptions(**config).dict())))


def pw_test_axe(page, include=None, **config):
    return AxeExceptions.from_test(pw_axe(page, include, **config))


# attach new attributes to the synchronous page

Page.axe = pw_axe
Page.test_axe = pw_test_axe
