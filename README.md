## 策略说明

- `🚀 代理选择`：香港 / 日本 / 新加坡 / 美国 / 台湾 / 其他地区 / 全球自动
- `✈️ Telegram`：Telegram 专用手动选择，仅提供香港 / 日本 / 台湾自动组
- `🍎 Apple`：默认选 `🍎 Apple 自动`，优先直连；Apple 测试地址连接失败时依次回退香港、日本、美国自动节点。也可手动选直连、美国、香港或通用代理
- `🤖 AI 服务`：香港 / 新加坡 / 日本 / 台湾 / 英国自动，亦可跟随普通代理
- `🎬 流媒体`：Netflix、Disney+、YouTube 及综合媒体规则走香港 / 日本 / 新加坡 / 美国节点
- `🛡 广告拦截`：`REJECT` 开启，`DIRECT` 关闭
- 各地区自动组为 `url-test`，测速目标 `https://www.gstatic.com/generate_204`，每 600 秒检查、容差 80 ms
- `url-test` 衡量的是测速目标的响应延迟，**不是下载带宽、稳定性或 AI 地区解锁保证**
- Apple 组覆盖 `cm-apple-cn` 规则集及 `apple.com`、`apple.com.cn`、`icloud.com`、`itunes.com`、`mzstatic.com`、`cdn-apple.com`；自动组每 300 秒检测 `https://apps.apple.com/` 的连通性，超时后按直连、香港、日本、美国的顺序回退。它无法判断某款美区 App 是否可下载；直连可用但需要美区出口时，手动选 `🇺🇸 美国自动`。切换后需重新发起 App Store 下载。应用可用地区仍受 Apple 账号的国家或地区限制。

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

聚合模块包含去广告和全部 App Rewrite，并试验性处理米家 `home.mi.com` 的两个开屏 `openingBanner` 接口。使用聚合模块时不要再同时启用下面的独立模块；独立模块适合单独排查某个 App。

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
| [`Xiaohongshu-AppRewrite.stoverride`](modules/Xiaohongshu-AppRewrite.stoverride) | 小红书信息流广告响应 |

每个 App Rewrite 模块只处理自己的域名和响应。当前已扩展哔哩哔哩动态/直播、闲鱼页面推荐、京东开屏、微博信息流广告过滤和发现页热搜保留，以及小红书发现页信息流广告过滤。微博发现页会保留“微博热搜”，并移除榜单、同城、超话、常看的人、热门话题和热门视频模块。可以单独启用；需要 HTTPS 解密的条目要求证书状态为 Ready。遇到误杀时只关闭对应 App 模块，再根据 Activity 日志调整。

## 规则集来源
