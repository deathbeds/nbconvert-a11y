"""specific ui and accessibility tests for the custom a11y template."""

from turtle import color
from pytest import fixture, mark, param

from nbconvert_a11y.axe.axe_exceptions import color_contrast_enhanced, empty_table_header, focus_order_semantics, target_size, td_has_header
from nbconvert_a11y.axe.base_axe_exceptions import AxeExceptions
from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS
import nbconvert_a11y.test_utils

NEEDS_WORK = mark.xfail(reason="state needs work", raises=AxeExceptions)


@fixture()
def lorenz(page):
    page.from_notebook(NOTEBOOKS / "lorenz-executed.ipynb", CONFIGURATIONS / "a11y.py")
    return page


class JS:
    SNIPPET_FONT_SIZE = (
        """window.getComputedStyle(document.querySelector("body")).getPropertyValue("font-size")"""
    )


@mark.parametrize(
    "dialog",
    [
        "[aria-controls=nb-settings]",
        "[aria-controls=nb-help]",
        param("[aria-controls=nb-visibility-dialog]", marks=NEEDS_WORK),
    ],
)
def test_dialogs(lorenz, dialog):
    """Test the controls in dialogs."""
    # dialogs are not tested in the baseline axe test. they need to be active to test.
    # these tests activate the dialogs to assess their accessibility with the active dialogs.
    lorenz.click(dialog)
    try:
        assert lorenz.test_axe().xfail(empty_table_header, td_has_header)
    except* (color_contrast_enhanced, target_size, focus_order_semantics):
        pass


def test_settings_font_size(lorenz):
    """Test that the settings make their expected changes."""
    assert lorenz.evaluate(JS.SNIPPET_FONT_SIZE) == "16px", "the default font size is unexpected"
    lorenz.click("[aria-controls=nb-settings]")
    lorenz.locator("[name=font-size]").select_option("xx-large")
    assert lorenz.evaluate(JS.SNIPPET_FONT_SIZE) == "32px", "font size not changed"
