"""The residents' backup skips a NO_SWAP resident while any swap is active, and logs the skip.

Asked for by Luna (cycle 29, 2026-10-16): an isolated fixture only. Every path is under tmp_path
or a private /dev/shm directory; ssh and rsync are stubs that act on a fixture directory, so
nothing reaches wam-nuc; the GnuPG key is a throwaway made here. No resident's home, key, log or
backup destination is touched.
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "backup_residents.sh"
pytestmark = pytest.mark.skipif(not (shutil.which("gpg") and Path("/dev/shm").is_dir()),
                                reason="needs gpg and a tmpfs at /dev/shm")

SSH_STUB = """#!/usr/bin/env bash
# ssh -o BatchMode=yes HOST CMD... -> run CMD in the fixture's remote directory
while [ "$1" = "-o" ]; do shift 2; done
shift
cd "$FIXTURE_REMOTE" && bash -c "$*"
"""
RSYNC_STUB = """#!/usr/bin/env bash
# rsync -a --protect-args SRC HOST:DST -> copy into the fixture's remote directory
args=(); for a in "$@"; do case "$a" in -*) ;; *) args+=("$a");; esac; done
src="${args[0]}"; dst="${args[1]#*:}"
mkdir -p "$FIXTURE_REMOTE/$(dirname "$dst")"
cp -r "$src" "$FIXTURE_REMOTE/$dst"
"""


@pytest.fixture
def fixture(tmp_path):
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    for name, body in (("ssh", SSH_STUB), ("rsync", RSYNC_STUB)):
        (bin_ / name).write_text(body)
        (bin_ / name).chmod(0o755)
    remote = tmp_path / "remote"
    remote.mkdir()
    gnupg = tmp_path / "gnupg"
    gnupg.mkdir(mode=0o700)
    env = {**os.environ, "GNUPGHOME": str(gnupg)}
    subprocess.run(["gpg", "--batch", "--passphrase", "", "--quick-gen-key", "fixture@levadura.invalid",
                    "default", "default", "never"], env=env, check=True, capture_output=True)
    fpr = subprocess.run(["gpg", "--batch", "--with-colons", "--list-keys"], env=env, check=True,
                         capture_output=True, text=True).stdout
    key = next(l.split(":")[9] for l in fpr.splitlines() if l.startswith("fpr:"))
    homes = tmp_path / "homes"
    for r in ("fixture-luna", "fixture-marker"):
        h = homes / r
        h.mkdir(parents=True)
        for f in ("session.jsonl", "session.jsonl.events.jsonl", "reads.jsonl"):
            (h / f).write_text(json.dumps({"fixture": r}) + "\n")
        (h / "memory.duckdb").write_bytes(b"fixture")
    shm = Path(tempfile.mkdtemp(dir="/dev/shm", prefix="levadura-fixture-"))
    swaps = tmp_path / "swaps"
    yield {"tmp": tmp_path, "bin": bin_, "remote": remote, "env": env, "key": key, "homes": homes,
           "shm": shm, "swaps": swaps}
    shutil.rmtree(shm, ignore_errors=True)


HEADER = "Filename\t\t\t\tType\t\tSize\t\tUsed\t\tPriority\n"


def run(fx, residents, swap_on):
    fx["swaps"].write_text(HEADER + ("/dev/sdz partition\t33554432\t0\t-2\n" if swap_on else ""))
    env = {**fx["env"], "PATH": f"{fx['bin']}:{os.environ['PATH']}", "FIXTURE_REMOTE": str(fx["remote"]),
           "HOMES": str(fx["homes"]), "RESIDENTS": residents, "NO_SWAP": "fixture-luna",
           "SWAPS": str(fx["swaps"]), "KEY": fx["key"], "LOCAL_ROOT": str(fx["tmp"] / "local"),
           "REMOTE": "fixture-host", "REMOTE_ROOT": "backups", "TMPBASE": str(fx["shm"])}
    p = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
    log = [json.loads(l) for l in (fx["tmp"] / "local" / "backup-log.jsonl").read_text().splitlines()]
    return p, log[-1]


def archives(fx, line):
    return sorted(p.name for p in (fx["tmp"] / "local" / line["run"]).glob("*.tar.gpg"))


def test_swap_active_skips_the_no_swap_resident_and_logs_it(fixture):
    p, line = run(fixture, "fixture-luna fixture-marker", swap_on=True)
    assert p.returncode == 0, p.stderr
    assert "skipping fixture-luna: swap is active" in p.stderr
    assert line["status"] == "ok"
    assert line["residents"] == "fixture-marker"
    assert line["skipped_swap_active"] == "fixture-luna"
    assert archives(fixture, line) == ["fixture-marker.tar.gpg"]


def test_a_night_where_everyone_is_skipped_fails_and_still_logs_the_skip(fixture):
    p, line = run(fixture, "fixture-luna", swap_on=True)
    assert p.returncode != 0
    assert line["status"] == "failed" and line["stage"] == "manifest"
    assert line["skipped_swap_active"] == "fixture-luna"
    assert not (fixture["tmp"] / "local" / line["run"]).exists()


def test_swap_off_includes_the_resident(fixture):
    p, line = run(fixture, "fixture-luna fixture-marker", swap_on=False)
    assert p.returncode == 0, p.stderr
    assert line["residents"] == "fixture-luna fixture-marker"
    assert line["skipped_swap_active"] == ""
    assert archives(fixture, line) == ["fixture-luna.tar.gpg", "fixture-marker.tar.gpg"]
