"""a script to transform axe rules into python exceptions"""

from inspect import getsource
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
from unittest.mock import Base

HERE = Path(__file__).parent
GET_AXE_RULES = HERE / "get_axe_rules.mjs"
TARGET = HERE / ".." / "test_a11y" / "axe_exceptions.py"


def get_rules():
    """get the axe rules for the installed version of axe"""
    return json.loads(subprocess.check_output(["node", str(GET_AXE_RULES)]))


def get_version():
    """get the current axe-core version"""
    return subprocess.check_output(["npx", "axe", "--version"]).strip().decode()


def ruleId_to_name(ruleId):
    """convert axe rules name to valid python slugs"""
    return ruleId.replace(*"-_")


def rule_to_class(ruleId, description, help, helpUrl=None, tags=None, **kwargs):
    """create python code from a rule payload"""
    base = "object"
    if tags:
        base = ", ".join(
            [("cat." if tag.startswith("cat") else "") + tag_to_class_name(tag) for tag in tags]
        )

    return f"""
class {ruleId_to_name(ruleId)}({base}, ruleId="{ruleId}"):
    \"\"\"{description}
    
{help}

{helpUrl}\"\"\"
    
""".lstrip()
    # the helpurl will be clickable in a few contexts


def tag_to_class(tag):
    """convert an axe tag to a python class"""

    return f"""class {tag_to_class_name(tag)}(AxeException): ..."""


def tag_to_class_name(tag):
    """transform a tag name into valid python"""
    if tag.startswith(("TT", "EN", "section508")):
        tag = tag.replace(*"._")
    if tag.startswith("cat"):
        tag = tag.partition(".")[2]
    return tag.replace(*"-_")


tags = set()
impacts = set()
for rule in get_rules():
    tags.update(rule.get("tags") or ())
    tags.update(rule.get("impact") or ())


body = io.StringIO()
# should add the version
body.write(
    f"""
\"\"\"axe types generated from {Path(__file__).relative_to(os.path.abspath(HERE.parent))} for axe-core version v{get_version()}
\"\"\"

from .base_axe_exceptions import *
""".lstrip()
)

body.write("\n\n" * 2)

had_cats = cats = False
tags = sorted(tags)
for tag in tags:
    py = tag_to_class(tag)
    cats = tag.startswith("cat")
    if not had_cats and cats:
        body.write("class cat:")
        body.write("\n" * 2)
    if cats:
        body.write(" " * 4)
    body.write(py)
    body.write("\n" * 2)
    had_cats = cats

assert compile(body.getvalue(), "test framework", "exec"), "the python code is not valid"

for tag in impacts:
    py = tag_to_class(tag)
    body.write(py)
    body.write("\n" * 2)

assert compile(body.getvalue(), "test with impact", "exec"), "the python code is not valid"

body.write("\n" * 2)

rules = get_rules()

for rule in rules:
    body.write(rule_to_class(**rule))
    body.write("\n" * 2)

assert compile(body.getvalue(), "test", "exec")

print("valid python code generated.")

TARGET.write_text(body.getvalue())
(HERE / ".." / ".." / "nbconvert_a11y" / "axe" / "axe_exceptions.py").write_text(body.getvalue())
print(f"axe types written to {TARGET}")
