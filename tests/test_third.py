"""these tests verify how third party tools effect the accessibility of rendered notebook components.

these tests allow us to track ongoing community progress and record inaccessibilities
upstream of our control.
"""

from os import environ
from unittest import TestCase

import pytest
from flask import url_for
from pytest import fixture, mark, skip

from nbconvert_a11y.pytest_axe import SELECTORS as S, ExpectedFail, Violation

# only run these tests when the CI environment variables are defined.
environ.get("CI") or skip(allow_module_level=True)


class DefaultTemplate(TestCase):
    """automated accessibility testing of the default nbconvert light theme."""

    # test all of the accessibility violations
    # then incrementally explain them in smaller tests.
    @mark.xfail(reason="there are problems in multiple upstreams.", raises=ExpectedFail)
    def xfail_all(self):
        self.axe.run().raises(
            xfail=(
                self.axe.exception["critical-image-alt"],
                self.axe.exception["serious-color-contrast-enhanced"],
                self.axe.exception["serious-aria-input-field-name"],
                self.axe.exception["serious-color-contrast"],
                self.axe.exception["minor-focus-order-semantics"],
            )
        )

    @mark.xfail(reason="a different theme is needed.", raises=ExpectedFail)
    def xfail_pygments_highlight_default(self):
        """The default template has two serious color contrast violations.

        an issue needs to be opened or referenced.
        """
        # further verification would testing the nbviewer layer.
        self.axe.run({"include": [S.PYGMENTS]}).raises(
            xfail=(
                self.axe.exception["serious-color-contrast-enhanced"],
                self.axe.exception["serious-color-contrast"],
            )
        )

    @mark.xfail(reason="an issue report needs to be filed with ipywidgets.", raises=ExpectedFail)
    def xfail_widget_display(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        self.axe.run({"include": [S.JUPYTER_WIDGETS], "exclude": [S.NO_ALT]}).raises(
            xfail=(
                self.axe.exception["minor-focus-order-semantics"],
                self.axe.exception["serious-aria-input-field-name"],
            )
        )

    @fixture(autouse=True)
    def url(self, axe, notebook):
        self.axe = axe(notebook("html", "lorenz-executed.ipynb")).configure()


class A11yTemplate(TestCase):
    @mark.xfail(reason="an issue report needs to be filed with sa11y.", raises=ExpectedFail)
    def xfail_sa11y(self):
        """The simple lorenz widget generates one minor and one serious accessibility violation."""
        self.axe.run({"include": [S.SA11Y]}).raises(
            xfail=(self.axe.exception["serious-label-content-name-mismatch"])
        )

    @fixture(autouse=True)
    def url(self, axe, notebook):
        self.axe = axe(notebook("a11y", "lorenz-executed.ipynb", include_sa11y=True)).configure()


class FlaskDev(TestCase):
    """there are accessibility violations in the flask debug templates.

    flask is taught commonly enough that having accessible debugging sessions
    is critical for assistive technology users learning app development.
    """

    @mark.xfail(raises=ExpectedFail)
    def xfail_flask_dev(self):
        self.axe.run().raises(
            xfail=(
                self.axe.exception["serious-color-contrast-enhanced"],
                self.axe.exception["serious-color-contrast"],
                self.axe.exception["minor-empty-heading"],
                self.axe.exception["moderate-landmark-one-main"],
                self.axe.exception["moderate-region"],
            )
        )

    @fixture(autouse=True)
    def url(self, axe, live_server):
        # the query string causes the web server to raise an error so we can test flask dev tools
        self.axe = axe(url_for("bad", foo="bar", _external=True)).configure()
