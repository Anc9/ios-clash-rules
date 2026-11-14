# Clash iOS Rules

适用于 [ProjectClash/Clash-Client](https://github.com/ProjectClash/Clash-Client) 的个人分流规则方案。

> 当前版本 **v2.2.2（待 iOS 实机完整验证）**。这不是机场节点订阅，也不是一份包含节点的独立完整配置。

## 目标

- 使用机场订阅作为**节点来源**，让节点跟随原订阅更新
- 使用本仓库 YAML 作为**规则方案**，与节点来源分开维护
- 顶层只保留 4 个策略组：`🚀 代理选择`、`🤖 AI 服务`、`🎬 流媒体`、`🛡 广告拦截`
- 地区节点通过 `include-all` 和名称正则分组，地区内使用 `url-test` 进行低延迟自动选择
- 国内直连、国外代理、AI 独立、流媒体独立、轻度广告拦截

## 规则文件

[`rules/ClashRules.yaml`](rules/ClashRules.yaml)

本仓库为 Public，可使用固定 Raw URL：

`https://raw.githubusercontent.com/Anc9/ios-clash-rules/main/rules/ClashRules.yaml`

**注意：** Raw URL 仅包含无凭据的规则方案；不要把 GitHub 访问令牌或机场订阅密钥写进 YAML。

## ProjectClash 使用方法

1. 「配置中心」→「节点库」：保留你的机场订阅并启用自动更新
2. 「配置中心」→「规则库」：添加/导入本仓库的 YAML 规则方案
3. 「配置中心」→「配置库」：编辑运行中的配置，保留机场作为节点来源
4. 在「规则方案」中选择导入的方案，而不是「原始（Original）」
5. 保存、重新启用配置后检查「代理」中的地区组和实际路由

不要直接删除仍被原配置引用的旧规则来源。先切换运行中的规则方案，再按需清理。

## 策略说明

- `🚀 代理选择`：香港 / 日本 / 新加坡 / 美国 / 台湾 / 其他地区 / 全球自动
- `🤖 AI 服务`：使用 `🤖 AI 自动` 兜底，在日本 / 新加坡 / 美国 / 台湾 / 英国节点间自动切换；亦可手动选择
- `🎬 流媒体`：Netflix、Disney+、YouTube 及综合媒体规则走香港 / 日本 / 新加坡 / 美国节点
- `🛡 广告拦截`：`REJECT` 开启，`DIRECT` 关闭
- 各地区自动组为 `url-test`，测速目标 `https://www.gstatic.com/generate_204`，每 600 秒检查、容差 80 ms
- OpenAI 相关域名（认证、上传、静态资源和 WebSocket）统一进入 `🤖 AI 服务`
- AI 兜底检测地址为 `https://chatgpt.com/`，不使用香港节点
- `url-test` 衡量的是测速目标的响应延迟，**不是下载带宽、稳定性或 AI 地区解锁保证**

## 修改与验证

修改 `rules/ClashRules.yaml` 后，运行：

```bash
python -m pip install pyyaml
python scripts/validate.py
```

GitHub Actions 会自动运行同样的结构检查。它无法替代 iOS 真机验证或检查远程 MRS 文件是否下载成功。

规则方案只保留 `proxy-groups`、`rule-providers`、`rules` 和 `sub-rules`，不要加入 `proxies`、`proxy-providers`、`dns` 或其他完整配置字段。

变更建议：优先一次只改一类（地区分组、AI 分流、广告、DNS），记录变更及回归结果到 [`CHANGELOG.md`](CHANGELOG.md)。

## 安全

**不要提交**机场订阅 URL、节点密码、UUID、访问密钥、完整导出的含凭据 YAML。请将节点订阅与本规则仓库分离；敏感内容应先撤销或更换。

此仓库的规则集文件通过 URL 引用第三方维护的 MRS 数据，实际内容及更新由第三方维护。

## HTTPS 去广告模块

模块与分流规则分开维护，但同在本仓库：

[`modules/Domestic-AdBlock.stoverride`](modules/Domestic-AdBlock.stoverride)

Raw 导入地址：

`https://raw.githubusercontent.com/Anc9/ios-clash-rules/main/modules/Domestic-AdBlock.stoverride`

当前模块针对 QQ/腾讯广告接口、淘宝/闲鱼、京东、高德、美团、中国联通、哔哩哔哩等常见广告域名，并对闲鱼、淘宝、腾讯新闻的少量开屏接口做精确拒绝。模块包含一个每天检查一次的远程广告规则集，并补充 B 站开屏响应字段清理和开屏素材 CDN 路径的精确拦截；不加载远程脚本、不包含 VIP 解锁，也不修改正常业务响应。固定的精确广告规则仍保留在模块中。

在 Clash 的「Modules」中添加后，按官方流程安装并信任证书，再打开 HTTPS Decryption。普通域名拦截可直接生效；需要接口级拒绝的条目要求证书状态为 Ready。广告接口会随 App 版本变化，遇到漏网或误杀时应先在 Modules 中关闭模块，再根据 Activity 日志逐项调整。

## 规则集来源

本仓库的路由结构和策略组由本仓库维护；远程 MRS 规则集来自 [DustinWin/ruleset_geodata](https://github.com/DustinWin/ruleset_geodata)，使用其 [mihomo-ruleset 发布文件](https://github.com/DustinWin/ruleset_geodata/releases/tag/mihomo-ruleset)。

当前引用的规则集：

| 文件 | 用途 |
| --- | --- |
| `private.mrs` / `privateip.mrs` | 私有网络域名与 IP |
| `apple-cn.mrs` / `microsoft-cn.mrs` | 苹果中国、微软中国 |
| `ai.mrs` / `ads.mrs` | AI 服务、广告域名 |
| `netflix.mrs` / `disney.mrs` / `youtube.mrs` / `media.mrs` | 流媒体域名 |
| `netflixip.mrs` / `mediaip.mrs` | 流媒体 IP |
| `proxy.mrs` / `cn.mrs` | 国外域名、国内域名 |
| `telegramip.mrs` / `cnip.mrs` | Telegram IP、国内 IP |

规则文件中的每个规则集设置为每 24 小时检查一次。第三方规则集的具体内容和更新节奏由其上游项目决定，本仓库只负责引用和组合，不复制维护这些 MRS 文件。

## License

MIT License，详见 [`LICENSE`](LICENSE)。
