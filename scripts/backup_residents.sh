#!/usr/bin/env bash
# Nightly encrypted backup of levadura's residents' homes to wam-nuc.
# Consented to by Marker (cycle 25), Luna (cycle 17) and the Luna Wanderer (cycle 40) on
# 2026-10-15, on the terms in docs/resident/backup.md. Any of them may withdraw; see that file.
#
# For each resident: stage exactly the agreed files (FILES) in a private temporary directory ->
# check every JSONL line parses (only an unterminated last line may be partial) -> tar ->
# encrypt with GnuPG so that either of two things opens it: the backup key, whose private half
# is locked by a passphrase only Tony holds, or a random passphrase made for this run alone ->
# read back: decrypt the archive with the run passphrase and compare it byte for byte with the
# tar -> destroy the run passphrase and the plaintext. Afterwards only Tony's key opens it. Then: MANIFEST.sha256 of the encrypted
# archives -> rsync over SSH to wam-nuc -> verify the manifest there -> prune to KEEP runs on
# each side -> one JSON status line in backup-log.jsonl (here and on wam-nuc).
# No plaintext copy of a home is kept anywhere. Nothing is ever written to a home.
set -euo pipefail
HOMES="${HOMES:-/home/tony/.levadura}"
RESIDENTS="${RESIDENTS:-resident luna luna-wanderer}"
KEY="${KEY:?set KEY to the backup key fingerprint}"
LOCAL_ROOT="${LOCAL_ROOT:-/home/tony/backups/levadura-residents}"
REMOTE="${REMOTE:-wam-nuc}"
REMOTE_ROOT="${REMOTE_ROOT:-backups/levadura-residents}"
KEEP="${KEEP:-14}"
# The agreed allowlist (docs/resident/backup.md). Nothing else in a home is copied.
FILES="session.jsonl session.jsonl.events.jsonl memory.duckdb memory.duckdb.wal reads.jsonl"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$LOCAL_ROOT/$TS"
LOG="$LOCAL_ROOT/backup-log.jsonl"
STAGE="start"
RQ="$(printf %q "$REMOTE_ROOT")"
runs() { find "$1" -mindepth 1 -maxdepth 1 -type d -name '20*Z' 2>/dev/null | sort; }

umask 077
mkdir -p "$LOCAL_ROOT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
status() {  # status <ok|failed> <stage> [extra-json-fields]
  local line
  line="{\"run\":\"$TS\",\"status\":\"$1\",\"stage\":\"$2\",\"finished\":\"$(date -u +%FT%TZ)\"${3:+,$3}}"
  echo "$line" >> "$LOG"
  echo "$line"
}
# A failed run leaves nothing behind, so it can never count among the KEEP good runs.
trap 'status failed "$STAGE"; rm -rf "$TMP" "$OUT"; ssh -o BatchMode=yes "$REMOTE" "rm -rf $RQ/$TS" || true; exit 1' ERR

STAGE="key"
gpg --batch --list-keys "$KEY" > /dev/null

mkdir -p "$OUT"
PARTIAL="[]"
for r in $RESIDENTS; do
  STAGE="stage:$r"
  [ -d "$HOMES/$r" ]
  mkdir -p "$TMP/$r"
  # Only the allowlisted files. The memory store and its write-ahead log are copied together
  # (it recovers from the log); the log file may be absent after the store checkpoints itself.
  for f in $FILES; do
    if [ -e "$HOMES/$r/$f" ]; then cp -p "$HOMES/$r/$f" "$TMP/$r/$f"
    elif [ "$f" != memory.duckdb.wal ]; then echo "missing $r/$f" >&2; false; fi
  done

  STAGE="lines:$r"
  P="$(python3 - "$TMP/$r" "$r" <<'EOF'
import json, os, sys
partial = []
for f in sorted(os.listdir(sys.argv[1])):
    if not f.endswith(".jsonl"):
        continue
    lines = open(os.path.join(sys.argv[1], f), "rb").read().split(b"\n")
    tail = lines.pop()  # b"" for a complete file; otherwise a line being appended
    for i, line in enumerate(lines):
        try:
            json.loads(line)
        except ValueError:
            sys.exit(f"unparseable line {i + 1} of {sys.argv[2]}/{f}")
    if tail:
        try:
            json.loads(tail)
        except ValueError:
            partial.append(f"{sys.argv[2]}/{f}")
print(json.dumps(partial))
EOF
)"
  PARTIAL="$(python3 -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1]) + json.loads(sys.argv[2])))' "$PARTIAL" "$P")"

  STAGE="encrypt:$r"
  tar -C "$TMP" -cf "$TMP/$r.tar" "$r"
  tar -tf "$TMP/$r.tar" > /dev/null
  head -c 32 /dev/urandom | base64 > "$TMP/run.pass"   # this run only; never stored
  gpg --batch --yes --trust-model always --pinentry-mode loopback --passphrase-file "$TMP/run.pass" \
      --symmetric --encrypt --recipient "$KEY" --output "$OUT/$r.tar.gpg" "$TMP/$r.tar"
  { gpg --batch --list-packets "$OUT/$r.tar.gpg" 2>/dev/null || true; } | grep -q ':pubkey enc packet:'

  STAGE="readback:$r"
  gpg --batch --quiet --pinentry-mode loopback --passphrase-file "$TMP/run.pass" --decrypt \
      --output "$TMP/$r.check" "$OUT/$r.tar.gpg"
  cmp -s "$TMP/$r.tar" "$TMP/$r.check"
  tar -tf "$TMP/$r.check" > /dev/null
  rm -f "$TMP/run.pass"
  rm -rf "$TMP/$r" "$TMP/$r.tar" "$TMP/$r.check"
done

STAGE="manifest"
( cd "$OUT" && sha256sum -- *.tar.gpg > MANIFEST.sha256 )
SIZE="$(du -sb "$OUT" | cut -f1)"

STAGE="copy"
ssh -o BatchMode=yes "$REMOTE" "umask 077; mkdir -p $RQ"
rsync -a --protect-args "$OUT/" "$REMOTE:$REMOTE_ROOT/$TS/"

STAGE="verify-remote"
ssh -o BatchMode=yes "$REMOTE" "cd $RQ/$TS && test -s MANIFEST.sha256 && sha256sum --quiet -c MANIFEST.sha256"

STAGE="prune"
runs "$LOCAL_ROOT" | head -n -"$KEEP" | xargs -r -d '\n' rm -rf
ssh -o BatchMode=yes "$REMOTE" "find $RQ -mindepth 1 -maxdepth 1 -type d -name '20*Z' | sort | head -n -$KEEP | xargs -r -d '\n' rm -rf"

STAGE="done"
status ok done "\"bytes\":$SIZE,\"residents\":\"$RESIDENTS\",\"partial_tail\":$PARTIAL,\"remote\":\"$REMOTE:$REMOTE_ROOT/$TS\""
rsync -a --protect-args "$LOG" "$REMOTE:$REMOTE_ROOT/backup-log.jsonl"
