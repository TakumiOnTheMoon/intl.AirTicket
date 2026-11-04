#!/usr/bin/env python3
"""Validate the syntax and basic consistency of the repository's Surge rulesets."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "Surge" / "rules"
SUPPORTED_RULE_TYPES = {"DOMAIN", "DOMAIN-SUFFIX"}
DOMAIN_PATTERN = re.compile(
    r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z",
    re.IGNORECASE,
)
METADATA_KEYS = ("NAME", "AUTHOR", "UPDATED")
EOF_MARKER = "################## EOF ##################"


def validate() -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    overlaps: list[str] = []
    rules_by_domain: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    ruleset_paths = sorted(RULES_DIR.glob("*.list"))
    active_rule_count = 0

    if not ruleset_paths:
        return [f"No rulesets found in {RULES_DIR.relative_to(ROOT)}"], [], 0, 0

    for path in ruleset_paths:
        relative_path = path.relative_to(ROOT)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{relative_path}: not valid UTF-8 ({error})")
            continue

        if not content.endswith("\n"):
            errors.append(f"{relative_path}: missing final newline")

        lines = content.splitlines()
        for key in METADATA_KEYS:
            metadata = [
                (line_number, line.partition(":")[2].strip())
                for line_number, line in enumerate(lines, start=1)
                if line.startswith(f"# {key}:")
            ]
            if len(metadata) != 1 or not metadata[0][1]:
                errors.append(
                    f"{relative_path}: expected exactly one non-empty '# {key}:' header"
                )
            elif key == "UPDATED":
                line_number, value = metadata[0]
                try:
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                        raise ValueError
                    date.fromisoformat(value)
                except ValueError:
                    errors.append(
                        f"{relative_path}:{line_number}: UPDATED must use YYYY-MM-DD"
                    )

        metadata_positions = {
            key: [
                line_number
                for line_number, line in enumerate(lines, start=1)
                if line.startswith(f"# {key}:")
            ]
            for key in METADATA_KEYS
        }
        description_positions = [
            line_number
            for line_number, line in enumerate(lines, start=1)
            if line.startswith("# DESCRIPTION:")
        ]
        if all(len(metadata_positions[key]) == 1 for key in METADATA_KEYS):
            ordered_header = [metadata_positions[key][0] for key in METADATA_KEYS]
            description_is_out_of_order = bool(
                description_positions
                and description_positions[0] < ordered_header[-1]
            )
            if ordered_header != sorted(ordered_header) or description_is_out_of_order:
                errors.append(
                    f"{relative_path}: metadata order must be NAME, AUTHOR, UPDATED, "
                    "then optional DESCRIPTION"
                )

        footer_lines = [
            (line_number, line)
            for line_number, line in enumerate(lines, start=1)
            if "EOF" in line
        ]
        if footer_lines != [(len(lines), EOF_MARKER)]:
            errors.append(
                f"{relative_path}: expected one '{EOF_MARKER}' footer on the final line"
            )

        for line_number, line in enumerate(lines, start=1):
            if not line or line.startswith("#") or line == "EOF":
                continue
            active_rule_count += 1
            if line != line.strip():
                errors.append(f"{relative_path}:{line_number}: leading/trailing whitespace")

            fields = line.split(",")
            rule_type = fields[0]
            if rule_type not in SUPPORTED_RULE_TYPES:
                errors.append(
                    f"{relative_path}:{line_number}: unsupported or policy-bearing "
                    f"rule type {rule_type!r}"
                )
                continue
            if len(fields) != 2 or not fields[1]:
                errors.append(
                    f"{relative_path}:{line_number}: {rule_type} requires exactly one domain"
                )
                continue

            domain = fields[1]
            if not DOMAIN_PATTERN.fullmatch(domain):
                errors.append(
                    f"{relative_path}:{line_number}: invalid domain value {domain!r}"
                )
                continue

            key = domain.lower()
            rules_by_domain[key].append((relative_path.as_posix(), line_number, rule_type))

    for domain, entries in sorted(rules_by_domain.items()):
        rule_types = {entry[2] for entry in entries}
        if len(entries) > 1 and len(rule_types) == 1:
            locations = ", ".join(f"{path}:{line}" for path, line, _ in entries)
            errors.append(f"duplicate domain {domain!r}: {locations}")

    suffixes = sorted(rules_by_domain)
    for domain in suffixes:
        for parent in suffixes:
            if domain == parent:
                child_entries = [
                    entry for entry in rules_by_domain[domain] if entry[2] == "DOMAIN"
                ]
                parent_entries = [
                    entry
                    for entry in rules_by_domain[parent]
                    if entry[2] == "DOMAIN-SUFFIX"
                ]
            elif domain.endswith(f".{parent}"):
                child_entries = rules_by_domain[domain]
                parent_entries = [
                    entry
                    for entry in rules_by_domain[parent]
                    if entry[2] == "DOMAIN-SUFFIX"
                ]
            else:
                continue
            if child_entries and parent_entries:
                child_entry = child_entries[0]
                parent_entry = parent_entries[0]
                overlaps.append(
                    f"{child_entry[0]}:{child_entry[1]} ({domain}) is covered by "
                    f"{parent_entry[0]}:{parent_entry[1]} ({parent})"
                )

    return errors, overlaps, len(ruleset_paths), active_rule_count


def main() -> int:
    errors, overlaps, ruleset_count, rule_count = validate()

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for overlap in overlaps:
        print(f"REVIEW: possible suffix overlap: {overlap}")

    if errors:
        print(f"Validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        f"Validated {ruleset_count} rulesets and {rule_count} rules "
        f"with no syntax errors or duplicate domains."
    )
    if overlaps:
        print(
            f"Found {len(overlaps)} parent/child suffix overlap(s); "
            "review them for intentional scope."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
