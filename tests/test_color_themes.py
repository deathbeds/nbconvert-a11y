from nbconvert import get_exporter
from pytest import fixture, mark, param

from nbconvert_a11y.pytest_axe import JUPYTER_WIDGETS, MATHJAX, PYGMENTS, Axe
from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, get_target_html

LORENZ = NOTEBOOKS / "lorenz-executed.ipynb"
THEMES = ["a11y", "a11y-high-contrast", "gh", "gh-colorblind", "gh-high", "gotthard", "blinds"]


@fixture(params=THEMES)
def lorenz(page, tmp_path, request):
    e = get_exporter("a11y")()
    e.color_theme = request.param
    e.wcag_priority = "AA"
    html, *_ = e.from_filename(LORENZ)
    tmp = tmp_path / f"{request.param}.html"
    tmp.write_text(html)
    axe = Axe(page=page, url=tmp.absolute().as_uri())
    yield axe.configure()


@mark.xfail
def test_dark_themes(lorenz):
    lorenz.page.click("""[aria-controls="nb-settings"]""")
    lorenz.page.locator("select[name=color-scheme]").select_option("dark mode")
    lorenz.page.keyboard.press("Escape")
    lorenz.run(dict(include=[".nb-source"])).raises()
