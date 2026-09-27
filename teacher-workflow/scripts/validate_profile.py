#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学生画像校验脚本 validate_profile.py

用途：防止多个环节（A1-A10）写入/回写学生画像时把 JSON 写坏。
在任何环节回写 state/<学生名>.json 之后运行一次，或由 AI 在写入前/后自动调用。

用法:
    python validate_profile.py <profile.json>
退出码: 0=通过  1=结构错误  2=用法错误/文件不存在

校验范围（对应 references/student-profile.md 的 Schema）:
    顶层字段、basic、proficiency.knowledge_map、weaknesses、zpd、history
"""
import json
import sys

REQUIRED_TOP = ["student_id", "basic", "proficiency", "weaknesses", "preferences", "zpd", "history"]
REQUIRED_BASIC = ["grade", "subject"]
KM_KEYS = ["topic", "mastery", "updated"]
WEAK_KEYS = ["topic", "attribution", "detail", "plan"]
ZPD_KEYS = ["mastered", "next", "too_far"]
HISTORY_KEYS = ["date", "stage", "summary"]
ALLOWED_STAGES = {"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"}
ATTRIBUTIONS = {"概念未掌握", "审题失误", "计算断链", "公式会用不会用", "变式迁移不足", "待进一步诊断"}

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def validate_required_keys(obj, keys, label):
    if not isinstance(obj, dict):
        check(False, f"{label} 应为对象 (dict)")
        return
    for k in keys:
        check(k in obj, f"{label} 缺少字段: {k}")


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_profile.py <profile.json>")
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[FAIL] 文件不存在: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[FAIL] JSON 格式错误（多为多环节并发写入互相覆盖所致）: {e}")
        sys.exit(1)

    for k in REQUIRED_TOP:
        check(k in data, f"缺少顶层字段: {k}")

    validate_required_keys(data.get("basic"), REQUIRED_BASIC, "basic")

    prof = data.get("proficiency")
    if isinstance(prof, dict):
        km = prof.get("knowledge_map", [])
        check(isinstance(km, list), "proficiency.knowledge_map 应为数组")
        for i, item in enumerate(km):
            validate_required_keys(item, KM_KEYS, f"knowledge_map[{i}]")
            m = item.get("mastery")
            check(isinstance(m, (int, float)) and 0 <= m <= 100,
                  f"knowledge_map[{i}].mastery 应为 0-100 数字，当前: {m!r}")

    weak = data.get("weaknesses")
    if weak is not None:
        check(isinstance(weak, list), "weaknesses 应为数组")
        for i, item in enumerate(weak):
            validate_required_keys(item, WEAK_KEYS, f"weaknesses[{i}]")
            if isinstance(item, dict) and "attribution" in item:
                check(item["attribution"] in ATTRIBUTIONS,
                      f"weaknesses[{i}].attribution 不在归因五类中: {item['attribution']!r}")

    validate_required_keys(data.get("zpd"), ZPD_KEYS, "zpd")

    hist = data.get("history")
    if hist is not None:
        check(isinstance(hist, list), "history 应为数组")
        for i, item in enumerate(hist):
            validate_required_keys(item, HISTORY_KEYS, f"history[{i}]")
            if isinstance(item, dict) and "stage" in item:
                check(item["stage"] in ALLOWED_STAGES,
                      f"history[{i}].stage 应为 A1-A10，当前: {item['stage']!r}")

    if errors:
        print(f"[FAIL] 共 {len(errors)} 处问题:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    print(f"[OK] 画像校验通过: {path}")
    print(f"     知识点 {len(prof.get('knowledge_map', [])) if isinstance(prof, dict) else 0} 个 | "
          f"薄弱点 {len(weak) if isinstance(weak, list) else 0} 条 | "
          f"历史记录 {len(hist) if isinstance(hist, list) else 0} 条")
    sys.exit(0)


if __name__ == "__main__":
    main()
