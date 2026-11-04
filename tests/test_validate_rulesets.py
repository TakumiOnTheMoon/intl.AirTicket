import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_rulesets  # noqa: E402
import export_rulesets  # noqa: E402


EOF_MARKER = "################## EOF ##################"
HEADER = (
    "# NAME: Test Ruleset\n"
    "# AUTHOR: Test Author\n"
    "# UPDATED: 2026-11-04\n"
)


class RulesetValidatorTests(unittest.TestCase):
    def validate_content(self, content: str) -> tuple[list[str], list[str], int, int]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            rules_dir = root / "Surge" / "rules"
            rules_dir.mkdir(parents=True)
            (rules_dir / "test.list").write_text(content, encoding="utf-8")
            with (
                patch.object(validate_rulesets, "ROOT", root),
                patch.object(validate_rulesets, "RULES_DIR", rules_dir),
            ):
                return validate_rulesets.validate()

    def test_accepts_valid_domain_rules(self) -> None:
        errors, overlaps, ruleset_count, rule_count = self.validate_content(
            HEADER + "\nDOMAIN,login.example.com\nDOMAIN-SUFFIX,example.org\n\n" + EOF_MARKER + "\n"
        )

        self.assertEqual(errors, [])
        self.assertEqual(overlaps, [])
        self.assertEqual(ruleset_count, 1)
        self.assertEqual(rule_count, 2)

    def test_rejects_policy_fields_and_unsupported_rule_types(self) -> None:
        errors, _, _, _ = self.validate_content(
            HEADER
            + "\nDOMAIN-SUFFIX,example.com,PROXY\n"
            + "DOMAIN-KEYWORD,example\n"
            + EOF_MARKER
            + "\n"
        )

        self.assertTrue(any("requires exactly one domain" in error for error in errors))
        self.assertTrue(any("unsupported or policy-bearing" in error for error in errors))

    def test_rejects_case_insensitive_duplicate_domains(self) -> None:
        errors, _, _, _ = self.validate_content(
            HEADER
            + "\nDOMAIN-SUFFIX,Example.com\n"
            + "DOMAIN-SUFFIX,example.COM\n"
            + EOF_MARKER
            + "\n"
        )

        self.assertTrue(any("duplicate domain 'example.com'" in error for error in errors))

    def test_reports_exact_domain_covered_by_matching_suffix(self) -> None:
        errors, overlaps, _, _ = self.validate_content(
            HEADER
            + "\nDOMAIN-SUFFIX,bunq.com\n"
            + "DOMAIN,bunq.com\n"
            + EOF_MARKER
            + "\n"
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(overlaps), 1)

    def test_reports_parent_suffix_coverage_for_review(self) -> None:
        errors, overlaps, _, _ = self.validate_content(
            HEADER
            + "\nDOMAIN-SUFFIX,example.com\n"
            + "DOMAIN,login.example.com\n"
            + EOF_MARKER
            + "\n"
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(overlaps), 1)

    def test_rejects_invalid_metadata_order_and_footer(self) -> None:
        content = (
            "# AUTHOR: Test Author\n"
            "# NAME: Test Ruleset\n"
            "# UPDATED: 2026-11-04\n"
            "DOMAIN-SUFFIX,example.com\n"
            "################## EOF ##################\n"
        )
        content = content.replace(EOF_MARKER, "# EOF")

        errors, _, _, _ = self.validate_content(content)

        self.assertTrue(any("metadata order" in error for error in errors))
        self.assertTrue(any("expected one" in error and "footer" in error for error in errors))


class RulesetExportTests(unittest.TestCase):
    def test_clash_provider_keeps_policy_out_of_payload(self) -> None:
        source = ROOT / "Surge" / "rules" / "sample.list"
        content = HEADER + "\nDOMAIN-SUFFIX,example.com\n" + EOF_MARKER + "\n"

        output = export_rulesets.render_clash_provider(source, content)

        self.assertIn("payload:\n  - DOMAIN-SUFFIX,example.com\n", output)
        self.assertNotIn(",DIRECT", output)
        self.assertNotIn(",PROXY", output)

    def test_shadowrocket_export_preserves_canonical_rule_lines(self) -> None:
        source = ROOT / "Surge" / "rules" / "sample.list"
        content = HEADER + "\nDOMAIN,login.example.com\n" + EOF_MARKER + "\n"

        output = export_rulesets.render_shadowrocket(source, content)

        self.assertIn("DOMAIN,login.example.com\n", output)
        self.assertIn("GENERATED FROM: Surge/rules/sample.list", output)

    def test_export_check_detects_missing_or_stale_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_dir = root / "Surge" / "rules"
            source_dir.mkdir(parents=True)
            source_path = source_dir / "sample.list"
            source_path.write_text(
                HEADER + "\nDOMAIN-SUFFIX,example.com\n" + EOF_MARKER + "\n",
                encoding="utf-8",
            )
            output_dir = root / "exports"
            expected = export_rulesets.expected_exports(source_dir, output_dir)

            self.assertEqual(len(expected), 2)
            self.assertTrue(export_rulesets.check_exports(source_dir, output_dir))
            for path, content in expected.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            self.assertEqual(export_rulesets.check_exports(source_dir, output_dir), [])
            next(iter(expected)).write_text("stale\n", encoding="utf-8")
            self.assertTrue(export_rulesets.check_exports(source_dir, output_dir))


if __name__ == "__main__":
    unittest.main()
