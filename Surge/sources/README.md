# Financial domain evidence ledger

Use this directory to record evidence for newly researched financial-service rules. The existing rulesets predate this ledger and have not all been audited or backfilled.

Before adding a service or domain, record:

| Field | What to capture |
| --- | --- |
| Service | Official service or institution name |
| Country/region | Account jurisdiction the ruleset targets |
| Category | Bank, payment, brokerage, telecom/MVNO, or other risk-sensitive service |
| Official source | Service website, support page, official app listing, or regulator/institution directory |
| Evidence type/date | How the domain was verified and when |
| Candidate host and match | Exact hostname or owned suffix, with the narrowest suitable rule type |
| Ownership/scope | Whether the host is first-party or shared infrastructure and likely unrelated-traffic impact |
| Decision | Added, deferred, or rejected, with a short reason |

Use a public third-party ruleset only as a discovery lead. Do not treat copied entries or repository search hits as ownership evidence. For shared identity, CDN, analytics, anti-fraud, or cloud endpoints, include a service-specific source proving the dependency and document the expected routing impact before adding them.

Expand country coverage by region and service category (retail banks, digital banks, brokers, payment rails, and telecom/MVNOs). Use official institution/regulator directories to build the service checklist, then verify each service's own web/app surfaces. Record gaps as unverified rather than claiming exhaustive coverage.

Keep the evidence ledger limited to new research until existing rules can be audited; do not infer missing sources for legacy entries.
