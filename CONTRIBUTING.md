# Contributing / 参与共创

NeuBE-Structural-Rebuild connects domain experts with modeling, AI, and software contributors. You can contribute professional judgment without writing code.

NeuBE-Structural-Rebuild 连接行业专家与建模、AI 和软件贡献者。即使不写代码，你也可以贡献关键的专业判断。

## Three ways to contribute / 三种参与方式

### Domain expert / 行业专家

Explain how practitioners read drawings, name entities, resolve conflicts, recognize impossible results, and decide when human review is mandatory. A useful proposal can be a glossary, annotated synthetic drawing, decision table, or review checklist.

说明从业者如何阅读图纸、命名对象、解决冲突、识别不可能的结果，以及何时必须人工复核。术语表、合成图纸标注、判断表或审查清单都可以成为有效贡献。

### Domain builder / 领域构建者

Translate expert knowledge into ontology, rules, validators, fixtures, and a reusable Skill under `domains/<domain>/`. Preserve the expert's terms and responsibility boundary instead of silently replacing them with implementation assumptions.

把专家知识转化为 `domains/<domain>/` 下的本体、规则、验证器、测试样例和可复用 Skill。保留专家术语和责任边界，不要用实现假设悄悄替换专业判断。

### Tool and evaluation contributor / 工具与评测贡献者

Build parsers, solvers, CAD/BIM adapters, viewers, review interfaces, or synthetic evaluation cases. Make failures inspectable and keep generated geometry traceable to evidence and decisions.

构建解析器、求解器、CAD/BIM 适配器、查看器、审查界面或合成评测案例。让失败可以被检查，并让生成几何始终能够追溯到证据和决策。

## Minimum viable Domain Pack / 最小可用领域包

Follow the bilingual [Create a Domain 3D Rebuild Skill guide](references/create-domain-3d-rebuild-skill.md) for the complete domain-to-release workflow.

完整的领域定义、Skill 编写、评测与发布流程，请参考双语[《创建 Domain 3D Rebuild Skill》指南](references/create-domain-3d-rebuild-skill.md)。

A first contribution does not need to solve an entire industry. Start with one narrow, testable slice:

1. one sanitized, synthetic, or redistributable representative drawing;
2. a glossary of symbols, entities, attributes, and relationships;
3. at least three acceptance or rejection rules;
4. one ambiguity that must stop for expert review;
5. one expected 3D or semantic result a peer can evaluate;
6. a declared maturity ceiling and responsibility boundary.

第一次贡献不需要解决整个行业。请从一个边界清楚、可以测试的小问题开始：一份可公开的代表性图纸、一套术语和关系、至少三条验收或否决规则、一个必须由专家复核的歧义、一个同行可以评价的预期结果，以及明确的成熟度上限和责任边界。

Open a [Domain Pack Proposal](https://github.com/ConcentricCirclesMRTT/NeuBE-Structural-Rebuild/issues/new?template=domain-pack-proposal.yml) before implementing a new field. The proposal is designed for domain experts and does not require code.

实现新领域前，请先创建 [Domain Pack Proposal](https://github.com/ConcentricCirclesMRTT/NeuBE-Structural-Rebuild/issues/new?template=domain-pack-proposal.yml)。该提案面向行业专家，不要求提交代码。

## Safety and submission requirements / 安全与提交要求

1. Do not submit confidential drawings, scans, geometry, catalogs, standards, or derived project identifiers.
2. Record the source and redistribution basis for every non-original asset.
3. Keep observations separate from interpretations and retain stable evidence references.
4. Keep Chinese and English user-facing documentation aligned.
5. Run `python3 scripts/validate_workspace.py` and `python3 scripts/self_test.py` before opening a pull request.
6. Preserve `LICENSE`, `NOTICE`, and `built_from` provenance. State significant modifications in the pull request.

请勿提交保密图纸、扫描、几何、目录、标准或可识别项目的信息；记录所有非原创资产的来源与再分发依据；保持观察与解释分离；同步维护中英文说明；提交前运行验证和自测试；保留 `LICENSE`、`NOTICE` 与 `built_from` 来源信息。

By submitting a contribution, you agree that it may be distributed under the repository's Apache-2.0 license.

提交贡献即表示你同意该贡献可以按照本仓库的 Apache-2.0 许可证发布。
