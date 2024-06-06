"""async playwright axe testing

axe accessibility tests are only applicable to html versions of documents
and we need to control them with a web driver. this library relies on playwright, 
but it probably would not be too difficult to generalize this for selenium.

the easiest way to use axe is through the playwright page at the end of the script we append new convenience methods to the public playwright api."""

from asyncio import create_subprocess_shell
from functools import lru_cache
from json import dumps, loads
from pathlib import Path
from subprocess import PIPE, check_output
from playwright.async_api import Page

from .base_axe_exceptions import AxeExceptions

OUTER_HTML = "(node) => node.outerHTML"
HTML_OUTER_HTML = """document.querySelector("html").outerHTML"""
CHECK_FOR_AXE = """window.hasOwnProperty("axe")"""
RUN_AXE = """window.axe.run({}, {})"""
VNU_TEST = "vnu --format json -"


class JS:
    OUTER_HTML = "(node) => node.outerHTML"
    HTML_OUTER_HTML = """document.querySelector("html").outerHTML"""
    CHECK_FOR_AXE = """window.hasOwnProperty("axe")"""
    RUN_AXE = """window.axe.run({}, {})"""
    VNU_TEST = "vnu --format json -"


@lru_cache(1)
def get_axe() -> str:
    return (
        Path(check_output("npm root axe-core".split()).strip().decode()) / "axe-core/axe.js"
    ).read_text()


async def pw_axe(page: Page, selector=None, **config):
    # we should be able to type output
    if not (await page.evaluate(CHECK_FOR_AXE)):
        await page.evaluate(get_axe())
    return await page.evaluate(RUN_AXE.format(selector or "document", dumps(config)))


async def pw_test_axe(page: Page, selector=None, **config):
    return AxeExceptions.from_test(await pw_axe(page, selector, **config))


async def validate_html(html: str) -> dict:
    # we should be able to type output
    process = await create_subprocess_shell(VNU_TEST, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _, stderr = await process.communicate(html.encode())
    return loads(stderr)


async def pw_validate_html(page):
    return await validate_html(await page.outer_html())


async def pw_screenshots(page, *selectors):
    from IPython.display import Image

    shots = {}
    for selector in selectors:
        shots.setdefault(selector, [])
        async for shot in _pw_selected(page.locator(selector)):
            shots[selector].append(Image(data=shot))
    return shots


async def _pw_selected(selected):
    for nth in range(await selected.count()):
        select = selected.nth(nth)
        yield await select.screenshot()


async def pw_outer_html(page: Page):
    return await page.evaluate(HTML_OUTER_HTML)


async def pw_accessibility_tree(page: Page):
    return await page.accessibility.snapshot()


Page.vnu = pw_validate_html
Page.axe = pw_axe
Page.test_axe = pw_test_axe
Page.screenshots = pw_screenshots
Page.outer_html = pw_outer_html
Page.aom = pw_accessibility_tree
