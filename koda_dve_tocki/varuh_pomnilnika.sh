#!/bin/bash
# Ustavi meritveni zagon (zahtevnost.py), če porabi več kot MEJA_KB pomnilnika.
MEJA_KB=${1:-8000000}
while pgrep -f "meri_zahtevnost.py" > /dev/null; do
  for pid in $(pgrep -f "zahtevnost.py [0-9]"); do
    rss=$(ps -o rss= -p "$pid" 2>/dev/null | tr -d ' ')
    if [ -n "$rss" ] && [ "$rss" -gt "$MEJA_KB" ]; then
      echo "$(date '+%H:%M:%S') ustavljen PID $pid pri $((rss / 1024)) MB: $(ps -o command= -p "$pid")" >> varuh_pomnilnika.log
      kill "$pid"
    fi
  done
  sleep 5
done
