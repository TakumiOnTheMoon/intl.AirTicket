# intl.AirTicket

🌍 **Surge ruleset collection for international travel, finance, and risk-sensitive platforms**  
✈️ 面向国际出行 / 金融 / 风控敏感平台的 Surge 规则集合集

---

## 📌 What is this? | 这是什么？

**intl.AirTicket** is a curated collection of **pure Surge rulesets** designed for:

- International travel services  
- Financial & payment platforms  
- Telecom / identity-sensitive services  
- Platforms with **strict anti-fraud and risk-control systems**

**intl.AirTicket** 是一套**只包含规则、不包含策略**的 Surge ruleset 集合，适用于：

- 国际航旅 / 出行平台  
- 金融、支付、加密资产相关服务  
- 电信、身份敏感类平台  
- **风控严格、容易触发验证/封号的平台**

> ⚠️ This project provides **rulesets only**  
> It never binds policies, never defines proxy groups, and never forces routing decisions.

> ⚠️ 本项目**只提供规则集**  
> 不绑定策略、不定义代理组、不干涉你的路由选择。

---

## 🎯 Design Philosophy | 设计理念

### 1️⃣ Ruleset ≠ Policy（规则 ≠ 策略）
- Rulesets **only define matching conditions**
- No `select`, no `url-test`, no policy binding
- All routing logic stays in your Surge configuration

规则集**只负责“匹配”**，不负责：
- 选节点
- 切策略
- 自动测速或切换

---

### 2️⃣ Prefer coarse granularity（优先使用粗粒度规则）
- `DOMAIN-SUFFIX` first
- Avoid `DOMAIN-KEYWORD` unless strictly necessary
- Fine-grained rules are used **only when**:
  - A CDN / risk-control domain is shared across platforms
  - `DOMAIN-SUFFIX` would cause obvious false positives

优先使用：
- `DOMAIN-SUFFIX`

仅在以下情况才拆细：
- 跨平台共用的 CDN / 风控域名
- 使用后缀会产生明显误伤

---

### 3️⃣ Stability over automation (for finance)  
### 金融场景：稳定优先于自动化

For financial and risk-sensitive platforms, this project **strongly recommends**:

- ❌ Avoid `url-test`, `fallback`, `load-balance`
- ✅ Use **manual `select`**
- ✅ Keep **Web & App traffic on the same exit IP**
- ✅ Prefer long-lived, low-churn nodes

对于金融 / 风控平台，强烈建议：
- ❌ 不使用自动测速 / 自动切换
- ✅ 手动选择出口
- ✅ 网页端 & App 端保持同一出口
- ✅ 使用稳定、长期不变的节点

---

## 📁 Repository Structure / 仓库结构

```text
.
├── .github/workflows/validate-rules.yml  # Ruleset CI
├── scripts/
│   ├── validate_rulesets.py             # Canonical rules validation
│   └── export_rulesets.py               # Generated client formats
├── Surge/
│   ├── conf/Ticket.conf                  # Reusable example profile
│   ├── conf/README.md                    # Configuration writing standard
│   ├── rules/                            # Policy-free canonical rulesets
│   └── sources/README.md                 # Evidence requirements for new finance domains
├── exports/
│   ├── Shadowrocket/                     # Generated policy-free .list files
│   └── Clash/                            # Generated Mihomo/Clash Meta YAML providers
├── tests/                                # Validator and exporter regression tests
├── AGENTS.md                             # Repository-specific AI agent guidance
├── CHANGELOG.md
└── README.md
```

The rules are grouped by region and category. Existing filenames are stable because consumer profiles may reference them.

| Ruleset | Scope |
| --- | --- |
| `AppleIntelligence.list` | Apple Intelligence, Siri, APNs push, and relay domains |
| `AppleLocations.list` | Apple location and mapping services |
| `DevTools.list` | Developer tools and package registries |
| `Fin_Flex.list` | Multi-region financial services |
| `Fin_Tel_CA.list` | Canada finance and telecom |
| `Fin_Tel_DE.list` | Germany finance and telecom |
| `Fin_Tel_HK.list` | Hong Kong finance and telecom |
| `Fin_Tel_UK.list` | United Kingdom finance and telecom |
| `Fin_Tel_US.list` | United States finance and telecom |

Each ruleset is **self-contained** and intended to be referenced from a Surge profile. It matches traffic only; routing policy remains in the consumer's configuration.

---

## 📱 Other clients / 其他客户端

`Surge/rules/` remains the canonical, policy-free domain source. Following the per-client publishing pattern used by [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule), run `python3 scripts/export_rulesets.py` to generate Shadowrocket `.list` files and Mihomo/Clash Meta YAML rule providers under `exports/`; CI checks that generated output stays synchronized.

The generated files contain matching rules only. Assign the desired policy in each client's own profile. For Clash Meta/Mihomo, configure a `classical` rule provider with `format: yaml`, then reference it using that profile's policy:

```yaml
rule-providers:
  intl-us-finance:
    type: http
    behavior: classical
    format: yaml
    path: ./rules/intl-us-finance.yaml
    url: https://raw.githubusercontent.com/TakumiOnTheMoon/intl.AirTicket/main/exports/Clash/Fin_Tel_US.yaml
    interval: 86400
rules:
  - RULE-SET,intl-us-finance,US-FIN
```

In Shadowrocket, import the generated list as a `RULE-SET` and assign its policy in the Shadowrocket profile. App-level import testing has not been run in this repository; treat the exports as format targets until verified in the specific client/version you use. Legacy Clash variants may require a different provider format.

For finance-domain expansion, add the source and ownership assessment to [`Surge/sources/README.md`](./Surge/sources/README.md). Existing rule entries have not all been backfilled into an evidence ledger.

---

## 🚀 Usage / 使用方法

### 1️⃣ Reference ruleset in Surge / 在 Surge 中引用规则

[Rule]  
RULE-SET,Fin_Flex,FIN-FLEX

### 2️⃣ Define flexible policy group / 定义策略组

[Proxy Group]  
FIN-FLEX = select, US-FIN, HK-FIN, SG-FIN, DIRECT

- Switch routing **only at the policy level / 只在策略层切换**  
- Ruleset files do **not** need to be modified when changing regions / 切换地区时无需修改规则文件

For services with accounts in more than one country—such as American Express, Wise, Revolut, BMO, or Scotiabank—keep the service in `Fin_Flex.list` and manually select the exit country that matches the account currently in use. A domain rule cannot safely infer account jurisdiction from the browser session.

### Configuration template / 配置模板

`Surge/conf/Ticket.conf` is a reusable example profile. It deliberately contains only commented personal-node placeholders and an example subscription URL. Replace those values only in a local, untracked profile; never commit proxy credentials, subscription URLs, local IP addresses, Host mappings, MITM certificates, or CA passphrases.

---

## 🧠 Design Philosophy / 设计理念

### Why minimal rules / 为什么要精简规则

- Redundant subdomain rules increase maintenance cost  
  冗余子域规则增加维护成本
- `DOMAIN-SUFFIX` provides sufficient coverage for most platforms  
  `DOMAIN-SUFFIX` 已覆盖绝大部分业务域名
- Only **cross-domain CDN or risk services** are listed separately when required  
  只有跨域 CDN 或风控服务才单独列出

> If a service works reliably with a single `DOMAIN-SUFFIX`, it should stay that way.  
> 如果某个服务使用单条 `DOMAIN-SUFFIX` 就可以稳定访问，就无需拆子域。

---

## 🔐 Notes on Financial & Risk-Sensitive Services / 金融及风控服务注意事项

- Avoid automatic policy switching (`url-test`, `fallback`)  
  避免自动切换策略（url-test、fallback）
- Keep **Web + App traffic on the same exit IP**  
  Web 与 App 流量使用同一出口 IP
- Change regions **manually**, not dynamically / 手动切换地区，不要动态切换
- Prefer long-lived, stable nodes over cheap shared IPs / 优先使用长期稳定节点，避免廉价共享 IP

These practices significantly reduce:  
遵循这些规则可以显著降低：  
- frequent CAPTCHA / 验证码频繁  
- account reviews / 账户风控审查  
- silent request failures / 请求静默失败

---

## 🛠 Maintenance Guidelines / 维护规范

- Rulesets should remain **pure** (no policy binding) / 保持规则文件纯粹（不绑定策略）  
- Group rules by region and service category / 按地区和服务类别组织规则
- Commit messages follow **Conventional Commits** where possible / 提交信息尽量遵循规范格式  

Before submitting a ruleset change, run the dependency-free static check:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_rulesets.py
python3 scripts/export_rulesets.py --check
```

Both checks are also run by GitHub Actions for changes to rulesets, tests, or the validator. The validator rejects malformed metadata, unsupported rule types, invalid domains, policy-bearing lines, and duplicate domains. Parent/child suffix overlaps are reported for manual review because some may be intentional. It is not a substitute for checking official service evidence or testing a ruleset in Surge.

The current `.list` files remain the canonical, policy-free domain data. Other clients can be supported with generated adapters (for example, provider/YAML exports), but each client format must be verified independently; do not maintain copied lists by hand or embed routing policies in the canonical files.

Repository-specific instructions for AI agents and contributors are maintained in [`AGENTS.md`](./AGENTS.md). Tracked Surge configuration conventions are documented in [`Surge/conf/README.md`](./Surge/conf/README.md).
For Surge syntax, agents should consult the official [LLM documentation index](https://nssurge.com/llms.txt) and the specific current documentation it references. Live profile syncing, symlink creation, and automatic reload/deployment are intentionally outside this repository's maintenance workflow.

Example / 示例:

refactor(surge): simplify finance ruleset to minimal domain-suffix coverage

---

## 📌 Disclaimer / 免责声明

This repository is provided for **personal and educational use** only.  
本仓库仅用于个人学习与研究使用。

Routing behavior, account risk, and compliance are ultimately the responsibility of the user.  
路由行为、账户风控与合规责任由用户自行承担。  

No guarantee is made regarding account safety or service availability.  
不保证账户安全或服务可用性。

---

## License / 许可证

Licensed under the Apache License, Version 2.0 (Apache-2.0).
See `LICENSE` for details.
