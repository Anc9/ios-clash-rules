# Clash iOS Rules

适用于 [ProjectClash/Clash-Client](https://github.com/ProjectClash/Clash-Client) 的个人分流规则方案。

> 当前版本 **v2.2.5（HTTPS 模块测试分支）**。这不是机场节点订阅，也不是一份包含节点的独立完整配置。

## 目标

- 使用机场订阅作为**节点来源**，让节点跟随原订阅更新
- 使用本仓库 YAML 作为**规则方案**，与节点来源分开维护
- 顶层保留 5 个策略组：`🚀 代理选择`、`🤖 AI 服务`、`🎬 流媒体`、`🛡 广告拦截`
- 地区节点通过 `include-all` 和名称正则分组，地区内使用 `url-test` 进行低延迟自动选择
- 国内直连、国外代理、AI 独立、流媒体独立、轻度广告拦截

## 规则文件

当前只保留一个规则方案文件，普通分流和 AI 自动兜底已经合并：

[rules/ClashRules.yaml](rules/ClashRules.yaml)

https://raw.githubusercontent.com/Anc9/ios-clash-rules/https-module/rules/ClashRules.yaml

AI 自动组按香港、新加坡、日本、台湾、英国的顺序回退，美国节点不参与 AI 自动兜底；美国节点仍保留在普通代理和流媒体策略组中。

## ProjectClash 使用方法

1. 「配置中心」→「节点库」：保留你的机场订阅并启用自动更新
2. 「配置中心」→「规则库」：添加/导入本仓库的 YAML 规则方案
3. 「配置中心」→「配置库」：编辑运行中的配置，保留机场作为节点来源
4. 在「规则方案」中选择导入的方案，而不是「原始（Original）」
5. 保存、重新启用配置后检查「代理」中的地区组和实际路由

不要直接删除仍被原配置引用的旧规则来源。先切换运行中的规则方案，再按需清理。

## 策略说明

- `🚀 代理选择`：香港 / 日本 / 新加坡 / 美国 / 台湾 / 其他地区 / 全球自动
- `✈️ Telegram`：Telegram 专用自动兜底，仅使用香港 / 日本 / 台湾自动组
- `🤖 AI 服务`：香港 / 日本 / 美国 / 新加坡自动，亦可跟随普通代理
- `🎬 流媒体`：Netflix、Disney+、YouTube 及综合媒体规则走香港 / 日本 / 新加坡 / 美国节点
- `🛡 广告拦截`：`REJECT` 开启，`DIRECT` 关闭
- 各地区自动组为 `url-test`，测速目标 `https://www.gstatic.com/generate_204`，每 600 秒检查、容差 80 ms
- `url-test` 衡量的是测速目标的响应延迟，**不是下载带宽、稳定性或 AI 地区解锁保证**

## 修改与验证

修改 `rules/ClashRules.yaml` 后，运行：

```bash
python -m pip install pyyaml
python scripts/validate.py
```

GitHub Actions 会自动运行同样的结构检查。它无法替代 iOS 真机验证或检查远程 MRS 文件是否下载成功。

变更建议：优先一次只改一类（地区分组、AI 分流、广告、DNS），记录变更及回归结果到 [`CHANGELOG.md`](CHANGELOG.md)。

## 安全

**不要提交**机场订阅 URL、节点密码、UUID、访问密钥、完整导出的含凭据 YAML。请将节点订阅与本规则仓库分离；敏感内容应先撤销或更换。

此仓库的规则集文件通过 URL 引用第三方维护的 MRS 数据，实际内容及更新由第三方维护。

## HTTPS 去广告模块

模块清单和聚合关系见 [`docs/MODULES.md`](docs/MODULES.md) 与 [`modules/manifest.yaml`](modules/manifest.yaml)。

支持一个聚合链接一次性导入全部模块：

[`modules/All-HTTPS-AdBlock.stoverride`](modules/All-HTTPS-AdBlock.stoverride)

`https://raw.githubusercontent.com/Anc9/ios-clash-rules/https-module/modules/All-HTTPS-AdBlock.stoverride`

修改 HTTPS 模块后，除了结构校验，还应运行：

```bash
python scripts/check_aggregate.py
python scripts/test_module_matchers.py
```

聚合模块包含去广告和全部 App Rewrite。使用聚合模块时不要再同时启用下面的独立模块；独立模块适合单独排查某个 App。

去广告规则合并为一个模块；单个 App 的 Rewrite 独立启用。

### 域名广告拦截

[`modules/Domestic-AdBlock.stoverride`](modules/Domestic-AdBlock.stoverride)

`https://raw.githubusercontent.com/Anc9/ios-clash-rules/https-module/modules/Domestic-AdBlock.stoverride`

负责远程广告 MRS 和普通广告域名拦截。

### 单个 App Rewrite

| 模块 | 作用 |
| --- | --- |
| [`Bilibili-AppRewrite.stoverride`](modules/Bilibili-AppRewrite.stoverride) | 哔哩哔哩开屏响应和 CDN |
| [`Weibo-AppRewrite.stoverride`](modules/Weibo-AppRewrite.stoverride) | 微博开屏、信息流广告和仅保留热搜的发现页 |
| [`Goofish-AppRewrite.stoverride`](modules/Goofish-AppRewrite.stoverride) | 闲鱼开屏 JSON |
| [`Taobao-AppRewrite.stoverride`](modules/Taobao-AppRewrite.stoverride) | 淘宝开屏和广告 JSON |
| [`QQNews-AppRewrite.stoverride`](modules/QQNews-AppRewrite.stoverride) | 腾讯新闻开屏 JSON |
| [`JD-AppRewrite.stoverride`](modules/JD-AppRewrite.stoverride) | 京东开屏 JSON |

每个 App Rewrite 模块只处理自己的域名和响应。当前已扩展哔哩哔哩动态/直播、闲鱼页面推荐、京东开屏、微博信息流广告过滤和发现页热搜保留。微博发现页会保留“微博热搜”，并移除榜单、同城、超话、常看的人、热门话题和热门视频模块。可以单独启用；需要 HTTPS 解密的条目要求证书状态为 Ready。遇到误杀时只关闭对应 App 模块，再根据 Activity 日志调整。

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
