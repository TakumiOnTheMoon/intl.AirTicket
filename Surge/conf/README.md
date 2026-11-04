# Surge configuration writing standard

This standard applies to tracked Surge configuration examples such as [`Ticket.conf`](./Ticket.conf). It does not authorize editing a user's live Surge profile.

## File layout

- Keep reusable profile examples in `Surge/conf/` and canonical policy-free domain lists in `Surge/rules/`.
- Preserve the existing section order used by the example profile unless a documented Surge requirement calls for a change:
  `[General]`, `[Proxy]`, `[Proxy Group]`, `[Rule]`, followed by optional sections such as `[Host]`, `[URL Rewrite]`, `[Script]`, `[MITM]`.
- Use one section header per line, exactly as supported by Surge. Do not duplicate a section to append items; add them to the existing section.
- Keep each setting, proxy, group, or rule on its own line. Use blank lines between logical groups and short comments to explain non-obvious intent.

## Formatting and references

- Preserve the key spelling and syntax used by the relevant Surge feature. Before introducing or changing syntax, consult the official [Surge LLM documentation index](https://nssurge.com/llms.txt) and the specific current feature documentation.
- In `[General]`, write `key = value`. Keep comma-separated values on one line unless Surge's current documentation specifies otherwise.
- In `[Proxy]` and `[Proxy Group]`, use Surge's documented delimiters and quote names that contain spaces or punctuation as required. Keep referenced policy names consistent across sections.
- In `[Rule]`, use one complete Surge rule per line; preserve argument order, quoting, and supported rule options. Keep referenced rulesets policy-free and bind routing policy only in the configuration.
- Keep remote rule URLs explicit and stable. When adding, renaming, or deleting a local ruleset, update every config and documentation reference in the same change.
- Do not reformat or reorder unrelated profile sections just for visual consistency. Make minimal, local edits.

## Secrets and local values

- Commit only sanitized examples. Use clearly fake placeholders for nodes, local paths, IPs, subscription URLs, tokens, credentials, certificate paths, and passphrases.
- Never copy values from a personal profile into `Ticket.conf`, docs, tests, generated output, or command output.
- Do not place a real credential in comments; comments are still committed content.
- A local profile may override placeholders privately, but do not add automatic symlinks, synchronization, deployment, or reload behavior to this repository.

## Validation and review

- Review changed lines for valid section placement, delimiter/quoting consistency, unresolved local ruleset references, and accidental policy or secret inclusion.
- Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate_rulesets.py`, and `python3 scripts/export_rulesets.py --check` when relevant.
- If Surge is available, import only a sanitized isolated test profile. Never use a production profile for smoke testing without explicit authorization.
- Static checks do not prove that the profile imports or routes traffic correctly. State when Surge/client import testing was unavailable.
