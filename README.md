# NeuBE-Structural-Rebuild

**Neural Building Engine Structural Rebuild**

[中文](#中文说明) | [English](#english)

## 中文说明

NeuBE-Structural-Rebuild 是一个可复用的模板，用于构建从异构证据中重构物理结构的领域型 AI Skill。

它不是一个已经理解所有工程领域的万能模型。它提供一套通用工作流、数据边界、验证门禁和复核状态，帮助开发者把新的专业领域可靠地教给 AI Agent。

### 核心思想

许多重构系统直接把图纸、照片或扫描数据转换成三维模型。这样的结果可能看起来合理，却隐藏着构件身份不确定、尺寸冲突、连接缺失或下游几何已经失效等问题。

本模板保留一条可审计的工作链：

```text
来源 Sources
  -> 观察 Observations
  -> 假设 Hypotheses
  -> 领域语义模型 Domain Semantic Model
  -> 确定性约束 Deterministic Constraints
  -> 人工复核 Human Review
  -> 版本化输出 Versioned Outputs
```

AI 负责提出有边界的解释候选；领域工具负责求解和验证确定性事实；人类专家负责那些具有工程责任的歧义决策。

### 领域型 Skill 的通用模板

本仓库将可复用行为与领域知识分开：

| 通用核心 | 领域扩展 |
| --- | --- |
| 证据来源和稳定 ID | 领域来源类型与提取规范 |
| 观察与解释分离 | 领域实体、属性和关系 |
| 假设与复核状态 | 领域歧义类型与复核问题 |
| 约束记录与残差 | 领域求解器、容差和工程规则 |
| 发布门禁与失效传播 | 领域成熟度标准和输出适配器 |
| 公开安全边界 | 经授权的标准、目录和项目策略 |

适合使用该模板的领域，应当能够由专业人员明确回答：

1. 什么可以作为证据；
2. 领域中存在哪些物理或概念实体；
3. 哪些约束和规则可以被程序验证；
4. 哪些未决问题必须阻止发布；
5. 不同输出成熟度分别意味着什么。

同一模式可以用于建筑框架、桥梁、桁架、设备支撑、工业装配体，也可以迁移到具有类似“证据到决策”流程的非结构专业领域。

### 角钢塔重构：验证案例

角钢塔重构是该模板的一个领域特例，而不是模板本身的定义。

它适合作为验证案例，因为其中同时存在：

- 密集的多视图工程图纸；
- 投影重合但可能代表不同物理实体的构件；
- 结构拓扑、共享节点和复杂连接；
- 方向、对称、尺寸与几何约束；
- 必须由专家处理的高后果歧义；
- 上游判断改变后必须失效的 CAD 与制造制品。

在角钢塔 Skill 中，通用语义实体会被专业化为构件、节点、结构面、连接组件、孔和紧固件；通用约束会被专业化为结构面关联、构件方向、长度闭合、孔型、连接叠层和制造检查。这些专业规则应当属于独立的领域包，因此不会出现在本公开通用模板中。

三者关系如下：

```text
领域 Skill 通用模板
  -> 结构重构模板
      -> 角钢塔重构 Skill
```

角钢塔案例用于证明：该模板能够组织真实的领域推理、确定性程序、专家决定和可追溯输出。它并不意味着一个通用提示词可以在没有专业化的情况下解决所有领域。

### 创建新的领域版本

1. Fork 或复制本仓库。
2. 保留 `SKILL.md` 中从证据到输出的六层契约。
3. 在 `references/` 中定义领域本体和来源规范。
4. 使用领域实体和类型化关系扩展公开 IR Schema。
5. 在 `scripts/` 中添加确定性解析器、求解器和验证器。
6. 添加可公开的合成案例，同时覆盖通过和阻塞状态。
7. 定义成熟度等级、复核权限、不支持范围和发布阻塞条件。
8. 在作出能力声明前，使用代表性任务对 Skill 进行前向测试。

不要把保密案例或私有规则目录复制到公开领域包。公开案例应当是完全合成或明确获得再分发授权的数据，并在保留推理难度的同时，避免让受保护的真实项目能够被反向恢复。

### 仓库内容

- [`SKILL.md`](SKILL.md)：Agent 工作流和行为契约；
- [`assets/public-ir.schema.json`](assets/public-ir.schema.json)：通用公开 IR Schema；
- [`assets/public-ir-template.json`](assets/public-ir-template.json)：空白项目模板；
- [`assets/synthetic-frame-example.json`](assets/synthetic-frame-example.json)：合成的跨来源框架案例；
- [`references/domain-profiles.md`](references/domain-profiles.md)：结构领域起始配置；
- [`references/reconstruction-method.md`](references/reconstruction-method.md)：关联、拓扑、求解和变更控制方法；
- [`references/public-safety-boundary.md`](references/public-safety-boundary.md)：公开发布和工程安全边界；
- [`scripts/validate_public_ir.py`](scripts/validate_public_ir.py)：零第三方依赖的公开 IR 验证器。

### 验证示例

```bash
python3 scripts/validate_public_ir.py assets/synthetic-frame-example.json
```

预期结果：

```text
OK: assets/synthetic-frame-example.json is a valid public structure reconstruction IR
```

### 能力边界

本公开仓库支持概念级和协调级重构。几何一致不代表结构承载能力、安全性、规范符合性、详图完整性或制造就绪。用于重要工程决策时，必须引入经授权的领域规则、独立验证以及具备相应资质的工程复核。

---

## English

NeuBE-Structural-Rebuild is a reusable template for building domain-specific AI skills that reconstruct physical structures from heterogeneous evidence.

It is not a universal model that already understands every engineering domain. It provides the common workflow, data boundaries, validation gates, and review states needed to teach an AI agent a new reconstruction domain safely.

## The core idea

Many reconstruction systems jump directly from a drawing, image, or scan to a 3D model. That result may look plausible while hiding uncertain identities, conflicting dimensions, missing connections, or stale downstream geometry.

This template preserves an auditable chain:

```text
Sources
  -> Observations
  -> Hypotheses
  -> Domain Semantic Model
  -> Deterministic Constraints
  -> Human Review
  -> Versioned Outputs
```

The AI proposes bounded interpretations. Domain tools solve and validate deterministic facts. Human experts decide the ambiguities that carry engineering responsibility.

## A template for domain skills

The repository separates reusable behavior from domain knowledge.

| Reusable core | Domain-specific extension |
| --- | --- |
| Evidence provenance and stable IDs | Domain source types and extraction conventions |
| Observation versus interpretation | Domain entities, attributes, and relationships |
| Hypothesis and review states | Domain ambiguity patterns and review questions |
| Constraint records and residuals | Domain solvers, tolerances, and engineering rules |
| Release gates and stale propagation | Domain maturity criteria and output adapters |
| Public safety boundary | Authorized standards, catalogs, and project policy |

A suitable domain is one where practitioners can define:

1. what counts as evidence;
2. which physical or conceptual entities exist;
3. which constraints and rules can be tested;
4. which unresolved decisions must block release;
5. what output maturity means.

The same pattern can support building frames, bridges, trusses, equipment supports, industrial assemblies, or non-structural professional domains with an equivalent evidence-to-decision workflow.

## Angle-tower reconstruction as a proof case

Angle-tower reconstruction is one domain-specific instance of this template, not the definition of the template itself.

It is a useful validation case because it combines:

- dense multi-view engineering drawings;
- projected members that can represent different physical instances;
- structural topology and shared connections;
- orientation, symmetry, dimension, and geometry constraints;
- high-consequence ambiguity that should require expert review;
- downstream CAD and manufacturing artifacts that must become stale after upstream changes.

In an angle-tower skill, the generic semantic entities become members, nodes, structural faces, connection assemblies, holes, and fasteners. Generic constraints become face incidence, member orientation, length closure, hole pattern, connection stack, and fabrication checks. Those specialized rules belong in the domain package; they are intentionally absent from this public generic template.

This relationship is:

```text
Domain Skill Template
  -> Structure Reconstruction Template
      -> Angle-Tower Reconstruction Skill
```

The angle-tower case demonstrates that the template can organize real domain reasoning, deterministic programs, review decisions, and traceable outputs. It does not imply that one generic prompt can solve every domain without specialization.

## Create a domain-specific version

1. Fork or copy this repository.
2. Keep the six-layer evidence-to-output contract in `SKILL.md`.
3. Define the domain ontology and source conventions in `references/`.
4. Extend the public IR schema with domain entities and typed relationships.
5. Add deterministic parsers, solvers, and validators under `scripts/`.
6. Add synthetic or redistributable fixtures that contain both passing and blocked cases.
7. Define maturity levels, review authority, unsupported cases, and release blockers.
8. Forward-test the skill on representative tasks before making capability claims.

Do not copy confidential examples or private rule catalogs into a public specialization. A public example should be synthetic or explicitly redistributable and should preserve the reasoning challenge without allowing a protected project to be reconstructed.

## Repository contents

- [`SKILL.md`](SKILL.md): agent workflow and behavioral contract;
- [`assets/public-ir.schema.json`](assets/public-ir.schema.json): public generic IR schema;
- [`assets/public-ir-template.json`](assets/public-ir-template.json): empty project template;
- [`assets/synthetic-frame-example.json`](assets/synthetic-frame-example.json): synthetic cross-source example;
- [`references/domain-profiles.md`](references/domain-profiles.md): starter structural profiles;
- [`references/reconstruction-method.md`](references/reconstruction-method.md): association, topology, solving, and change-control method;
- [`references/public-safety-boundary.md`](references/public-safety-boundary.md): publication and engineering safety limits;
- [`scripts/validate_public_ir.py`](scripts/validate_public_ir.py): zero-dependency public IR validator.

## Validate the example

```bash
python3 scripts/validate_public_ir.py assets/synthetic-frame-example.json
```

Expected result:

```text
OK: assets/synthetic-frame-example.json is a valid public structure reconstruction IR
```

## Scope

This public repository supports concept- and coordination-grade reconstruction. Geometric consistency does not establish structural capacity, safety, regulatory compliance, detailing completeness, or fabrication readiness. Consequential use requires authorized domain rules, independent validation, and appropriately qualified engineering review.
