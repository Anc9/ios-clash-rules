## v2.2.4 — 2026-11-16

- 将普通分流与 AI 自动兜底合并为单一 ClashRules.yaml
- AI 自动兜底移除美国节点
- 修复校验脚本对 AND 规则的解析
- 保留 HTTPS 模块与聚合模块

# 变更记录

## HTTPS module 1.0.12 — 2026-11-18

- 什么值得买：新增 `app-api.smzdm.com` MITM，并精确拒绝 `/util/loading` 开屏响应。
- 聚合清单、匹配测试和 README 已同步更新，待真机验证后再决定是否拆分独立模块。

## HTTPS module 1.0.11 — 2026-11-17

- 米家开屏：在聚合模块中针对 `home.mi.com` 的两个 `openingBanner` 接口返回空字典；现有 `sdkconfig.ad.xiaomi.com` 拦截保持不变。
- 路径参考 [fmz200 米家模块](https://github.com/fmz200/wool_scripts/blob/main/Surge/module/split/partM/Mijia.sgmodule)，待 ProjectClash 真机验证。

## v2.2.10 — 2026-11-17

- Apple 自动组改为直连优先，失败时依次回退香港、日本、美国自动节点。
- 手动美区出口仍可在 Apple 组选择美国自动节点。

## v2.2.9 — 2026-11-17

- Apple 组默认使用隐藏的自动回退组：直连优先，连通性检测失败后使用美国自动节点。
- 保留 Apple 组手动选择美国、香港和通用代理；测速不判断 App Store 区域许可。

## v2.2.8 — 2026-11-17

- 新增 `🍎 Apple` 手动选择组，默认直连，可切换美国、香港自动节点或通用代理。
- Apple 相关域名与 `cm-apple-cn` 规则集统一进入该组，便于按需下载美区 App。


## HTTPS module 0.9 — 2026-11-17

- 新增小红书独立 Rewrite 模块，过滤发现页信息流中的推广项。
- 同步加入 HTTPS 聚合模块；小红书模块标记为 experimental，便于实机验证。


## v2.2.7 — 2026-11-16

- 增加 `msmp.abchina.com.cn` 子域名的 `REJECT` 拦截规则。