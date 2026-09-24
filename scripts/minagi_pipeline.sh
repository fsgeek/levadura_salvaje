#!/bin/bash
# mini-AGI instrument on gazelle: train seeds 0-2 from scratch on the 1997 CFR,
# 60 minutes each, then score the stratified 2025 sample with each.
# Resumable: a finished stage leaves a marker; an interrupted training run
# resumes from its last checkpoint (every 5 minutes) with the minutes left.
set -uo pipefail
L=$HOME/projects/levadura_salvaje; M=$HOME/projects/mini-AGI; PY=$L/.venv-minagi/bin/python
R=$L/minagi-runs; mkdir -p $R
cd $M
for seed in 0 1 2; do
  W=$R/seed$seed
  if [ ! -f $W.trained ]; then
    used=$(cat $W.minutes 2>/dev/null || echo 0)
    left=$((60 - used))
    if [ $left -gt 0 ]; then
      start=$(date +%s)
      $PY train.py read $L/data/minagi/train --save --weights-dir $W --held-out $L/data/minagi/val \
        --seed $seed --minutes $left --sample-every 1000000 --sample-log $W-samples.txt >> $W.log 2>&1
      echo $(( used + ($(date +%s) - start) / 60 )) > $W.minutes
    fi
    grep -q "^read " $W.log && touch $W.trained
  fi
  [ -f $W.trained ] || { echo "seed $seed training incomplete"; exit 1; }
  if [ ! -f $W.scored ]; then
    $PY $L/scripts/minagi_score.py $W $R/score-seed$seed.jsonl $L/data/minagi/sample-2025.json >> $W.score.log 2>&1 \
      && touch $W.scored
  fi
done
echo ALL_DONE
