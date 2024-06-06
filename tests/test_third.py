"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from os import environ
from unittest import TestCase

import pytest
from flask import url_for
from pytest import fixture, mark, skip

from nbconvert_a11y.axe.axe_exceptions import (
    color_contrast,
    color_contrast_enhanced,
    focus_order_semantics,
)
from nbconvert_a11y.test_utils import SELECTORS as S
from tests.conftest import CONFIGURATIONS, NOTEBOOKS

# only run these tests when the CI environment variables are defined.
environ.get("CI") or skip(allow_module_level=True)


class DefaultTemplate(TestCase):
    """automated accessibility testing of the default nbconvert light theme."""

    # test all of the accessibility violations
    # then incrementally explain them in smaller tests.
    # @mark.xfail(reason="there are problems in multiple upstreams.", raises=ExpectedFail)
    def xfail_all(self):
        self.page.test_axe().xfail(color_contrast, color_contrast_enhanced, focus_order_semantics)

    # @mark.xfail(reason="a different theme is needed.", raises=ExpectedFail)
    def xfail_pygments_highlight_default(self):
        """The default template has two serious color contrast violations.

        an issue needs to be opened or referenced.
        """
        # further verification would testing the nbviewer layer.
        self.page.test_axe({"include": [S.PYGMENTS]}).xfail(color_contrast, color_contrast_enhanced)

    # @mark.xfail(reason="an issue report needs to be filed with ipywidgets.", raises=ExpectedFail)
    def test_widget_display(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        self.page.test_axe({"include": [S.JUPYTER_WIDGETS], "exclude": [S.NO_ALT]}).xfail(
            focus_order_semantics
        )

    @fixture(autouse=True)
    def url(self, page):
        self.page = page
        page.from_notebook(NOTEBOOKS / "lorenz-executed.ipynb", "html")


class A11yTemplate(TestCase):
    def test_sa11y(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        self.page.test_axe({"include": [S.SA11Y]}).xfail()

    @fixture(autouse=True)
    def url(self, page):
        self.page = page
        page.from_notebook(NOTEBOOKS / "lorenz-executed.ipynb", CONFIGURATIONS / "a11y.py")
