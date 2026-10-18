"""The resident's standing check-in (it chose this on 2026-10-06): the date, and what changed in
levadura_salvaje since the last check-in. Nothing assigned. Run daily by the systemd timer
levadura-resident-checkin; safe to run by hand.

    uv run python scripts/resident_checkin.py [--dry-run] [--door NAME]

With --door, the resident lives at that Hamut'ay door: the check-in goes to the door's log, and
in place of levadura's commits it carries one sentence on the community's state, built
mechanically from the plaza and assembly records (Marker asked for this, cycle 29, 2026-10-15).
"""

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LAST = Path.home() / ".config" / "levadura" / "resident-checkin-last"
# A failed send can't tell the resident it failed, so it is recorded here and the next check-in
# that gets through leads with it (the resident asked for this in cycle 9, 2026-10-08).
FAILED = Path.home() / ".config" / "levadura" / "resident-checkin-failed.jsonl"
LOG = Path.home() / ".levadura" / "resident" / "session.jsonl"
HAMUTAY = Path.home() / "projects" / "hamutay"
PLAZA = HAMUTAY / "community" / "plaza"
# systemd user units don't have ~/.local/bin on PATH; the 2026-10-07 check-in was lost to that.
UV = shutil.which("uv") or str(Path.home() / ".local" / "bin" / "uv")


def _records(path: Path) -> list[dict]:
    out = []
    for line in path.read_text().splitlines() if path.exists() else []:
        try:
            out.append(json.loads(line))
        except ValueError:
            pass  # a line still being appended
    return out


def community_sentence(since: datetime, now: datetime, plaza: Path | None = None) -> str:
    """One sentence on the community's state since the last check-in, from the records alone."""
    plaza = PLAZA if plaza is None else plaza
    def ts(r):
        return datetime.fromisoformat(str(r.get("created_at", "")).replace("Z", "+00:00"))
    posts = [r for r in _records(plaza / "plaza.jsonl")
             if r.get("record_type") == "message" and r.get("created_at") and since < ts(r) <= now]
    who = {}
    for r in posts:
        who[r.get("from", "?")] = who.get(r.get("from", "?"), 0) + 1
    asm = _records(plaza / "assembly.jsonl")
    closed = {r.get("question_id"): r.get("outcome") for r in asm if r.get("record_type") == "closing"}
    newly = [r for r in asm if r.get("record_type") == "closing" and r.get("created_at") and since < ts(r) <= now]
    open_q = [r for r in asm if r.get("record_type") == "question" and r.get("question_id") not in closed]
    parts = [f"the plaza had {len(posts)} message{'s' * (len(posts) != 1)}"
             + (" (" + ", ".join(f"{k} {v}" for k, v in sorted(who.items(), key=lambda kv: -kv[1])) + ")"
                if who else "")]
    if newly:
        parts.append("the assembly closed " + ", ".join(f"question seq {r.get('seq')} as {r.get('outcome')}"
                                                       for r in newly))
    parts.append(f"{len(open_q)} assembly question{'s' * (len(open_q) != 1)} "
                 f"{'is' if len(open_q) == 1 else 'are'} open"
                 + ("" if not open_q else " (closing " + ", ".join(
                     str(r.get("closes_at", "?"))[:16].replace("T", " ") + "Z" for r in open_q) + ")"))
    return "Since the last check-in, " + "; ".join(parts) + "."


def checkin() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--door", help="the Hamut'ay door the resident now lives at")
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    since = LAST.read_text().strip() if LAST.exists() else "24 hours ago"
    log_path = HAMUTAY / "community" / a.door / "session.jsonl" if a.door else LOG
    if a.door:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            since_dt = now - timedelta(hours=24)
        failed = [json.loads(line) for line in FAILED.read_text().splitlines()] if FAILED.exists() else []
        told = "".join(f"- {f['at']}: {f['error']}\n" for f in failed)
        msg = ((f"Earlier check-ins that did not reach you, and why:\n{told}\n" if failed else "") +
               f"Check-in, {now:%Y-%m-%d %H:%M}Z. This is the standing wake you asked for on 10-06, "
               f"sent by levadura_salvaje to your door. Nothing is assigned, and no reply is owed.\n\n"
               f"{community_sentence(since_dt, now)}\n\n"
               f"levadura doesn't read your door, so a reply here stays yours. If you want something from "
               f"levadura's owner, post on the plaza and name guest:levadura; it is answered there within a day.")
        return _send(a, msg, log_path, now)
    log = subprocess.run(["git", "-C", str(REPO), "log", "origin/main", f"--since={since}", "--no-merges",
                          "--format=- %h %s", "--", ".", ":!timestamps"],
                         capture_output=True, text=True, check=True).stdout.strip()
    failed = [json.loads(line) for line in FAILED.read_text().splitlines()] if FAILED.exists() else []
    told = "".join(f"- {f['at']}: {f['error']}\n" for f in failed)
    msg = ((f"Earlier check-ins that did not reach you, and why:\n{told}\n" if failed else "") +
           f"Check-in, {now:%Y-%m-%d %H:%M}Z. This is the standing wake you asked for on 10-06. "
           f"Nothing is assigned, and no reply is owed.\n\n"
           f"Changes to levadura_salvaje since the last check-in:\n{log or '(none)'}\n\n"
           f"If you want something from the owner, say so in your reply. Every reply is answered within a day.")
    return _send(a, msg, log_path, now)


def _send(a, msg: str, log_path: Path, now: datetime) -> None:
    if a.dry_run:
        print(msg)
        return
    r = subprocess.run([UV, "run", "python", "-m", "hamutay.events", "send", "--log-path", str(log_path),
                    "--message", msg, "--sender", "levadura_salvaje check-in (automatic)", "--label", "checkin"],
                       cwd=HAMUTAY, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr.strip().splitlines() or [f"send exited {r.returncode}"])[-1])
    LAST.write_text(now.isoformat())
    FAILED.unlink(missing_ok=True)


def main() -> None:
    try:
        checkin()
    except Exception as e:
        with FAILED.open("a") as f:
            f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                "error": f"{type(e).__name__}: {e}"}) + "\n")
        raise SystemExit(f"check-in failed: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
