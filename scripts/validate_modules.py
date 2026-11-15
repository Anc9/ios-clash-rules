#!/usr/bin/env python3
"""Structural checks for ProjectClash HTTPS modules."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
BUILTIN_ACTIONS = {
    "DIRECT", "REJECT", "REJECT-DROP", "REJECT-200", "REJECT-DICT",
    "REJECT-ARRAY", "REJECT-IMG", "REJECT-TINYGIF", "REJECT-VIDEO",
}

def fail(message):
    raise SystemExit("FAIL: " + message)

for path in sorted(MODULES.glob("*.stoverride")):
    text = path.read_text(encoding="utf-8")
    for pattern in (
        r"(?m)^(?:proxies|proxy-providers):",
        r"(?mi)^\s*(?:password|uuid|secret|token|server|alterId):",
    ):
        if re.search(pattern, text):
            fail(f"{path.name}: possible node source or credential")

    try:
        config = yaml.safe_load(text)
    except yaml.YAMLError as error:
        fail(f"{path.name}: invalid YAML: {error}")

    if not isinstance(config, dict):
        fail(f"{path.name}: root must be a mapping")

    for key in ("name", "desc", "author", "category", "version", "date"):
        if not str(config.get(key, "")).strip():
            fail(f"{path.name}: missing metadata field {key}")

    providers = config.get("rule-providers", {})
    if not isinstance(providers, dict):
        fail(f"{path.name}: rule-providers must be a mapping")
    for name, provider in providers.items():
        if not isinstance(provider, dict):
            fail(f"{path.name}: provider {name} must be a mapping")
        if provider.get("type") != "http":
            fail(f"{path.name}: provider {name} must use http")
        if provider.get("behavior") not in ("domain", "ipcidr", "classical"):
            fail(f"{path.name}: provider {name} has unsupported behavior")
        if provider.get("format") != "mrs":
            fail(f"{path.name}: provider {name} must use mrs")
        if not str(provider.get("url", "")).startswith("https://"):
            fail(f"{path.name}: provider {name} must use HTTPS")

    rules = config.get("rules", [])
    if rules is None:
        rules = []
    if not isinstance(rules, list):
        fail(f"{path.name}: rules must be a list")
    if len(rules) != len(set(rules)):
        fail(f"{path.name}: duplicate rules")

    for rule in rules:
        if not isinstance(rule, str):
            fail(f"{path.name}: rule must be text")
        parts = rule.split(",")
        kind = parts[0].upper()
        if kind == "RULE-SET":
            if len(parts) < 3 or parts[1] not in providers:
                fail(f"{path.name}: unknown rule provider in {rule}")
            target = parts[2].upper()
        elif kind in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "GEOIP"}:
            if len(parts) < 3:
                fail(f"{path.name}: malformed rule {rule}")
            target = parts[2].upper()
        else:
            fail(f"{path.name}: unsupported rule type {kind}")
        if target not in BUILTIN_ACTIONS:
            fail(f"{path.name}: module rule target must be a built-in action: {target}")

    http = config.get("http", {})
    if http is None:
        http = {}
    if not isinstance(http, dict):
        fail(f"{path.name}: http must be a mapping")
    mitm = http.get("mitm", [])
    if not isinstance(mitm, list) or len(mitm) != len(set(mitm)):
        fail(f"{path.name}: http.mitm must be a unique list")
    rewrite = http.get("rewrite")
    body_rewrite = http.get("body-rewrite", [])
    if isinstance(rewrite, dict):
        body_rewrite = rewrite.get("body-rewrite", body_rewrite)
    if body_rewrite is None:
        body_rewrite = []
    if not isinstance(body_rewrite, list):
        fail(f"{path.name}: body-rewrite must be a list")
    if not rules and not body_rewrite:
        fail(f"{path.name}: module must contain rules or body-rewrite")
    for item in body_rewrite:
        if not isinstance(item, str) or len(item.split(None, 1)) < 2:
            fail(f"{path.name}: malformed body-rewrite entry")

    print(f"PASS: {path.name} ({len(rules)} rules, {len(mitm)} MITM hosts, {len(body_rewrite)} rewrites)")
