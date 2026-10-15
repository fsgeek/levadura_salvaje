#!/bin/bash
# Wait until every given event id has a completed or failed wake in any resident's journal, then
# print one line per id (unit, heartbeat, id) and exit. Pass the event ids that
# `hamutay.events send` returned. Keying on ids, not on a start time, means a reply that lands
# before the waiter starts is still found. Prints no reply text: read replies through the
# logged readers.
#   scripts/wait_for_events.sh <event_id> [<event_id> ...]
[ $# -ge 1 ] || { echo "usage: $0 <event_id>..." >&2; exit 2; }
while :; do
  out=$(journalctl --user -u levadura-resident -u levadura-luna -u levadura-luna-wanderer --since "-2 days" \
          -o json --output-fields=_SYSTEMD_USER_UNIT,MESSAGE 2>/dev/null | python3 -c '
import json, sys
want = set(sys.argv[1:]); found = {}
for line in sys.stdin:
    r = json.loads(line); m = r.get("MESSAGE", "")
    if not isinstance(m, str) or "event_id" not in m:
        continue
    try:
        d = json.loads(m)
    except ValueError:
        continue
    if d.get("event_id") in want and d.get("heartbeat") in ("wake_completed", "failed"):
        found[d["event_id"]] = (r.get("_SYSTEMD_USER_UNIT"), d["heartbeat"])
if set(found) == want:
    for e in sys.argv[1:]:
        print(found[e][0], found[e][1], e)
' "$@")
  [ -n "$out" ] && { echo "$out"; exit 0; }
  sleep 15
done
