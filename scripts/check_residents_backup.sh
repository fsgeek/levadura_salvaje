#!/usr/bin/env bash
# Is the residents' backup alive? The last run must be ok and younger than 26 h. A failure fails
# this unit; `systemctl --user list-units --failed` shows it. Read-only.
LOG="${LOG:-/home/tony/backups/levadura-residents/backup-log.jsonl}"
python3 - "$LOG" <<'PY'
import json, sys, datetime as dt
try:
    r = json.loads(open(sys.argv[1]).read().strip().splitlines()[-1])
except Exception:
    print(f"FAIL residents backup: no record at {sys.argv[1]}"); sys.exit(1)
age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(r["finished"].replace("Z", "+00:00"))
good = r["status"] == "ok" and age <= dt.timedelta(hours=26)
print(f"{'ok  ' if good else 'FAIL'} residents backup: {r['status']} at {r['finished']} ({age.total_seconds()/3600:.1f} h ago)")
sys.exit(0 if good else 1)
PY
