# HTTPS 模块维护规则

## 模块归属

`modules/manifest.yaml` 是模块清单，记录模块版本、状态、聚合关系和冲突组。现有模块路径保持不变，避免影响已经导入的 Raw 地址。

## 聚合模块

`All-HTTPS-AdBlock.stoverride` 是一次性导入入口。它包含公共去广告规则和已经验证过的 App Rewrite。

启用聚合模块后，不要再启用同一冲突组里的独立模块。独立模块用于单独排查和回归测试。

当前携程和知乎规则仍然是聚合模块内的 inline 规则，等实机验证稳定后再拆成独立模块。Apple WeatherKit 保持独立，不加入广告聚合模块。

## 修改流程

1. 先修改对应的独立 App 模块；如果功能还没有独立模块，暂时只修改聚合模块并在 `manifest.yaml` 的 `inline` 中登记。
2. 更新模块自己的 `version` 和 `date`。
3. 运行结构校验、聚合覆盖检查和 URL 回归测试。
4. 在 iOS 真机上验证 Activity 日志和正常功能。
5. 实机确认后再更新聚合模块和 `manifest.yaml`。

## 已知限制

- URL 正则测试只能确认请求路径能命中，不能代替 ProjectClash 的实际 MITM 和响应改写测试。
- `DIRECT` 不等于绕过 iOS 的 VPN/TUN 环境检测。
- WeatherKit 在 iOS 27.3 开发版上的问题属于上游兼容性问题，模块标记为 `experimental`。
