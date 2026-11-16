#!/usr/bin/env python3
"""Run lightweight URL regression tests for module rewrite patterns."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "module_matchers.yaml"


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def load(path):
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        fail(f"{path.relative_to(ROOT)}: cannot read YAML: {error}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: root must be a mapping")
    return value


def pattern_for(section, item):
    if section == "url-rewrite":
        parts = item.split(None, 2)
    else:
        parts = item.split(None, 1)
    if not parts:
        return None
    return parts[0]


manifest = load(CASES)
cases = manifest.get("cases")
if not isinstance(cases, list) or not cases:
    fail("tests/module_matchers.yaml must contain cases")

for case in cases:
    if not isinstance(case, dict):
        fail("each matcher case must be a mapping")
    module = ROOT / str(case.get("module", ""))
    section = str(case.get("section", ""))
    url = str(case.get("url", ""))
    if section not in {"rewrite", "url-rewrite", "body-rewrite"}:
        fail(f"unsupported section in case: {section}")
    if not module.is_file() or not url:
        fail(f"invalid matcher case: {case}")

    config = load(module)
    http = config.get("http") or {}
    patterns = [pattern_for(section, item) for item in http.get(section, []) or []]
    patterns = [pattern for pattern in patterns if pattern]
    matches = []
    for pattern in patterns:
        try:
            if re.search(pattern, url):
                matches.append(pattern)
        except re.error as error:
            fail(f"{module.relative_to(ROOT)}: invalid regex {pattern}: {error}")
    if not matches:
        fail(f"no {section} pattern matched {url} in {module.relative_to(ROOT)}")

print(f"PASS: {len(cases)} module URL matcher cases")
