# Contributing

NeuBE-Structural-Rebuild is a base repository for traceable, domain-specific 3D reconstruction. Contributions should improve the reusable core or add sanitized domain knowledge without mixing in customer data.

## Contribution paths

- Improve the generic evidence-to-model workflow, schemas, validators, or publishing tools.
- Add a reusable domain pack under `domains/<domain>/` with its own ontology, rules, Skill, and validator.
- Add a fully synthetic or explicitly redistributable example.
- Improve bilingual documentation while keeping the Chinese and English sections aligned.

## Requirements

1. Do not submit confidential drawings, scans, geometry, catalogs, standards, or derived project identifiers.
2. Record the source and redistribution basis for every non-original asset.
3. Keep observations separate from interpretations and retain stable evidence references.
4. Run `python3 scripts/validate_workspace.py` and `python3 scripts/self_test.py` before opening a pull request.
5. Preserve `LICENSE` and `NOTICE`. State significant modifications in the pull request.

By submitting a contribution, you agree that it may be distributed under the repository's Apache-2.0 license.

## 参与贡献

NeuBE-Structural-Rebuild 是一个用于可追溯、领域化三维重构的基础仓库。贡献应改进通用核心或增加已脱敏的领域知识，不应混入客户数据。

可以改进通用工作流、Schema、验证器和发布工具，也可以在 `domains/<domain>/` 中增加领域包，或提交完全合成、明确允许再分发的案例。提交前请确保：不包含保密图纸、扫描、几何、目录或项目标识；记录非原创资产的来源与授权；保持观察和解释分离；运行仓库验证与自测试；保留 `LICENSE` 和 `NOTICE`。
