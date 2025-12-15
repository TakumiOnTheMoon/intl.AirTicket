# intl.AirTicket

A curated Surge ruleset collection for international travel, financial services, and risk-sensitive platforms.

This repository focuses on **clean, minimal, and maintainable rulesets**, designed for users who:

* manage **multiple regions / accounts**
* use **financial services, crypto exchanges, and travel platforms**
* need **stable routing with flexible policy switching**

---

## ✨ Features

* **Pure ruleset design**

  * Rules only define *what to match*, not *how to route*
* **Finance-friendly**

  * Optimized for crypto exchanges, PayPal, Amex, and other risk-sensitive services
* **Minimal & maintainable**

  * Prefer `DOMAIN-SUFFIX` over verbose subdomain rules
* **Surge-first**

  * Designed and tested specifically for Surge

---

## 📁 Repository Structure

```
Surge/
├─ rules/
│  ├─ Fin_Tel_CA.list          # Base finance & telecom rules
│  ├─ Fin_Flex_Finance.list   # Flexible finance services (crypto, PayPal, Amex)
│  └─ ...                     # Other categorized rulesets
```

> Each ruleset is **self-contained** and intended to be referenced from Surge main configuration.

---

## 🚀 Usage

### 1️⃣ Reference ruleset in Surge

```ini
[Rule]
RULE-SET,Fin_Flex_Finance,FIN-FLEX
```

### 2️⃣ Define flexible policy group

```ini
[Proxy Group]
FIN-FLEX = select, US-FIN, HK-FIN, SG-FIN, DIRECT
```

* Switch routing **only at the policy level**
* Ruleset files do **not** need to be modified when changing regions

---

## 🧠 Design Philosophy

### Why minimal rules?

* Redundant subdomain rules increase maintenance cost
* `DOMAIN-SUFFIX` provides sufficient coverage for most platforms
* Only **cross-domain CDN or risk services** are listed separately when required

> If a service works reliably with a single `DOMAIN-SUFFIX`, it should stay that way.

---

## 🔐 Notes on Financial & Risk-Sensitive Services

* Avoid automatic policy switching (`url-test`, `fallback`)
* Keep **Web + App traffic on the same exit IP**
* Change regions **manually**, not dynamically
* Prefer long-lived, stable nodes over cheap shared IPs

These practices significantly reduce:

* frequent CAPTCHA
* account reviews
* silent request failures

---

## 🧪 Tested Platforms (Non-Exhaustive)

* Crypto exchanges (e.g. Kraken, Binance, Coinbase)
* PayPal (multi-region accounts)
* American Express
* International travel & airline services

---

## 🛠 Maintenance Guidelines

* Rulesets should remain **pure** (no policy binding)
* Group rules by **service type**, not by region
* Commit messages follow **Conventional Commits** where possible

Example:

```
refactor(surge): simplify finance ruleset to minimal domain-suffix coverage
```

---

## 📌 Disclaimer

This repository is provided for **personal and educational use** only.

Routing behavior, account risk, and compliance are ultimately the responsibility of the user.
No guarantee is made regarding account safety or service availability.

---

## 📄 License

MIT License
