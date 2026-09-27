# 学生画像统一 Schema

学生画像用于跨环节共享学情。建议以 JSON 落盘（如 `state/<学生名>.json`），各环节读取最新版本、执行后回写。字段含义固定，学科相关字段按需扩展。

## 画像 JSON 结构

```json
{
  "student_id": "唯一标识（姓名或学号）",
  "basic": {
    "grade": "年级",
    "subject": "主要学科（可多科）",
    "school": "学校（可选）",
    "notes": "其他备注"
  },
  "proficiency": {
    "overall": "总评（0-100 或 优/良/中/待提高）",
    "knowledge_map": [
      { "topic": "知识点", "mastery": "掌握度（0-100）", "updated": "最近更新" }
    ]
  },
  "weaknesses": [
    { "topic": "薄弱知识点", "attribution": "归因类别（见 error-taxonomy）", "detail": "具体表现", "plan": "对应订正/训练计划" }
  ],
  "preferences": {
    "learning_style": "视觉/听觉/动觉/读写",
    "pacing": "快/中/慢",
    "motivation": "兴趣点、内驱或外在动机",
    "known_triggers": "易挫败/易走神等场景"
  },
  "zpd": {
    "mastered": "已掌握（无需再练）",
    "next": "最近发展区（当前应练）",
    "too_far": "暂不适合（过难）"
  },
  "history": [
    { "date": "日期", "stage": "环节(A1-A10)", "summary": "做了什么", "outcome": "结果/数据", "notes": "备注" }
  ]
}
```

## 读写规则

1. 读到旧画像 → 先看 `updated`/`history` 判断是否最新，避免用过时数据。
2. 更新掌握度/薄弱点 → 保留 `updated` 时间戳，追加 `history` 记录，不覆盖删除已有结论（历史留痕）。
3. 跨学科：`subject` 与 `knowledge_map` 按学科区分；一个文件可含多学科。
4. 数据不足的字段：显式留空或标注「待补充」，不要编造默认值。
