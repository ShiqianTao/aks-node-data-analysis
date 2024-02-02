import subprocess
import threading
import time
import os
from datetime import datetime

# Ensure the log directory exists
os.makedirs('log', exist_ok=True)

# Function to monitor node status
def monitor_node_status():
    with open("log/node-realtime-status.log", "a") as file:
        process = subprocess.Popen(["kubectl", "get", "node", "-owide", "-w"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} {line.decode()}")
            file.flush()  # Flush the output buffer

# Function to monitor pod status
def monitor_pod_status():
    with open("log/pod-realtime-status.log", "a") as file:
        process = subprocess.Popen(["kubectl", "get", "pod", "-A", "-owide", "-w"], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} {line.decode()}")
            file.flush()  # Flush the output buffer

# Function to log status every minute
def log_status_every_minute():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nodes_list = subprocess.check_output(["kubectl", "get", "node", "-owide"]).decode()

        # Get all pods
        pods_output = subprocess.check_output(["kubectl", "get", "pod", "-A", "-owide"]).decode()

        # Count all pods, pods with name "wait-forever", and pods with name "wait-forever" that are running
        pods_all = pods_output.count("\n")  # Each pod is on a new line
        pods_wait_forever = 0
        pods_wait_forever_running = 0
        for line in pods_output.split('\n'):
            if 'wait-forever' in line:
                pods_wait_forever += 1
                if 'Running' in line:
                    pods_wait_forever_running += 1

        with open("log/minute-status.log", "a") as file:
            file.write(f"System time: {timestamp}\nPodsAll(kube-system and customer): {pods_all}\nPodsWaitForever(only customer): {pods_wait_forever}\nPodsWaitForeverRunning(only customer and running): {pods_wait_forever_running}\n{nodes_list}\n")
        time.sleep(60)

# Start the threads
threading.Thread(target=monitor_node_status).start()
threading.Thread(target=monitor_pod_status).start()
threading.Thread(target=log_status_every_minute).start()
