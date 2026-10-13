#!/bin/zsh
# Stops every Codex session at 12:45 Paris time each day (the runner resumes them at 23:00).
while true; do
  hm=$(TZ=Europe/Paris date +%H%M)
  if [ "$hm" -ge 1245 ] && [ "$hm" -lt 1300 ]; then pkill -INT -f "CodexCLI.app/Contents/MacOS" && echo "$(date -u +%FT%TZ) watchdog stopped Codex for Julien's hours" >> $HOME/Research/emergent-space/artifacts/runs/codex-oct13/status-watchdog.txt; fi
  sleep 60
done
