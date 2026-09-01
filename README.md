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

Surge/  
├─ rules/  
│  ├─ Fin_Tel_CA.list          # Base finance & telecom rules / 基础金融及电信规则  
│  ├─ Fin_Flex_Finance.list    # Flexible finance services (crypto, PayPal, Amex) / 弹性金融规则  
│  └─ ...                      # Other categorized rulesets / 其他分类规则  

> Each ruleset is **self-contained** and intended to be referenced from Surge main configuration.  
> 每个规则文件独立，可在 Surge 主配置中直接引用。

---

## 🚀 Usage / 使用方法

### 1️⃣ Reference ruleset in Surge / 在 Surge 中引用规则

[Rule]  
RULE-SET,Fin_Flex_Finance,FIN-FLEX

### 2️⃣ Define flexible policy group / 定义策略组

[Proxy Group]  
FIN-FLEX = select, US-FIN, HK-FIN, SG-FIN, DIRECT

- Switch routing **only at the policy level / 只在策略层切换**  
- Ruleset files do **not** need to be modified when changing regions / 切换地区时无需修改规则文件

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
- Group rules by **service type**, not by region / 按服务类型分组，而非地区  
- Commit messages follow **Conventional Commits** where possible / 提交信息尽量遵循规范格式  

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
