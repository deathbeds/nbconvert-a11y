from time import sleep
from pytest import fixture

from nbconvert_a11y.exporter import THEMES
from tests.conftest import CONFIGURATIONS, NOTEBOOKS
from playwright.sync_api import expect
import nbconvert_a11y.test_utils

LORENZ = "lorenz-executed.ipynb"


@fixture(params=list(THEMES))
def lorenz(page, request):
    nb, config = NOTEBOOKS / LORENZ, CONFIGURATIONS / "a11y.py"
    page.from_notebook(
        nb, config, color_theme=request.param, include_settings=True, wcag_priority="AA"
    )
    return page


def test_dark_themes(lorenz):
    lorenz.click("""[aria-controls="nb-settings"]""")
    lorenz.locator("select[name=color-scheme]").select_option("dark mode")
    lorenz.keyboard.press("Escape")
    _test_no_textarea(lorenz)
    # verify the themes are consistent
    assert lorenz.locator(f"#nb-light-highlight").get_attribute("media") == "not screen"
    assert lorenz.test_axe(dict(include=[".nb-source"])).xfail()
    # accessible pygments disclsoes that we should expect some color contrast failures on some themes.
    # there isnt much code which might not generate enough conditions to create color contrast issues.


def test_light_themes(lorenz):
    _test_no_textarea(lorenz)
    assert lorenz.locator(f"#nb-dark-highlight").get_attribute("media") == "not screen"
    assert lorenz.test_axe(dict(include=[".nb-source"])).xfail()


def _test_no_textarea(page):
    for element in page.locator("textarea.nb-source").all():
        expect(element).not_to_be_visible()
