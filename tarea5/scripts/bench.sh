#!/bin/zsh
# Uso: bench.sh <particle> <box_label> <output_file_to_measure> -- <cmd...>
set -e
PART="$1"; BOX="$2"; OUTFILE="$3"; shift 3
[[ "$1" == "--" ]] && shift
START=$(python3 -c 'import time; print(time.time())')
"$@"
END=$(python3 -c 'import time; print(time.time())')
SECS=$(python3 -c "print(f'{$END - $START:.3f}')")
if [[ -f "$OUTFILE" ]]; then
  BYTES=$(stat -f%z "$OUTFILE")
else
  BYTES=0
fi
echo "$PART,$BOX,$SECS,$BYTES" >> results.csv
echo ">>> $PART | $BOX | ${SECS}s | ${BYTES} bytes | $OUTFILE"
