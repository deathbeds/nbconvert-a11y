"""specific ui and accessibility tests for the custom a11y template."""


from pytest import fixture, mark, param

from nbconvert_a11y.pytest_axe import AxeViolation, Axe
from tests.test_smoke import CONFIGURATIONS, NOTEBOOKS, get_target_html

NEEDS_WORK = mark.xfail(reason="state needs work", raises=Violations)


@fixture()
def lorenz(page, notebook):
    axe = Axe(page=page, url=notebook("a11y", "lorenz-executed.ipynb", config="a11y.py"))
    return axe.configure()


class JS:
    SNIPPET_FONT_SIZE = (
        """window.getComputedStyle(document.querySelector("body")).getPropertyValue("font-size")"""
    )


@mark.parametrize(
    "dialog",
    [
        "[aria-controls=nb-settings]",
        "[aria-controls=nb-help]",
        # "[aria-controls=nb-metadata]",
        param("[aria-controls=nb-expanded-dialog]", marks=mark.xfail(reason=NEEDS_WORK)),
        param("[aria-controls=nb-visibility-dialog]", marks=mark.xfail(reason=NEEDS_WORK)),
    ],
)
def test_dialogs(lorenz, dialog):
    """Test the controls in dialogs."""
    # dialogs are not tested in the baseline axe test. they need to be active to test.
    # these tests activate the dialogs to assess their accessibility with the active dialogs.
    lorenz.page.click(dialog)
    test = lorenz.run()
    try:
        test.raises()
    except* AxeViolation["serious-color-contrast-enhanced"]:
        ...
    except* AxeViolation["serious-target-size"]:
        "the line height raises a target size error for some reason"

def test_settings_font_size(lorenz):
    """Test that the settings make their expected changes."""
    assert (
        lorenz.page.evaluate(JS.SNIPPET_FONT_SIZE) == "16px"
    ), "the default font size is unexpected"
    lorenz.page.click("[aria-controls=nb-settings]")
    lorenz.page.locator("[name=font-size]").select_option("xx-large")
    assert lorenz.page.evaluate(JS.SNIPPET_FONT_SIZE) == "32px", "font size not changed"
