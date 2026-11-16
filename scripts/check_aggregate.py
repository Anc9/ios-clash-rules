#!/usr/bin/env python3
"""Check that the aggregate module contains all declared source modules."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "modules" / "manifest.yaml"


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


def as_list(config, key):
    value = config.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        fail(f"{key} must be a list")
    return value


manifest = load(MANIFEST)
module_entries = manifest.get("modules")
if not isinstance(module_entries, list) or not module_entries:
    fail("manifest.modules must be a non-empty list")

entry_by_path = {}
entry_ids = set()
for entry in module_entries:
    if not isinstance(entry, dict):
        fail("each manifest module entry must be a mapping")
    module_id = str(entry.get("id", "")).strip()
    relative = str(entry.get("path", "")).strip()
    if not module_id or not relative:
        fail("each manifest module needs id and path")
    if module_id in entry_ids:
        fail(f"duplicate module id: {module_id}")
    if relative in entry_by_path:
        fail(f"duplicate module path: {relative}")
    if entry.get("status") not in {"stable", "experimental", "deprecated"}:
        fail(f"{relative}: unsupported module status")
    if not (ROOT / relative).is_file():
        fail(f"manifest module path does not exist: {relative}")
    entry_ids.add(module_id)
    entry_by_path[relative] = entry

aggregate_meta = manifest.get("aggregate")
if not isinstance(aggregate_meta, dict):
    fail("manifest.aggregate must be a mapping")

aggregate_path = ROOT / aggregate_meta.get("path", "")
if not aggregate_path.is_file():
    fail("aggregate.path does not exist")
aggregate = load(aggregate_path)

declared_version = str(aggregate_meta.get("version", "")).strip()
actual_version = str(aggregate.get("version", "")).strip()
if declared_version != actual_version:
    fail(f"aggregate version mismatch: manifest={declared_version}, file={actual_version}")

included = aggregate_meta.get("includes", [])
if not isinstance(included, list) or not included:
    fail("aggregate.includes must be a non-empty list")
included_set = set(included)
if len(included_set) != len(included):
    fail("aggregate.includes contains duplicate paths")
for relative in included:
    entry = entry_by_path.get(relative)
    if entry is None:
        fail(f"aggregate source missing from manifest.modules: {relative}")
    if entry.get("aggregate") is not True:
        fail(f"aggregate source is not marked aggregate: {relative}")
for relative, entry in entry_by_path.items():
    if entry.get("aggregate") is True and relative not in included_set:
        fail(f"module marked aggregate but absent from aggregate.includes: {relative}")

aggregate_rules = set(as_list(aggregate, "rules"))
aggregate_http = aggregate.get("http") or {}
if not isinstance(aggregate_http, dict):
    fail("aggregate.http must be a mapping")

for key in ("mitm", "rewrite", "url-rewrite", "body-rewrite"):
    if not isinstance(aggregate_http.get(key, []) or [], list):
        fail(f"aggregate.http.{key} must be a list")

for relative in included:
    source_path = ROOT / relative
    if not source_path.is_file():
        fail(f"declared source does not exist: {relative}")
    source = load(source_path)

    providers = source.get("rule-providers") or {}
    aggregate_providers = aggregate.get("rule-providers") or {}
    for name, provider in providers.items():
        if name not in aggregate_providers:
            fail(f"{relative}: missing rule-provider in aggregate: {name}")
        if aggregate_providers[name] != provider:
            fail(f"{relative}: rule-provider differs in aggregate: {name}")

    for rule in as_list(source, "rules"):
        if rule not in aggregate_rules:
            fail(f"{relative}: missing rule in aggregate: {rule}")

    source_http = source.get("http") or {}
    if not isinstance(source_http, dict):
        fail(f"{relative}: http must be a mapping")
    for key in ("mitm", "rewrite", "url-rewrite", "body-rewrite"):
        aggregate_items = set(aggregate_http.get(key, []) or [])
        for item in as_list(source_http, key):
            if item not in aggregate_items:
                fail(f"{relative}: missing http.{key} item in aggregate: {item}")

print(f"PASS: aggregate covers {len(included)} declared source modules")
