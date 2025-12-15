# intl.AirTicket

A curated Surge ruleset collection for international travel, financial services, and risk-sensitive platforms.  
精心整理的 Surge 规则集合，适用于国际出行、金融服务和风控敏感平台。

---

## ✨ Features / 特性

- **Pure ruleset design / 纯规则设计**  
  Rules only define *what to match*, not *how to route*  
  规则仅定义“匹配哪些域名”，而不绑定具体策略。

- **Finance-friendly / 金融友好**  
  Optimized for crypto exchanges, PayPal, Amex, and other risk-sensitive services  
  优化覆盖数字货币交易所、PayPal、美运等高风控服务。

- **Minimal & maintainable / 精简易维护**  
  Prefer `DOMAIN-SUFFIX` over verbose subdomain rules  
  尽量使用 `DOMAIN-SUFFIX`，避免冗余子域规则。

- **Surge-first / Surge 优先**  
  Designed and tested specifically for Surge  
  专为 Surge 设计和测试，保证兼容性。

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

## 🧪 Tested Platforms (Non-Exhaustive) / 已测试平台（非详尽）

- Crypto exchanges (Kraken, Binance, Coinbase…)  
  数字货币交易所（Kraken、Binance、Coinbase…）
- PayPal (multi-region accounts) / 多地区 PayPal 账号
- American Express / 美运卡
- International travel & airline services / 国际出行及航空服务

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

## 📄 License / 许可证

MIT License
