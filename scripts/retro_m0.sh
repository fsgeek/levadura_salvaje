#!/bin/bash
# Retrospective forecast, arm M0 (docs/retrospective-design.md, draft 3): for one
# fold, train two mini-AGI readers (seeds 0 and 1) from scratch on that fold's
# 1997 corpus, then score the fold's held-out cohort sections with each.
# One fold per ayllu-gpu lease, so Hamut'ay's resident is rested ~1.5h at a time.
# Same reader settings as obs-0147 (resident 16, context 2048); 31 minutes on
# the 4090 is ~9.7M characters, the obs-0147 budget. Resumable via markers.
#
# Usage: scripts/retro_m0.sh <fold>
set -euo pipefail
K=$1
L=$(git -C "$(dirname "$0")" rev-parse --show-toplevel); M=/home/tony/projects/mini-AGI
PY=$L/.venv-minagi/bin/python; R=$L/data/retro/runs; mkdir -p $R
python3 -c "
import json; rows=json.load(open('$L/results/retro-m0-folds-v1.json'))
json.dump([r for r in rows if r['fold']==$K], open('$R/fold$K-sections.json','w'))"
exec /home/tony/projects/hamutay/deploy/ayllu-gpu run --holder levadura-salvaje \
  --purpose "retrospective forecast M0: fold $K, two mini-AGI readers + scoring" --ttl 2h -- bash -c '
    set -euo pipefail
    cd '"$M"'
    for S in 0 1; do
      W='"$R"'/fold'"$K"'-seed$S
      if [ ! -f $W.trained ]; then
        rm -rf $W
        '"$PY"' train.py read '"$L"'/data/retro/fold'"$K"'/train --save --weights-dir $W \
          --held-out '"$L"'/data/retro/fold'"$K"'/val --seed $S --minutes 31 --resident 16 --context-end 2048 > $W.log 2>&1
        grep -q "^read " $W.log && touch $W.trained
      fi
      if [ ! -f $W.scored ]; then
        MINAGI_EDITION=1997 '"$PY"' '"$L"'/scripts/minagi_score.py $W $W.scores.jsonl '"$R"'/fold'"$K"'-sections.json > $W.score.log 2>&1
        touch $W.scored
      fi
    done'
