# Create a Domain 3D Rebuild Skill

Turn a profession's drawing language and expert judgment into a reusable AI Agent Skill for precise, traceable 3D reconstruction.

把一个行业的图纸语言和专家判断，转化为用于精确、可追溯三维重构的可复用 AI Agent Skill。

## Contents / 目录

- [中文指南](#中文指南)
- [English guide](#english-guide)
- [Definition of done](#definition-of-done--完成标准)

## 中文指南

### 1. 先选择一个窄而可验收的领域

不要从“重建所有船舶”开始。先选择一个同行能够清楚判断对错的任务，例如“根据总布置图和典型剖面重建船体舱段的协调级语义模型”。

在写代码前回答六个问题：

| 问题 | 示例答案 |
| --- | --- |
| 重建对象是什么？ | 船体舱段、甲板、舱壁、加强构件和开口 |
| 接受哪些证据？ | 总布置图、剖面图、节点详图、材料表和检验照片 |
| 输出给谁使用？ | 设计协调、检修规划或数字孪生展示 |
| 怎样判断正确？ | 构件数量、拓扑、标高、间距和连接关系通过验证 |
| 哪些问题必须人工复核？ | 图纸版本冲突、遮挡连接和影响安全的材料不确定性 |
| 最高成熟度是什么？ | `concept` 或 `coordination`，除非另有授权规则 |

把真实项目缩小成一个合成或明确允许再分发的公开样例。不要为了展示能力而公开客户图纸、专有规范或可反向识别的几何。

### 2. 从模板创建领域包

在 GitHub 使用 **Use this template** 创建自己的仓库，然后运行：

```bash
python3 scripts/init_domain.py ship-structure \
  --title "Ship Structure" \
  --description "Reconstruct ship structural compartments from drawings and inspection evidence."
```

生成目录：

```text
domains/ship-structure/
  domain.json
  SKILL.md
  references/
    ontology.md
    rules.md
  scripts/
    validate_domain.py
```

不要直接修改 `domains/_template/`。模板是未来所有领域包共享的起点。

### 3. 填写领域契约 `domain.json`

把领域边界写成机器可读契约：

- `target_objects`：要重建的物理对象族；
- `source_types`：允许作为证据的图纸、表格、照片或扫描类型；
- `entity_types`：Agent 必须区分的构件、节点、装配体和接口；
- `relation_types`：连接、包含、支撑、接触等关系；
- `constraint_types`：尺寸、共线、连续、间距、对称或领域专用约束；
- `output_types`：语义模型、协调模型、审查报告或其他制品；
- `maturity_ceiling`：该公开领域包能够诚实支持的最高成熟度；
- `validators`：发布前必须运行的确定性检查。

领域包不是词汇列表。它必须说明对象怎样关联、什么结果不可能、哪些错误会阻止发布。

### 4. 编写领域 `SKILL.md`

领域 Skill 是给 AI Agent 的操作说明。Frontmatter 只保留 `name` 和 `description`，并在 description 中同时写明能力和触发场景：

```markdown
---
name: ship-structure-reconstruction
description: Reconstruct ship compartments from general arrangement drawings, sections, detail drawings, schedules, and inspection evidence as traceable 3D semantic and coordination models. Use for ship structure drawing interpretation, deck and bulkhead topology, opening reconciliation, structural member association, and review-gated model publication.
---
```

正文使用祈使式，至少规定：

1. 如何登记和读取证据；
2. 如何区分观察、解释和假设；
3. 如何建立领域实体、关系和坐标系；
4. 如何求解尺寸与拓扑约束；
5. 什么时候必须向专家提出有边界的问题；
6. 哪些验证失败会阻止输出；
7. 能发布什么成熟度，不能声称什么。

把详细本体和规则放入 `references/`，把重复、确定性的检查放入 `scripts/`。不要让 `SKILL.md` 变成一本无法按需加载的行业百科。

### 5. 把专家经验变成可检查资产

与领域专家一起建立四类资产：

- `ontology.md`：术语、实体、属性、关系和同义词；
- `rules.md`：验收规则、容差、冲突优先级和必须复核的歧义；
- `validate_domain.py`：可以确定性检查的数量、拓扑、尺寸和引用完整性；
- 合成评测样例：保留真实推理难度，但不包含受保护项目内容。

先逐字记录专家规则，再决定哪些规则适合代码化。不要把“专家通常这样判断”偷偷改写成“程序永远这样判断”。

### 6. 创建第一个评测项目

```bash
python3 scripts/init_project.py demo-compartment \
  --domain ship-structure \
  --title "Synthetic Ship Compartment"
```

按顺序填充：

```text
projects/demo-compartment/sources/index.json   证据登记表
projects/demo-compartment/workspace/ir.json   当前可追溯语义模型
projects/demo-compartment/reviews/             专家决策
projects/demo-compartment/outputs/             中间三维结果
```

每个实体和结论都应能够回到 source、observation、hypothesis 或 review。外观看起来正确不能替代证据链。

### 7. 验证 Agent，而不只验证模型

至少测试四类情况：

1. 证据完整且规则明确时，Agent 能完成重构；
2. 图纸冲突时，Agent 保留冲突并请求复核；
3. 缺少关键尺寸时，Agent 不编造 fabrication 级几何；
4. 上游决定改变时，相关输出被标记为 stale。

运行：

```bash
python3 scripts/validate_workspace.py --domain ship-structure
python3 scripts/validate_workspace.py --project demo-compartment
python3 scripts/self_test.py
```

### 8. 审查并发布衍生产品

领域专家解决发布阻塞项后，将项目状态改为 `reviewed`，再显式选择制品：

```bash
python3 scripts/publish_result.py demo-compartment \
  --artifact coordination-model.glb \
  --artifact review-report.json
```

发布清单会记录 Domain Pack、输入 IR 哈希、制品哈希、成熟度、模板来源和许可证。保留 `Built from the NeuBE-Structural-Rebuild template`、`LICENSE`、`NOTICE` 与 `built_from` 信息。

一个 Domain Pack 可以继续衍生成行业 Skill、评测集、CAD/BIM 插件、审查工作台或完整产品，但必须保持专业责任边界和数据授权清晰。

## English guide

### 1. Select a narrow, reviewable domain

Do not start with “reconstruct every ship.” Choose a task a peer can judge, such as reconstructing a coordination-grade semantic model of one ship compartment from a general arrangement drawing and representative sections.

Define the target objects, accepted evidence, intended user, acceptance rules, mandatory review conditions, and honest maturity ceiling. Reduce the first case to synthetic or explicitly redistributable evidence.

### 2. Initialize the Domain Pack

Create a repository with **Use this template**, then run:

```bash
python3 scripts/init_domain.py ship-structure \
  --title "Ship Structure" \
  --description "Reconstruct ship structural compartments from drawings and inspection evidence."
```

Keep active work out of `domains/_template/`. Define the domain contract in `domain.json`, including target objects, source types, entities, relations, constraints, outputs, maturity ceiling, and validators.

### 3. Write the domain Skill

Use `domains/ship-structure/SKILL.md` to tell the AI agent how to inventory evidence, separate observations from interpretations, build domain semantics, solve constraints, request bounded review, validate outputs, and report limitations. Put detailed ontology and rules in `references/`; put repeated deterministic checks in `scripts/`.

Make the frontmatter description specific enough to trigger on the profession's drawings, vocabulary, operations, and expected outputs. Keep the body imperative and operational.

### 4. Encode expert knowledge

Work with domain experts to create:

- an ontology of terms, entities, attributes, relationships, and synonyms;
- acceptance rules, tolerances, conflict priorities, and review boundaries;
- deterministic validators for topology, dimensions, counts, and references;
- synthetic evaluation cases that preserve reasoning difficulty without exposing protected work.

Record the expert statement before converting it into code. Do not turn a contextual heuristic into an unconditional rule silently.

### 5. Build an evaluation project

```bash
python3 scripts/init_project.py demo-compartment \
  --domain ship-structure \
  --title "Synthetic Ship Compartment"
```

Register sources, build the current IR, record expert decisions, and write generated files under `outputs/`. Every entity and conclusion should trace to a source, observation, hypothesis, or review.

### 6. Test the agent behavior

Test successful reconstruction, conflicting drawings, missing critical dimensions, and downstream invalidation after an upstream decision changes. The agent must preserve ambiguity and stop for review instead of inventing high-maturity geometry.

```bash
python3 scripts/validate_workspace.py --domain ship-structure
python3 scripts/validate_workspace.py --project demo-compartment
python3 scripts/self_test.py
```

### 7. Review and publish

After a domain expert resolves release blockers, mark the project `reviewed` and publish selected artifacts with `scripts/publish_result.py`. Preserve the generated manifest, hashes, maturity, template provenance, Apache-2.0 license, and NOTICE.

A Domain Pack can become an industry skill, benchmark, CAD/BIM integration, review workbench, or complete product. Keep expert responsibility, data rights, and output claims explicit as it grows.

## Definition of done / 完成标准

A first Domain 3D Rebuild Skill is ready when:

- [ ] the domain boundary and maturity ceiling are explicit;
- [ ] the Skill description contains concrete professional triggers;
- [ ] ontology, relations, constraints, and unsupported cases are documented;
- [ ] at least three expert rules are deterministic or review-gated;
- [ ] one synthetic or redistributable evaluation project exists;
- [ ] evidence, interpretations, and review decisions remain traceable;
- [ ] conflicting or missing evidence does not produce false certainty;
- [ ] domain, project, and lifecycle validation pass;
- [ ] a domain expert has reviewed the expected result;
- [ ] license, NOTICE, data rights, and template provenance are preserved.
