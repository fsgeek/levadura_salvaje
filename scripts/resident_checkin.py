"""The resident's standing check-in (it chose this on 2026-10-06): the date, and what changed in
levadura_salvaje since the last check-in. Nothing assigned. Run daily by the systemd timer
levadura-resident-checkin; safe to run by hand.

    uv run python scripts/resident_checkin.py [--dry-run]"""

import argparse
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LAST = Path.home() / ".config" / "levadura" / "resident-checkin-last"
LOG = Path.home() / ".levadura" / "resident" / "session.jsonl"
HAMUTAY = Path.home() / "projects" / "hamutay"
# systemd user units don't have ~/.local/bin on PATH; the 2026-10-07 check-in was lost to that.
UV = shutil.which("uv") or str(Path.home() / ".local" / "bin" / "uv")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    since = LAST.read_text().strip() if LAST.exists() else "24 hours ago"
    log = subprocess.run(["git", "-C", str(REPO), "log", "origin/main", f"--since={since}", "--no-merges",
                          "--format=- %h %s", "--", ".", ":!timestamps"],
                         capture_output=True, text=True, check=True).stdout.strip()
    msg = (f"Check-in, {now:%Y-%m-%d %H:%M}Z. This is the standing wake you asked for on 10-06. "
           f"Nothing is assigned, and no reply is owed.\n\n"
           f"Changes to levadura_salvaje since the last check-in:\n{log or '(none)'}\n\n"
           f"If you want something from the owner, say so in your reply. Every reply is answered within a day.")
    if a.dry_run:
        print(msg)
        return
    r = subprocess.run([UV, "run", "python", "-m", "hamutay.events", "send", "--log-path", str(LOG),
                    "--message", msg, "--sender", "levadura_salvaje check-in (automatic)", "--label", "checkin"],
                       cwd=HAMUTAY, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"send failed ({r.returncode}):\n{r.stderr}")
    LAST.write_text(now.isoformat())


if __name__ == "__main__":
    main()
