#!/bin/sh
# Machine state, recorded with every measurement (AGENTS.md: heat and load are part of reality).
echo "state: $(date '+%F %T') | $(uptime | sed 's/.*load/load/') | swap $(sysctl -n vm.swapusage | sed 's/(encrypted)//;s/  */ /g') | $(pmset -g batt | head -1 | sed 's/Now drawing from //') | $(pmset -g therm 2>&1 | tr '\n' ' ' | sed 's/Note: //g') | $(sysctl -n machdep.cpu.brand_string)"
