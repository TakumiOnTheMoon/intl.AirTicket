#!/usr/bin/env python3
"""Generate Shadowrocket and Mihomo/Clash Meta rule-provider files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validate_rulesets import EOF_MARKER, ROOT, RULES_DIR, validate


EXPORTS_DIR = ROOT / "exports"
SHADOWROCKET_DIR = EXPORTS_DIR / "Shadowrocket"
CLASH_DIR = EXPORTS_DIR / "Clash"


def active_rules(content: str) -> list[str]:
    return [
        line
        for line in content.splitlines()
        if line and not line.startswith("#") and line != "EOF"
    ]


def render_shadowrocket(
    source_path: Path,
    content: str,
    source_root: Path = ROOT,
) -> str:
    source = source_path.relative_to(source_root).as_posix()
    return f"# GENERATED FROM: {source}; edit the canonical source instead.\n{content}"


def render_clash_provider(
    source_path: Path,
    content: str,
    source_root: Path = ROOT,
) -> str:
    source = source_path.relative_to(source_root).as_posix()
    metadata = [
        line
        for line in content.splitlines()
        if line.startswith(("# NAME:", "# AUTHOR:", "# UPDATED:"))
    ]
    rules = active_rules(content)
    lines = [
        *metadata,
        f"# GENERATED FROM: {source}; edit the canonical source instead.",
        "payload:",
        *(f"  - {rule}" for rule in rules),
        EOF_MARKER,
    ]
    return "\n".join(lines) + "\n"


def expected_exports(
    source_dir: Path = RULES_DIR,
    output_dir: Path = EXPORTS_DIR,
) -> dict[Path, str]:
    expected: dict[Path, str] = {}
    source_root = source_dir.parent.parent
    for source_path in sorted(source_dir.glob("*.list")):
        content = source_path.read_text(encoding="utf-8")
        expected[output_dir / "Shadowrocket" / source_path.name] = render_shadowrocket(
            source_path, content, source_root
        )
        expected[output_dir / "Clash" / f"{source_path.stem}.yaml"] = render_clash_provider(
            source_path, content, source_root
        )
    return expected


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def check_exports(
    source_dir: Path = RULES_DIR,
    output_dir: Path = EXPORTS_DIR,
) -> list[str]:
    expected = expected_exports(source_dir, output_dir)
    errors = [
        f"missing or stale generated file: {display_path(path)}"
        for path, content in expected.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != content
    ]

    expected_paths = set(expected)
    for directory, suffix in (
        (output_dir / "Shadowrocket", ".list"),
        (output_dir / "Clash", ".yaml"),
    ):
        if directory.is_dir():
            errors.extend(
                f"unexpected generated file: {display_path(path)}"
                for path in sorted(directory.glob(f"*{suffix}"))
                if path not in expected_paths
            )
    return errors


def write_exports() -> int:
    errors, _, _, _ = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    expected = expected_exports()
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Generated {len(expected)} client rule files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if checked-in client exports do not match canonical rules",
    )
    arguments = parser.parse_args()

    if arguments.check:
        errors = check_exports()
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if errors:
            return 1
        print(f"Client exports are current ({len(expected_exports())} files).")
        return 0

    return write_exports()


if __name__ == "__main__":
    raise SystemExit(main())
