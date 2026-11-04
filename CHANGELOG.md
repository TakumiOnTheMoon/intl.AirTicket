# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]
### Added
- Added a dependency-free ruleset validator and GitHub Actions check for syntax, metadata, and duplicate domains.
### Changed
- Standardized ruleset author/date metadata and EOF markers; removed 16 same-file subdomain rules already covered by parent suffixes and removed policy advice from the P2P ruleset comment.
- Documented the full ruleset inventory, repository layout, and AI-agent maintenance guidance.
- Added official Surge documentation references and safeguards against live-profile edits or policy-bearing rules.
- Ignored macOS Finder metadata files.
- Sanitized `Ticket.conf` into a reusable template with local-only node and subscription placeholders.
- Added encrypted DNS defaults, a flexible policy group, and references for the finance-flexible and Apple Intelligence rulesets.
- Removed personal-network matching and an overly broad high-port download rule to reduce accidental routing.
- Consolidated multi-region financial services in `Fin_Flex.list` and expanded the template's manual flexible policy group to include CA, UK, and DE exits.
- Removed broad third-party analytics/API domains and redundant country-list entries from finance rulesets.
- Replaced broad BT/P2P keyword matching with explicit tracker and DHT domains, and narrowed Apple matching to owned or exact relay hostnames.
### Fixed
### Removed

## [0.1.0] - 2026-02-02
### Added
- Initial public release of Surge ruleset collection for international travel, finance, and risk-sensitive platforms.
- Pure ruleset philosophy: rules define match only, no policy binding.
- Baseline rulesets: `Fin_Flex_Finance`, `Fin_Tel_CA`.
- Documentation: minimal working configuration and maintenance guidelines.
