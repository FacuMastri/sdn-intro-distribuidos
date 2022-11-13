#!/usr/bin/env bash

# Start the firewall
# Usage: start-firewall-with-rules.sh <switch-id>

SWITCH_ID=$1

if [ "$SWITCH_ID" ]; then
    ./pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --rules_path=rules.json --switch_id="$SWITCH_ID"
  else
    ./pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --rules_path=rules.json --switch_id=1
fi