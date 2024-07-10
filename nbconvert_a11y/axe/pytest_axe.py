"""fine-grained axe accessibility testing.

this module contains tooling to run headless browsers that assess the accessibility of web pages. 
the tooling can be used interactively in notebooks or as pytest fixtures

* an axe fixture to use in pytest
* a command line application for auditing files.

"""

# requires node and axe
# requires playwright
from functools import lru_cache
from json import dumps, loads
from pathlib import Path
from shlex import quote, split
from subprocess import CalledProcessError, check_output
from playwright.sync_api import Page
from pytest import fixture

from .async_axe import JS
from .base_axe_exceptions import AxeExceptions
from .types import AxeOptions


@lru_cache(1)
def get_axe():
    return (get_npm_directory("axe-core") / "axe.js").read_text()


# need to remove the node dependency by placing the js in the page
def get_npm_directory(package, data=False):
    """Get the path of an npm package in the environment"""
    try:
        info = loads(check_output(split(f"npm ls --long --depth 0 --json {quote(package)}")))
    except CalledProcessError:
        return None
    if data:
        return info
    return Path(info.get("dependencies").get(package).get("path"))


def inject_axe_sync(page):
    if not page.evaluate(JS.CHECK_FOR_AXE):
        page.evaluate(get_axe())


@fixture
def page_axe(page):
    """a playwright fixture that ensure axe is available to the page."""
    inject_axe_sync(page)
    return page


def pw_axe(page, include=None, exclude=None, **config):
    if not page.evaluate(JS.CHECK_FOR_AXE):
        page.evaluate(get_axe())
    # the axe context can take different combitions of include/exclude selectors
    # we use dict(include=..., exclude=...) if either are defined.
    # other we use the document, but a locator should use the selector.
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
