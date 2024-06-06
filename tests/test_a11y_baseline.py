"""axe accessibility testing on exported nbconvert scripts.

* test the accessibility of exported notebooks
* test the accessibility of nbconvert-a11y dialogs
"""

from pytest import mark

from nbconvert_a11y.test_utils import SELECTORS as S
from conftest import NOTEBOOKS, CONFIGURATIONS


@mark.parametrize("config", ["a11y.py", "section.py", "list.py"])
@mark.parametrize("nb", ["lorenz-executed.ipynb"])
def test_axe(page, config, nb):
    """Verify the baseline templates satisify all rules update AAA.

    any modifications to the template can only degrade accessibility.
    this baseline is critical for adding more features. all testing piles
    up without automation. these surface protections allow more manual testing
    or verified conformations of html.
    """

    page.from_notebook(NOTEBOOKS / nb, CONFIGURATIONS / config)
    assert page.test_axe(exclude=S.THIRD_PARTY).xfail()
