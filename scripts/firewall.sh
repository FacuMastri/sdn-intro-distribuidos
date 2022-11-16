#!/usr/bin/env bash

# Start the firewall
# Usage: firewall.sh <switch-id> <rules-path>

SWITCH_ID=$1
RULES_PATH=$2

if [ "$SWITCH_ID" ] && [ "$RULES_PATH" ]; then
    ./pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --rules_path="$RULES_PATH" --switch_id="$SWITCH_ID"
  else
    ./pox.py log.level --DEBUG log.color openflow.of_01 forwarding.l2_learning firewall --rules_path="$RULES_PATH" --switch_id=1
fi