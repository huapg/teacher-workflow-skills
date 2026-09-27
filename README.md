# Teacher Workflow Skills（教师全流程 Agent 技能套件）

一套面向**教师侧教学交付**的 Agent 技能集。把教学工作编排为「教前 · 教中 · 教后」三大阶段共 **10 个环节**（A1–A10），由总协调器负责环节路由、统一学生画像的读写与跨环节数据衔接。

> 面向 AI Agent 环境使用，可作为可安装的 Skill 集（每目录含 `SKILL.md`），也可直接参考其中的流程、规范与示例话术。

---

## 十环节地图

| 阶段 | 环节 | 对应 Skill | 产出 |
| --- | --- | --- | --- |
| 教前 | A1 学情诊断 | `teacher-a1-diagnosis` | 学生画像（起点） |
| 教前 | A2 备课 | `teacher-a2-lesson-prep` | 教案/教学设计 |
| 教前 | A3 变式出题 | `teacher-a3-question-gen` | 题组/分层作业 |
| 教中 | A4 课堂讲义 | `teacher-a4-lecture-notes` | 讲义/板书/课件文案 |
| 教中 | A5 实时答疑 | `teacher-a5-realtime-qa` | 引导式答疑 |
| 教中 | A6 作业批改 | `teacher-a6-homework-grading` | 成绩单/错题汇总 |
| 教中 | A7 错题归因 | `teacher-a7-error-attribution` | 归因+订正建议 |
| 教后 | A8 计算训练 | `teacher-a8-practice-drill` | 训练题/练习单 |
| 教后 | A9 学习规划 | `teacher-a9-learning-plan` | 个性化学习计划 |
| 教后 | A10 家长反馈 | `teacher-a10-parent-feedback` | 家校沟通文案 |

## 仓库结构

```
teacher-workflow-skills/
├── teacher-a1-diagnosis/SKILL.md      # 学情诊断
├── teacher-a2-lesson-prep/SKILL.md    # 备课
├── teacher-a3-question-gen/SKILL.md   # 变式出题
├── teacher-a4-lecture-notes/SKILL.md  # 课堂讲义
├── teacher-a5-realtime-qa/SKILL.md    # 实时答疑
├── teacher-a6-homework-grading/SKILL.md # 作业批改
├── teacher-a7-error-attribution/SKILL.md # 错题归因
├── teacher-a8-practice-drill/SKILL.md # 计算训练
├── teacher-a9-learning-plan/SKILL.md  # 学习规划
├── teacher-a10-parent-feedback/SKILL.md # 家长反馈
└── teacher-workflow/                  # 总协调器（编排层）
    ├── SKILL.md                       # 环节调度、画像读写、跨环节衔接
    ├── references/
    │   ├── workflow-routing.md        # 环节判定与路由规则
    │   ├── student-profile.md         # 学生画像统一 schema
    │   ├── error-taxonomy.md          # 错题归因分类法（五类）
    │   ├── question-format.md         # 出题/变式规范
    │   └── example-prompts.md         # 十环节示例 prompt 集
    ├── scripts/
    │   └── validate_profile.py        # 画像校验脚本
    └── state/
        └── 小明.json                   # 示例学生画像
```

## 设计理念

- **编排层 + 执行层分离**：`teacher-workflow` 是编排层（路由、统一画像），十个 `teacher-a*` 是执行层（各自环节）。执行层可独立使用，完整流程中由编排层统一数据，避免同一学生产生互相矛盾的画像。
- **共享学生画像**：学生学情以 JSON 落盘（`state/<学生名>.json`），各环节读写最新版本，保证跨环节数据衔接（schema 见 `references/student-profile.md`）。
- **错题归因驱动**：五类归因法（概念未掌握 / 审题失误 / 计算断链 / 公式会用不会用 / 变式迁移不足）贯穿 A5/A6/A7/A8/A9，训练与规划都围绕归因结果展开。
- **难度分层 L1–L4**：出题、训练、作业按难度分层，并贴合最近发展区（ZPD）。

## 快速使用

### 方式一：安装为 Skill（推荐 Agent 环境）

将 `teacher-workflow` 及需要的 `teacher-a*` 目录放入 Agent 的 skill 目录（如 `.user_skills/`），即可由总协调器自动路由环节。首次使用：

```bash
# 将仓库克隆或拷贝到 skill 目录
git clone https://github.com/huapg/teacher-workflow-skills.git
# 或仅复制需要环节的目录到你的 skill 根目录
```

### 方式二：直接复制示例话术

`teacher-workflow/references/example-prompts.md` 提供十环节即贴即用的话术，例如：

- 「给初二的 <学生名> 做一次学情诊断，他最近一元二次方程总出错」
- 「批改这份作业，分析错因，给 <学生名> 生成针对性变式训练」
- 「为 <学生名> 家长写一份阶段反馈，突出进步，语气鼓励」

一句话可串联多个环节（如「批改 → 归因 → 训练」），Agent 会按教学时序顺序执行。

## 工作流参考

- **开学/新学生**：A1 → A2 → A4（先诊断，再备课/讲义）
- **随堂答疑**：A5 为主；学生卡壳 → A7 归因 → A8 训练
- **作业闭环**：A6 批改 → A7 归因 → A3/A8 变式训练 → A9 规划沉淀 → A10 反馈家长
- **周期性**：A9 按月滚动，A1 按周/月复检更新画像

完整路由规则见 `teacher-workflow/references/workflow-routing.md`。

## 校验脚本

任何环节回写学生画像后，建议运行校验，防止多环节并发写入把 JSON 写坏：

```bash
python teacher-workflow/scripts/validate_profile.py teacher-workflow/state/小明.json
# 退出码：0=通过  1=结构错误  2=用法错误/文件不存在
```

## 贡献与交流

欢迎通过 Issue 或 Pull Request 贡献新的环节、学科示范（数学已示范，可扩展语文/英语/物理等）或改进现有规范。

**交流 QQ 群：1079921178**，欢迎加入讨论使用与改进。

## 许可

本仓库基于 **MIT License** 开源（见 `LICENSE` 文件），可自由使用、修改与分发，使用请保留版权与出处。
