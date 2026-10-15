#!/bin/bash
# Exit on the first completed or failed wake of any resident since $1 (default: now).
# Prints only unit, heartbeat and event id, never response text (reads go through the logged readers).
start="${1:-$(date -u '+%Y-%m-%d %H:%M:%S UTC')}"
while :; do
  hit=$(journalctl --user -u levadura-resident -u levadura-luna -u levadura-luna-wanderer --since "$start" -o cat --output-fields=_SYSTEMD_USER_UNIT,MESSAGE -o json 2>/dev/null \
    | python3 -c '
import json, sys
for line in sys.stdin:
    r = json.loads(line); m = r.get("MESSAGE", "")
    if isinstance(m, list): continue
    if "\"wake_completed\"" in m or "\"status\": \"failed\"" in m or "\"heartbeat\": \"failed\"" in m:
        try: d = json.loads(m)
        except Exception: d = {}
        print(r.get("_SYSTEMD_USER_UNIT"), d.get("heartbeat"), d.get("event_id")); break')
  [ -n "$hit" ] && { echo "$hit"; exit 0; }
  sleep 30
done
