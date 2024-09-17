"""a demonstration of the ability to test jupyterlab and notebook builds
using jupyak exports."""


from os import environ
from time import sleep

import pytest

from nbconvert_a11y.pytest_axe import AxeViolation

CI = environ.get("CI")

def xfail_yak_16(axe):
    lite = axe(
        "https://jupyak--16.org.readthedocs.build/en/16/_static/work/lite/lab/"
    )
    sleep(CI and 20 or 10) # the longer sleep time the less flaky the load
    
    try:
        raise lite.run().exception()
    except* AxeViolation["critical-aria-allowed-attr"]:
        ...
    except* AxeViolation["serious-aria-prohibited-attr"]:
        ...
    except* AxeViolation["critical-aria-required-attr"]:
        ...
    except* AxeViolation["critical-button-name"]:
        ...
    except* AxeViolation["minor-empty-heading"]:
        ...
    except* AxeViolation["minor-focus-order-semantics"]:
        ...
    pytest.xfail("we knew this.")
