from typing import Any, Dict, List, Literal, Required, TypedDict, Union


class _AxeFullStopAxeResults(TypedDict, total=False):
    """Object for axe Results"""

    inapplicable: Required[List["_AxeFullStopResult"]]
    """ Required property """

    incomplete: Required[List["_AxeFullStopResult"]]
    """ Required property """

    passes: Required[List["_AxeFullStopResult"]]
    """ Required property """

    testEngine: Required["_AxeFullStopTestEngine"]
    """ Required property """

    testEnvironment: Required["_AxeFullStopTestEnvironment"]
    """ Required property """

    testRunner: Required["_AxeFullStopTestRunner"]
    """ Required property """

    timestamp: Required[str]
    """ Required property """

    toolOptions: Required["_AxeFullStopRunOptions"]
    """ Required property """

    url: Required[str]
    """ Required property """

    violations: Required[List["_AxeFullStopResult"]]
    """ Required property """


class _AxeFullStopCheckResult(TypedDict, total=False):
    data: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """ Required property """

    id: Required[str]
    """ Required property """

    impact: Required[str]
    """ Required property """

    message: Required[str]
    """ Required property """

    relatedNodes: List["_AxeFullStopRelatedNode"]


_AxeFullStopCrossTreeSelector = Union[
    str, "_AxeFullStopMultiArrayPercentSign3CaxeFullStopBaseSelectorPercentSign3E"
]
""" Aggregation type: anyOf """


_AxeFullStopImpactValue = Union[
    Literal["minor"], Literal["moderate"], Literal["serious"], Literal["critical"], Literal[None]
]
_AXEFULLSTOPIMPACTVALUE_MINOR: Literal["minor"] = "minor"
"""The values for the '_AxeFullStopImpactValue' enum"""
_AXEFULLSTOPIMPACTVALUE_MODERATE: Literal["moderate"] = "moderate"
"""The values for the '_AxeFullStopImpactValue' enum"""
_AXEFULLSTOPIMPACTVALUE_SERIOUS: Literal["serious"] = "serious"
"""The values for the '_AxeFullStopImpactValue' enum"""
_AXEFULLSTOPIMPACTVALUE_CRITICAL: Literal["critical"] = "critical"
"""The values for the '_AxeFullStopImpactValue' enum"""
_AXEFULLSTOPIMPACTVALUE_NONE: Literal[None] = None
"""The values for the '_AxeFullStopImpactValue' enum"""


_AxeFullStopMultiArrayPercentSign3CaxeFullStopBaseSelectorPercentSign3E = List[str]
""" minItems: 2 """


class _AxeFullStopNodeResult(TypedDict, total=False):
    all: Required[List["_AxeFullStopCheckResult"]]
    """ Required property """

    ancestry: List["_AxeFullStopCrossTreeSelector"]
    any: Required[List["_AxeFullStopCheckResult"]]
    """ Required property """

    failureSummary: str
    html: Required[str]
    """ Required property """

    impact: "_AxeFullStopImpactValue"
    none: Required[List["_AxeFullStopCheckResult"]]
    """ Required property """

    target: Required[List["_AxeFullStopCrossTreeSelector"]]
    """ Required property """

    xpath: List[str]


class _AxeFullStopRelatedNode(TypedDict, total=False):
    ancestry: List["_AxeFullStopCrossTreeSelector"]
    html: Required[str]
    """ Required property """

    target: Required[List["_AxeFullStopCrossTreeSelector"]]
    """ Required property """

    xpath: List[str]


_AxeFullStopReporterVersion = Union[
    Literal["v1"], Literal["v2"], Literal["raw"], Literal["raw-env"], Literal["no-passes"]
]
_AXEFULLSTOPREPORTERVERSION_V1: Literal["v1"] = "v1"
"""The values for the '_AxeFullStopReporterVersion' enum"""
_AXEFULLSTOPREPORTERVERSION_V2: Literal["v2"] = "v2"
"""The values for the '_AxeFullStopReporterVersion' enum"""
_AXEFULLSTOPREPORTERVERSION_RAW: Literal["raw"] = "raw"
"""The values for the '_AxeFullStopReporterVersion' enum"""
_AXEFULLSTOPREPORTERVERSION_RAW_ENV: Literal["raw-env"] = "raw-env"
"""The values for the '_AxeFullStopReporterVersion' enum"""
_AXEFULLSTOPREPORTERVERSION_NO_PASSES: Literal["no-passes"] = "no-passes"
"""The values for the '_AxeFullStopReporterVersion' enum"""


class _AxeFullStopResult(TypedDict, total=False):
    description: Required[str]
    """ Required property """

    help: Required[str]
    """ Required property """

    helpUrl: Required[str]
    """ Required property """

    id: Required[str]
    """ Required property """

    impact: "_AxeFullStopImpactValue"
    nodes: Required[List["_AxeFullStopNodeResult"]]
    """ Required property """

    tags: Required[List[str]]
    """ Required property """


_AxeFullStopResultGroups = Union[
    Literal["inapplicable"], Literal["passes"], Literal["incomplete"], Literal["violations"]
]
_AXEFULLSTOPRESULTGROUPS_INAPPLICABLE: Literal["inapplicable"] = "inapplicable"
"""The values for the '_AxeFullStopResultGroups' enum"""
_AXEFULLSTOPRESULTGROUPS_PASSES: Literal["passes"] = "passes"
"""The values for the '_AxeFullStopResultGroups' enum"""
_AXEFULLSTOPRESULTGROUPS_INCOMPLETE: Literal["incomplete"] = "incomplete"
"""The values for the '_AxeFullStopResultGroups' enum"""
_AXEFULLSTOPRESULTGROUPS_VIOLATIONS: Literal["violations"] = "violations"
"""The values for the '_AxeFullStopResultGroups' enum"""


class _AxeFullStopRuleObjectAdditionalproperties(TypedDict, total=False):
    enabled: Required[bool]
    """ Required property """


class _AxeFullStopRunOnly(TypedDict, total=False):
    type: Required["_AxeFullStopRunOnlyType"]
    """ Required property """

    values: Required["_AxeFullStopRunOnlyValues"]
    """
    Aggregation type: anyOf

    Required property
    """


_AxeFullStopRunOnlyType = Union[Literal["rule"], Literal["rules"], Literal["tag"], Literal["tags"]]
_AXEFULLSTOPRUNONLYTYPE_RULE: Literal["rule"] = "rule"
"""The values for the '_AxeFullStopRunOnlyType' enum"""
_AXEFULLSTOPRUNONLYTYPE_RULES: Literal["rules"] = "rules"
"""The values for the '_AxeFullStopRunOnlyType' enum"""
_AXEFULLSTOPRUNONLYTYPE_TAG: Literal["tag"] = "tag"
"""The values for the '_AxeFullStopRunOnlyType' enum"""
_AXEFULLSTOPRUNONLYTYPE_TAGS: Literal["tags"] = "tags"
"""The values for the '_AxeFullStopRunOnlyType' enum"""


_AxeFullStopRunOnlyValues = Union[List[str], List[str]]
""" Aggregation type: anyOf """


class _AxeFullStopRunOptions(TypedDict, total=False):
    absolutePaths: bool
    ancestry: bool
    elementRef: bool
    frameWaitTime: Union[int, float]
    iframes: bool
    performanceTimer: bool
    pingWaitTime: Union[int, float]
    preload: bool
    reporter: "_AxeFullStopReporterVersion"
    resultTypes: List["_AxeFullStopResultGroups"]
    rules: Dict[str, "_AxeFullStopRuleObjectAdditionalproperties"]
    runOnly: "_AxeFullStopRunOptionsRunonly"
    """ Aggregation type: anyOf """

    selectors: bool
    xpath: bool


_AxeFullStopRunOptionsRunonly = Union["_AxeFullStopRunOnly", List[str], List[str], str]
""" Aggregation type: anyOf """


class _AxeFullStopTestEngine(TypedDict, total=False):
    name: Required[str]
    """ Required property """

    version: Required[str]
    """ Required property """


class _AxeFullStopTestEnvironment(TypedDict, total=False):
    orientationAngle: Union[int, float]
    orientationType: str
    userAgent: Required[str]
    """ Required property """

    windowHeight: Required[Union[int, float]]
    """ Required property """

    windowWidth: Required[Union[int, float]]
    """ Required property """


class _AxeFullStopTestRunner(TypedDict, total=False):
    name: Required[str]
    """ Required property """


class _Root(TypedDict, total=False):
    options: Required["_AxeFullStopRunOptions"]
    """ Required property """

    results: Required["_AxeFullStopAxeResults"]
    """
    Object for axe Results

    Required property
    """
