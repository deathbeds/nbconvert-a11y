"""report axe violations in html content

* an axe fixture to use in pytest
* a command line application for auditing files.

"""

# requires node and axe
# requires playwright
from collections import defaultdict
import dataclasses
from functools import lru_cache, partial
from json import dumps, loads
from pathlib import Path
from shlex import quote, split
from subprocess import CalledProcessError, check_output
from typing import Any

import exceptiongroup
from attr import dataclass
from pytest import fixture, mark, param

nbconvert_a11y_DYNAMIC_TEST = "nbconvert_a11y_DYNAMIC_TEST"

axe_config_aa = {
    "runOnly": ["act", "best-practice", "experimental", "wcag21a", "wcag21aa", "wcag22aa"],
    "allowedOrigins": ["<same_origin>"],
}

axe_config_aaa = {
    "runOnly": [
        "act",
        "best-practice",
        "experimental",
        "wcag21a",
        "wcag21aa",
        "wcag22aa",
        "wcag2aaa",
    ],
    "allowedOrigins": ["<same_origin>"],
}

MATHJAX = "[id^=MathJax]"
tests_axe = {"exclude": [MATHJAX]}


def get_npm_directory(package, data=False):
    """get the path of an npm package in the environment"""
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))


@dataclass
class AxeResults:
    data: Any

    def raises(self):
        if self.data["violations"]:
            raise Violation.from_violations(self.data)
        return self

    def dump(self, file: Path):
        if file.is_dir():
            file /= "axe-results.json"
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text(dumps(self.data))
        return self


@dataclasses.dataclass
class Violation(Exception):
    id: str = dataclasses.field(repr=False)
    impact: str | None = dataclasses.field(repr=False)
    tags: list = dataclasses.field(default=None, repr=False)
    description: str = ""
    help: str = ""
    helpUrl: str = ""
    nodes: list = dataclasses.field(default=None, repr=False)
    elements: dict = dataclasses.field(default_factory=partial(defaultdict, list))
    map = {}

    def __class_getitem__(cls, id):
        if id in cls.map:
            return cls.map[id]
        return cls.map.setdefault(id, type(id, (Violation,), {}))

    def __new__(cls, **kwargs):
        if cls is Violation:
            target = cls.cast(kwargs)
            self = Exception.__new__(target)
            self.__init__(**kwargs)
            return self
        self = super().__new__(cls, **kwargs)
        self.__init__(**kwargs)
        return self

    @classmethod
    def cast(cls, data):
        object = {"__doc__": f"""{data.get("help")} {data.get("helpUrl")}"""}
        if data["id"] in cls.map:
            return cls.map.get(data["id"])(**data)
        bases = ()
        # these generate types primitves
        if data["impact"]:
            bases += (Violation[data["impact"]],)
        for tag in data["tags"]:
            bases += (Violation[tag],)
        return cls.map.setdefault(
            data["id"], type(("-".join((data["impact"], data["id"]))), bases, object)
        )

    def get_elements(self, N=150):
        for node in self.nodes:
            key = node["html"]
            if len(key) > N:
                key = key[:N] + "..."
            self.elements[key].extend(node["target"])

    def __str__(self):
        self.get_elements()
        return repr(self)

    @classmethod
    def from_violations(cls, data):
        out = []
        for violation in (violations := data.get("violations")):
            out.append(Violation(**violation))

        return exceptiongroup.ExceptionGroup(f"{len(violations)} accessibility violations", out)


@mark.parametrize("package", ["axe-core", param("axe-core-doesnt-ship-this", marks=mark.xfail)])
def test_non_package(package):
    assert get_npm_directory(package), "package not found."


@lru_cache(1)
def get_axe():
    return (get_npm_directory("axe-core") / "axe.js").read_text()


def inject_axe(page):
    page.evaluate(get_axe())


def run_axe_test(page, tests_config=None, axe_config=None):
    return AxeResults(
        page.evaluate(
            f"window.axe.run({tests_config and dumps(tests_config) or 'document'}, {dumps(axe_config or {})})"
        )
    )


@fixture()
def axe(page):
    def go(url, tests=tests_axe, axe_config=axe_config_aa):
        page.goto(url)
        inject_axe(page)
        return run_axe_test(page, tests, axe_config)

    return go
