#!/usr/bin/env python3
"""
卸载上海展厅导览 Skill

使用方法：
1. scp uninstall_shanghai_exhibition.py pi@<机器人IP>:/tmp/
2. ssh 到机器人
3. cd /opt/phanthy-motus
4. sudo python3 /tmp/uninstall_shanghai_exhibition.py
5. sudo docker compose restart agent-core
"""

import sqlite3
import json

slug = "shanghai-exhibition-guide"
db_path = "/opt/phanthy-motus/data/data.db"

conn = sqlite3.connect(db_path)
row = conn.execute("SELECT value FROM config WHERE key='skills'").fetchone()

if not row:
    print(f"ERROR: config key='skills' not found in {db_path}")
    conn.close()
    exit(1)

skills = json.loads(row[0])
before = len(skills["installed"])
skills["installed"] = [s for s in skills["installed"] if s.get("slug") != slug]
after = len(skills["installed"])

if before == after:
    print(f"WARNING: 技能 \"{slug}\" 未找到，无需卸载")
else:
    conn.execute("UPDATE config SET value=? WHERE key='skills'", (json.dumps(skills, ensure_ascii=False),))
    conn.commit()
    print(f"OK: 已卸载技能 \"{slug}\"({before} -> {after})")
    print(f"    接下来执行: sudo docker compose restart agent-core")

conn.close()
