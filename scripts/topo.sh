#!/usr/bin/env bash

# Start the topology
# Usage: topo.sh <number-of-switches>

N_SWITCHES=$1

if [ "$N_SWITCHES" ]; then
    sudo mn --custom ./src/topology.py --topo topologia,n_switches="$N_SWITCHES" --arp --mac --switch ovsk --controller remote
  else
    sudo mn --custom ./src/topology.py --topo topologia --arp --mac --switch ovsk --controller remote
fi