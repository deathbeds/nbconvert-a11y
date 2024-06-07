
# the default test tags start with the most strict conditions.
# end-users can refine the TEST_TAGS they choose in their axe configuration.
# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#axe-core-tags
import dataclasses
from json import dumps
from typing import Any


TEST_TAGS = [
    "ACT",
    "best-practice",
    "experimental",
    "wcag2a",
    "wcag2aa",
    "wcag2aaa",
    "wcag21a",
    "wcag21aa",
    "wcag22aa",
    "TTv5",
]


class Base:
    """base class for exceptions and models"""

    def __init_subclass__(cls) -> None:
        dataclasses.dataclass(cls)

    def dict(self):
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}

    def dump(self):
        return dumps(self.dict())


# axe configuration should be a fixture.
# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#api-name-axeconfigure
class AxeConfigure(Base):
    """axe configuration model"""

    branding: str = None
    reporter: str = None
    checks: list = None
    rules: list = None
    standards: list = None
    disableOtherRules: bool = None
    local: str = None
    axeVersion: str = None
    noHtml: bool = False
    allowedOrigins: list = dataclasses.field(default_factory=["<same_origin>"].copy)


# axe options should be a fixture
# https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#options-parameter
class AxeOptions(Base):
    """axe options model"""

    runOnly: list = dataclasses.field(default_factory=TEST_TAGS.copy)
    rules: list = None
    reporter: str = None
    resultTypes: Any = None
    selectors: bool = None
    ancestry: bool = None
    xpath: bool = None
    absolutePaths: bool = None
    iframes: bool = True
    elementRef: bool = None
    frameWaitTime: int = None
    preload: bool = None
    performanceTimer: bool = None
    pingWaitTime: int = None

