# Clash iOS Rules

适用于 [ProjectClash/Clash-Client](https://github.com/ProjectClash/Clash-Client) 的个人分流规则方案。

> 当前版本 **v1.3（待 iOS 实机完整验证）**。这不是机场节点订阅，也不是一份包含节点的独立完整配置。

## 目标

- 使用机场订阅作为**节点来源**，让节点跟随原订阅更新
- 使用本仓库 YAML 作为**规则方案**，与节点来源分开维护
- 顶层只保留 3 个策略组：`🚀 代理选择`、`🤖 AI 服务`、`🛡 广告拦截`
- 地区节点通过 `include-all` 和名称正则分组，地区内使用 `url-test` 进行低延迟自动选择
- 国内直连、国外代理、AI 独立、轻度广告拦截

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
- `🤖 AI 服务`：日本 / 美国 / 新加坡自动，亦可跟随普通代理
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

## License

MIT License，详见 [`LICENSE`](LICENSE)。
