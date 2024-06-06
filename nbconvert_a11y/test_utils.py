from pathlib import Path
from nbconvert.nbconvertapp import NbConvertApp


# selectors for regions of the notebook
class SELECTORS:
    """ "selectors for notebook and third party components in notebooks."""

    # these should be moved to a config test.
    MATHJAX = "[id^=MathJax]"
    JUPYTER_WIDGETS = ".jupyter-widgets"
    OUTPUTS = ".jp-OutputArea-output"
    NO_ALT = "img:not([alt])"
    PYGMENTS = ".highlight"
    SA11Y = "sa11y-control-panel"
    THIRD_PARTY = JUPYTER_WIDGETS, MATHJAX, SA11Y


def get_exporter(config=None, **exporter_config):
    from nbconvert import get_exporter
    from traitlets.config import Config
    if config is None:
        config = "html"

    if isinstance(config, Path):
        app = NbConvertApp(config_file=str(config))
        app.load_config_file()
    if isinstance(config, str):
        app = NbConvertApp(export_format=config)
    elif isinstance(config, dict):
        app = NbConvertApp(config=Config(config))
    e = get_exporter(app.export_format)(config=app.config, **exporter_config)

    return get_exporter(app.export_format)(config=app.config, **exporter_config)


from playwright.sync_api import Page


def from_notebook(page, file, config=None, **exporter_config):
    print(config)
    page.set_content(
        get_exporter(
            config or {"NbConvertApp": {"export_format": "a11y"}}, **exporter_config
        ).from_filename(file)[0]
    )


Page.from_notebook = from_notebook
