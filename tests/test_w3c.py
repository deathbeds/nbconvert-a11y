# requires node
# requires jvm
from logging import getLogger
from pathlib import Path

import pytest
import requests
from nbconvert_a11y.pytest_w3c import ValidatorViolation, raise_if_errors

from tests.test_smoke import CONFIGURATIONS, get_target_html

HERE = Path(__file__).parent
NOTEBOOKS = HERE / "notebooks"
EXPORTS = HERE / "exports"
HTML = EXPORTS / "html"
LOGGER = getLogger(__name__)
VALIDATOR = EXPORTS / "validator"

# it would be possible to test loaded baseline documents with playwright.
# export the resting state document and pass them to the validator.
# this would be better validate widgets.

INVALID_MARKUP = pytest.mark.xfail(reason="invalid html markup")


htmls = pytest.mark.parametrize(
    "html",
    [
        pytest.param(
            get_target_html(
                (CONFIGURATIONS / (a := "a11y")).with_suffix(".py"),
                (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            ),
            id="-".join((b, a)),
        ),
        pytest.param(
            get_target_html(
                (CONFIGURATIONS / (a := "default")).with_suffix(".py"),
                (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            ),
            marks=[INVALID_MARKUP],
            id="-".join((b, a)),
        ),
    ],
)


@htmls
def test_baseline_w3c_paths(html: Path, validate_html_file: "TVnuValidator") -> None:
    result = validate_html_file(html)
    raise_if_errors(result)


def xfail_baseline_a11y_min(notebook, validate_html_url):
    exc = validate_html_url(notebook()).run().exception()
    try:
        raise exc
    except* ValidatorViolation[
        "error-The “aria-labelledby” attribute must point to an element in the same document."
    ]:
        ...
    except* ValidatorViolation[
        "error-The “aria-describedby” attribute must point to an element in the same document."
    ]:
        ...
    except* ValidatorViolation["info"]:
        ...
    finally:
        pytest.xfail("the minified a11y theme has superfluous idref's that need to conditionally removed.")