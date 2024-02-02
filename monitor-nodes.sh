#!/bin/bash

output_file="monitor-nodes.log"

while true; do
    # Get nodes list
    nodes_list=$(kubectl get node -owide)
    pods_all=$(kubectl get pod -A | grep wait-forever | wc -l)  # wait-forever pods 
    pods_running=$(kubectl get pod -A | grep wait-forever | grep Running | wc -l)  # wait-forever pods of Running

    # Get current timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Create a line with timestamp, nodes list, and append to the output file
    echo -e "System time: $timestamp\nPodsAll: $pods_all\nPodsRunning:$pods_running\n$nodes_list\n" >> "$output_file"

    # Sleep for 1 minute
    sleep 60
done

