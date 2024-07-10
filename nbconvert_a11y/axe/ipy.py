import atexit
from dataclasses import dataclass, field
from pathlib import Path
from traceback import print_exception
from playwright.async_api import Browser, Playwright, async_playwright
from asyncio import gather, get_event_loop

from nbconvert_a11y.axe.types import AxeConfigure, AxeOptions
from nbconvert_a11y.pytest_w3c import ValidatorViolation
from nbconvert_a11y.axe.async_axe import validate_html


def run(*args, **kwargs):
    from asyncio import run

    return run(*args, **kwargs)


@dataclass
class Results: ...


@dataclass
class Playwright:
    axe_options: AxeOptions = field(default_factory=AxeOptions)
    axe_config: AxeConfigure = field(default_factory=AxeConfigure)
    pw: Playwright = None
    browser: Browser = None

    def enter(self):
        if self.pw is None:
            self.pw = async_playwright()

            self.ctx = run(self.pw.__aenter__())
            atexit.register(self.exit)
        if self.browser is None:
            self.browser = run(self.ctx.chromium.launch())
        return self

    def exit(self):
        run(self.ctx.__aexit__())

    def new_page(self, content):
        page = run(self.browser.new_page())
        if isinstance(content, Path):
            run(page.goto(content))
        elif isinstance(content, str):
            if content.lstrip().startswith("<"):
                run(page.set_content(content))
            elif "://" in content:
                run(page.goto(content))
        return page

    async def test_axe_page(self, page):
        from . import pw_test_axe

        return await pw_test_axe(page, '"body"', **self.axe_options.dict())

    async def test_vnu_page(self, page):
        from . import pw_validate_html

        return ValidatorViolation.from_violations(await pw_validate_html(page))

    def test_axe_html(self, html):
        return run(self.test_axe_page(self.new_page(html)))

    def test_vnu_html(self, html):
        return ValidatorViolation.from_violations(run(validate_html(html)))

    def axe_magic_cell(self, line, cell):
        from IPython.display import HTML, display

        page = self.new_page(cell)
        display(HTML(cell))
        axe = self.test_axe_page(page)
        if isinstance(axe, Exception):
            print_exception(axe)

    def html_magic_cell(self, line, cell):
        axe = vnu = True
        from IPython.display import HTML, display

        display(HTML(cell))
        page = self.new_page(cell)
        for x in run(gather(self.test_axe_page(page), self.test_vnu_page(page))):
            print(x)

            if isinstance(x, (Exception, ExceptionGroup)):
                print_exception(x)

    def vnu_magic_cell(self, line, cell):
        vnu = self.test_vnu_html(cell)
        if isinstance(vnu, Exception):
            print_exception(vnu)

    def line_magic(self, line, cell=None):
        pass


def load_ipython_extension(shell):
    from traitlets import Instance

    if not shell.has_trait("pw"):
        shell.add_traits(pw=Instance(Playwright, args=()))
        shell.register_magic_function(shell.pw.axe_magic_cell, "cell", "axe")
        shell.register_magic_function(shell.pw.vnu_magic_cell, "cell", "vnu")
        shell.register_magic_function(shell.pw.html_magic_cell, "cell", "html")
        from nest_asyncio import apply

        apply()
        shell.pw.enter()


def unload_ipython_extension(shell):
    pass
