#!/usr/bin/env python3
"""Lightweight structural checks for the credential-free ProjectClash rule scheme."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "rules" / "ClashRules.yaml"
text = PATH.read_text(encoding="utf-8")

# This repo must not contain node credentials. Detect common config keys
# (not domains mentioned in ordinary routing rules).
for pattern in [
    r"(?m)^(?:proxies|proxy-providers):",
    r"(?mi)^\s*(?:password|uuid|secret|token|server|alterId):",
]:
    if re.search(pattern, text):
        sys.exit("FAIL: possible node source/credentials detected")


config = yaml.safe_load(text)
assert isinstance(config, dict), "root must be a YAML mapping"
groups = config.get("proxy-groups", [])
providers = config.get("rule-providers", {})
rules = config.get("rules", [])

assert isinstance(groups, list) and groups, "proxy-groups must be a non-empty list"
assert isinstance(providers, dict), "rule-providers must be a mapping"
assert isinstance(rules, list) and rules, "rules must be non-empty"
names = [g["name"] for g in groups]
assert len(names) == len(set(names)), "duplicate proxy group names"
assert len(rules) == len(set(rules)), "duplicate routing rules"
assert rules[-1].startswith("MATCH,"), "last rule must be MATCH"
assert sum(1 for r in rules if r.startswith("MATCH,")) == 1, "exactly one MATCH rule required"

builtins = {"DIRECT", "REJECT", "REJECT-DROP", "PASS", "COMPATIBLE", "GLOBAL"}
for group in groups:
    assert group["type"] in {"select", "url-test", "fallback", "load-balance"}, group
    for target in group.get("proxies", []):
        assert target in names or target in builtins, f"unknown proxy group reference {target!r}"
    if group.get("type") == "url-test":
        assert group.get("url"), f"missing url-test URL in {group['name']!r}"
        assert group.get("include-all") or group.get("proxies"), f"empty url-test group {group['name']!r}"
    for k in ("filter", "exclude-filter"):
        if k in group:
            re.compile(group[k])

for rule in rules:
    parts = rule.split(",")
    assert len(parts) >= 2, f"invalid rule: {rule}"
    if parts[0] == "RULE-SET":
        assert len(parts) >= 3 and parts[1] in providers, f"unknown rule provider: {rule}"
        target = parts[2]
    elif parts[0] == "AND":
        # AND conditions contain commas inside nested expressions. The target
        # is therefore the final field, rather than parts[2].
        target = parts[-1]
    else:
        target = parts[-1] if parts[0] == "MATCH" else parts[2]
    assert target in names or target in builtins, f"unknown target in rule: {rule}"

for name, provider in providers.items():
    assert provider.get("type") == "http", f"unexpected provider type {name}"
    assert provider.get("format") == "mrs", f"unexpected provider format {name}"
    assert provider.get("behavior") in ("domain", "ipcidr"), name
    assert str(provider.get("url", "")).startswith("https://"), name

print(f"PASS: {len(groups)} groups, {len(providers)} MRS providers, {len(rules)} rules")
