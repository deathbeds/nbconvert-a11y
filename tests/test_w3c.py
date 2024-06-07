# requires node
# requires jvm
from logging import getLogger
from pathlib import Path

import pytest

from nbconvert_a11y.pytest_w3c import ValidatorViolation, raise_if_errors, validate_html
from nbconvert_a11y.test_utils import get_exporter
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
                (CONFIGURATIONS / (a := "section")).with_suffix(".py"),
                (NOTEBOOKS / (b := "lorenz-executed")).with_suffix(".ipynb"),
            ),
            id="-".join((b, a)),
        ),
        pytest.param(
            get_target_html(
                (CONFIGURATIONS / (a := "list")).with_suffix(".py"),
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
def test_baseline_w3c_paths(html: Path, validate_html_path: "TVnuValidator") -> None:
    exc = validate_html_path(html).run().exception()
    try:
        raise exc
    except* ValidatorViolation["info"]:
        ...
    except* ValidatorViolation["error-Unrecognized at-rule “@layer”"]:
        ...
    except* ValidatorViolation["error-An “img” element must have an “alt” attribute, except under certain conditions. For details, consult guidance on providing text alternatives for images."]:
        ...

def test_a11y_max():
    html = get_exporter(CONFIGURATIONS / "a11y.py").from_filename(NOTEBOOKS / "lorenz-executed.ipynb")[0]
    exc = validate_html(html).exception()
    try:
        raise exc
    except* ValidatorViolation["info"]:
        ...
    except* ValidatorViolation["error-Unrecognized at-rule “@layer”"]:
        ...
    except* ValidatorViolation["error-Bad value “none” for attribute “role” on element “table”."]:
        ...


def xfail_default():
    html = get_exporter("html").from_filename(NOTEBOOKS / "lorenz-executed.ipynb")[0]
    exc = validate_html(html).exception()

    try:
        raise exc
    except* ValidatorViolation["error-Unknown pseudo-element or pseudo-class “:horizontal”"]:
        ...
    except* ValidatorViolation["error-Unknown pseudo-element or pseudo-class “:vertical”"]:
        ...
    except* ValidatorViolation["error-box-shadow"]:
        ...
    except* ValidatorViolation["error-overflow"]:
        ...
    except* ValidatorViolation["error-Stray start tag “script”."]:
        ...
    except* ValidatorViolation["info"]:
        ...
    finally:
        pytest.xfail("the default nbconvert template is non-conformant.")


def xfail_a11y_min():
    html = get_exporter("a11y").from_filename(NOTEBOOKS / "lorenz-executed.ipynb")[0]
    exc = validate_html(html).exception()
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
        pytest.xfail(
            "the minified a11y theme has superfluous idref's that need to conditionally removed."
        )
