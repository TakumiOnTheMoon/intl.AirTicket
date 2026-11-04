# Agent Guide: intl.AirTicket

## Project purpose

`intl.AirTicket` is a curated collection of **pure Surge rulesets** for international travel, financial, payment, brokerage, telecom, identity-sensitive, and risk-control-sensitive services.

The main task is to collect and maintain service domains that may require a stable country or region exit IP. Rulesets match traffic only; routing policy remains in the consumer's Surge configuration.

## Non-negotiable ruleset principles

- Keep rulesets policy-free. Do not add proxy groups, `select`, `url-test`, `fallback`, `load-balance`, `FINAL`, or policy names to files under `Surge/rules/`.
- Prefer `DOMAIN-SUFFIX` for a service's primary, owned domain.
- Use a more specific rule type only when a suffix would create a documented false positive, or when a shared CDN, API, identity, or anti-fraud endpoint is required.
- Do not add broad third-party infrastructure domains (for example, generic cloud, CDN, analytics, CAPTCHA, or identity providers) without showing that the specific service requires it and assessing its impact on unrelated traffic.
- Keep rules grouped by country/region and service category, following the surrounding file's headings and comment style.
- Keep files UTF-8, one Surge rule per non-comment line, and retain the `EOF` footer when the target file uses one.
- Update the file header's `UPDATED` date whenever its rules change.

## Research and coverage standard

Before adding, removing, or changing a domain:

1. Identify the owning service, its target country/region, and its category (bank, payment, brokerage, telecom/MVNO, travel, or other risk-sensitive service).
2. Prefer primary evidence: the service's official website, official app links, official support documentation, or observed first-party network hostnames. Treat search snippets, user lists, and unauthenticated third-party lists as leads, not proof.
3. Check whether the base domain or an equivalent suffix is already covered in the target list or another applicable list. Avoid redundant subdomains and duplicate rules.
4. Consider completeness: include essential first-party web, app API, login/identity, verification, and transaction domains when evidence supports them. Do not claim exhaustive coverage unless it has been verified against official service surfaces.
5. Consider false positives: confirm that a proposed suffix is actually controlled by the service and is not shared by unrelated businesses.
6. For a removal, document why the domain is obsolete, duplicated, misclassified, or too broad.

## Repository and data boundaries

- Treat this file as the source of truth for repository-specific agent behavior. Read it before changing rules, configuration examples, or maintenance automation.
- Keep personal Surge profiles and credentials outside the repository. Do not inspect external profiles unless the user explicitly authorizes it; when authorized, use them only for the requested check and never print, copy, commit, or otherwise expose their contents. Never make an external profile a default edit target.
- Do not add local machine files, credentials, subscription URLs, or user-specific routing policy to the repository.
- Preserve the existing `Surge/rules/` paths unless a migration includes updates to all references and is explicitly justified; consumers may depend on these paths.

## Surge documentation and live-profile safety

- Before changing Surge syntax in rules or configuration examples, consult the official LLM documentation index at <https://nssurge.com/llms.txt> and follow its relevant current documentation. The index is a reference, not a substitute for the specific feature documentation.
- If the official documentation cannot be reached, say so and avoid asserting unverified or remembered syntax as current. Continue only with changes whose syntax is already established in the repository or clearly mark validation as incomplete.
- Keep this repository focused on reusable, policy-free rulesets and the sanitized `Surge/conf/Ticket.conf` example. Do not add scripts, live-profile automation, or proxy/policy behavior as part of routine rules maintenance.
- Never create or alter symlinks to Surge's live profile directory, reload/import a production profile, or automatically deploy/roll back changes. Use static checks and, when available, validate an isolated test configuration. Ask for explicit authorization before any live-profile operation.
- Do not modify real proxy endpoints, IP addresses, passwords, tokens, subscription URLs, DNS, gateway, or MITM settings. If a separate task explicitly requires editing a local profile, keep the change narrowly scoped, preserve unrelated settings, and do not expose secret values in output or version control.
- A request to force `DIRECT`, bind a proxy policy, or define a strategy group is outside the pure-ruleset contract. Do not encode it in `Surge/rules/`; clarify the scope or handle it separately in a sanitized example only when explicitly requested.
- Keep scripts within `scripts/` limited to repository maintenance and validation unless the project scope is explicitly expanded. Any Surge scripting feature must be based on the official documentation and must not be silently mounted into a profile.

## Required validation for every ruleset change

Run and record the relevant checks before committing:

1. **Format and syntax** — inspect changed lines; every active rule must use a Surge-supported rule type and have the expected comma-separated fields. Ensure there are no blank domain values, malformed comments, or accidental policy bindings.
2. **Duplicate and overlap review** — check exact duplicates within the changed file and across `Surge/rules/`. Review parent/child suffix overlaps and retain only intentional ones.
3. **Scope review** — verify country and service-category placement, and evaluate likely routing impact and possible false positives.
4. **Configuration reference review** — when adding, renaming, moving, or deleting a ruleset, check `Surge/conf/Ticket.conf`, README examples, and any relevant documentation for references that must be updated.
5. **Surge import smoke test** — when Surge is available, import or reload the affected ruleset in a test configuration and verify it parses without errors. If Surge is unavailable, state that the smoke test was not run and perform the static checks above.
6. **Behavior check when feasible** — test representative official web/app endpoints through the intended policy and verify that expected traffic matches the rule. Do not log in, transact, or bypass security controls unless explicitly authorized.

Run the repository's static validator with `python3 scripts/validate_rulesets.py`. It checks UTF-8, metadata, dates, domain-rule syntax, policy-free format, exact duplicates, and reports parent/child suffix overlaps for manual review. Keep its supported rule types synchronized with any intentional format expansion.

## Documentation and change log

- Update `README.md` when the public ruleset inventory, usage guidance, philosophy, or maintenance workflow changes.
- Update `CHANGELOG.md` under `Unreleased` for user-visible additions, removals, or behavior-impacting corrections.
- Keep entries concise, specific, and factual; name the ruleset and service/country affected.

## Git workflow

- Inspect `git status` before editing. Preserve unrelated user changes and never add incidental files such as `.DS_Store`.
- Each completed logical change must be committed promptly. Do not combine unrelated countries, services, refactors, or documentation work in one commit.
- Stage only files belonging to the change, review the staged diff, run the required validation, then commit.
- Use Conventional Commits in imperative, specific English. Preferred scopes are `rules`, `surge`, `docs`, and `chore`.

Examples:

```text
feat(rules): add Hong Kong Standard Chartered domains
fix(rules): correct Canada telecom suffix coverage
refactor(rules): remove redundant US banking subdomains
docs: document ruleset validation workflow
chore: update ruleset maintenance metadata
```

- Include a concise commit body when the reason, evidence source, routing impact, or validation limitation is not obvious from the subject.
- Do not amend, force-push, reset, or rewrite existing history unless explicitly instructed.

## Completion checklist

Before declaring a change complete, confirm:

- The rule remains pure and uses the least broad safe match.
- The domain is evidence-backed, correctly categorized, and not redundant.
- Static validation, scope review, and any available Surge smoke/behavior tests have passed or their limitations are stated.
- Required README and CHANGELOG updates are included.
- Only intended files are staged.
- A focused Conventional Commit has been created.
