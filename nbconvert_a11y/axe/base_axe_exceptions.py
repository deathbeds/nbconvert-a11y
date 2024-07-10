__all__ = ("AxeExceptions", "AxeException", "minor", "critical", "serious", "moderate")


from itertools import chain
from pprint import pformat
from typing import Union

from nbconvert_a11y.exceptions import Violations


class Success:
    def xfail(self, *xfail, strict=True):
        if strict and xfail:
            raise UnexpectedPass(*xfail)
        return True
    
    
class AxeExceptions(ExceptionGroup):
    def xfail(self, *xfail, strict=True):

        found = set(xfail)
        try:
            raise self
        except* xfail as e:
            for t in map(type, e.args[1]):
                found.difference_update(t.__mro__)
        if strict and found:
            raise UnexpectedPass(*found)
        return True
    
    @classmethod
    def from_violations(cls, violations, id=None):
        if not violations:
            return Success()
        exceptions = []
        summary = {}
        for violation in violations:
            summary.setdefault(violation["impact"], 0)
            summary[violation["impact"]] += 1
            exceptions.append(AxeException.from_violation(violation))

        group = AxeExceptions(
            "accessibility violations" + (id and F" for {id}" or ""),
            exceptions,
        )
        return group

    @classmethod
    def from_test(cls, test):
        return cls.from_violations(test["violations"], test.get("url", "") )

    @classmethod
    async def from_page(cls, page, **config):
        return cls.from_test(await page.axe(**config))


class UnexpectedPass(Exception):
    pass


class AxeException(Exception):
    ruleId_mapping = {}

    def __class_getitem__(cls, ruleId):
        return cls.ruleId_mapping[ruleId]

    def __init_subclass__(cls, ruleId=None):
        if ruleId:
            cls.ruleId_mapping[ruleId] = cls

    @property
    def violation(self):
        return self.args[1]
    
    @property
    def help(self):
        return self.args[0]
    
    @classmethod
    def from_violation(cls, violation):
        new_violation = dict(**violation)
        nodes = new_violation["nodes"] = []
        summary = set()
        for node in violation["nodes"]:
            summary.add(node["failureSummary"])
            nodes.append(new_node := dict(**node))
            new_node["html"] = new_node["html"][:100]
        klass = cls[violation["id"]]
        if impact := violation.get("impact"):
            klass = type(f"""{klass.__name__}_{impact}""", (klass, cls[impact]), {})
        return klass(next(iter(summary)), new_violation)

    @property
    def nodes(self):
        return [exc.args[0] for exc in self.args[1]]

    def get_selectors(self):
        return set(chain.from_iterable(node["target"] for node in self.violation["nodes"]))
    
    def __str__(self):
        return pformat(self.violation)
    
AXE_HELP_MSG = "Fix any of the following:"
# add base classes for the impact of an error this way we can easily filter something like minor
# https://github.com/dequelabs/axe-core/blob/develop/doc/issue_impact.md


class minor(AxeException): ...


class moderate(AxeException): ...


class serious(AxeException): ...


class critical(AxeException): ...


AxeException.ruleId_mapping.update(
    {"minor": minor, "moderate": moderate, "serious": serious, "critical": critical}
)
