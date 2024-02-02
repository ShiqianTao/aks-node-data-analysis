import re
from datetime import datetime

# Path to the log file
log_file_path = "log/node-realtime-status.log"

# Path to the summary log file
summary_log_path = "log/flicker_summary.log"

# Regular expression pattern for extracting timestamp, node, and status
log_pattern = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(?P<node>akswin[^\s\t]+)[\s\t]+(?P<status>Ready|NotReady)')

# Dictionary to store node status changes
node_status = {}

# Function to parse the log file
def parse_log():
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = log_pattern.match(line)
            if match:
                timestamp = datetime.strptime(match.group('timestamp'), '%Y-%m-%d %H:%M:%S')
                node = match.group('node')
                status = match.group('status')

                # The first status start with 'Ready'
                if node not in node_status and status == 'Ready':
                    node_status[node] = []

                if node in node_status:
                    # Get the last status of node
                    last_status = ""
                    if len(node_status[node]) > 0:
                        _, last_status = node_status[node][-1]
                    
                    # Save the new different status
                    if status != last_status:
                        node_status[node].append((timestamp, status))

# Function to write the grouped and sorted summary to the log file
def write_grouped_and_sorted_summary():
    with open(summary_log_path, 'w') as summary_log:
        node_count = 0
        flicker_node_count = 0
        clicker_cannot_recover_node_count = 0
        for node, details in node_status.items():
            node_count += 1
            flicker_count = len(details) - 1
            if flicker_count == 0:
                continue
            flicker_node_count += 1
            if details[-1][1] == 'NotReady':
                clicker_cannot_recover_node_count += 1
            flicker_duration = details[-1][0] - details[0][0]
            summary_log.write(f"\n{node}\n")
            summary_log.write(f"flicker_count: {flicker_count}\n")
            summary_log.write(f"flicker_duration: {flicker_duration}\n")
            for timestamp, status in details:
                summary_log.write(f"{timestamp} {status}\n")
        summary_log.write(f"\n\nnode_count: {node_count}\n")
        summary_log.write(f"flicker_node_count: {flicker_node_count}\n")
        summary_log.write(f"clicker_cannot_recover_node_count: {clicker_cannot_recover_node_count}\n")

# Main execution
parse_log()
write_grouped_and_sorted_summary()
