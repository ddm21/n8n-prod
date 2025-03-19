import requests
import concurrent.futures
import time
from collections import defaultdict
import os

URL = "https://prod.korex.ovh/prod/test"
NUM_REQUESTS_PER_MINUTE = 60  # Number of requests per minute
TEST_DURATION = 30  # Duration in seconds
LOG_FILE = f"load-test-{int(time.time())}.log"  # Log file with Unix timestamp

REQUEST_INTERVAL = 60 / NUM_REQUESTS_PER_MINUTE  # Time between requests

def send_request(session, request_id):
    start_time = time.time()
    try:
        response = session.get(URL, timeout=10)  # Added timeout to prevent hanging
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            try:
                worker = response.json().get("containerId", "Unknown Worker")
            except Exception as e:
                worker = f"Error parsing JSON: {e}"
        else:
            worker = f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        worker = f"Request failed: {e}"
        elapsed_time = -1  # Indicating failure
    
    print(f"Request {request_id}: {worker}, Time: {elapsed_time:.4f} sec")
    return worker, elapsed_time

def main():
    worker_stats = defaultdict(list)
    start_time = time.time()
    total_requests = 0
    
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS_PER_MINUTE) as executor:
            while time.time() - start_time < TEST_DURATION:
                batch_start_time = time.time()
                futures = {executor.submit(send_request, session, i) for i in range(NUM_REQUESTS_PER_MINUTE)}
                for future in concurrent.futures.as_completed(futures):
                    worker, response_time = future.result()
                    if response_time >= 0:
                        worker_stats[worker].append(response_time)
                        total_requests += 1
                
                elapsed_batch_time = time.time() - batch_start_time
                sleep_time = max(0, REQUEST_INTERVAL - elapsed_batch_time)
                time.sleep(sleep_time)  # Ensures requests are sent at a controlled rate
    
    with open(LOG_FILE, "w") as log_file:
        log_file.write("Final Summary:\n")
        for worker, times in worker_stats.items():
            avg_time = sum(times) / len(times) if times else 0
            min_time = min(times) if times else 0
            max_time = max(times) if times else 0
            count = len(times)
            summary_entry = (f"{worker}: {count} requests, "
                             f"Avg Time: {avg_time:.4f} sec, "
                             f"Min Time: {min_time:.4f} sec, "
                             f"Max Time: {max_time:.4f} sec\n")
            log_file.write(summary_entry)
        total_entry = f"Total Requests Sent: {total_requests}\n"
        log_file.write(total_entry)
    
    print(f"Log file saved as: {os.path.abspath(LOG_FILE)}")

if __name__ == "__main__":
    main()
