import time
import sys
import os
import requests
import json
import threading

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))

from agent.event_sender import EventSender
from agent.agent_config import config

def send_dummy_event(sender, idx):
    data = {
        "original_text": f"Load Test Message {idx}",
        "detected_label": "scam",
        "confidence": 0.95,
        "raw_score": 0.95,
        "action_taken": "blocked"
    }
    # We use sender.send_event which handles encryption/auth
    # Mock token generation inside event_sender to avoid expiration issues in long tests?
    # It regenerates token each time.
    sender.send_event(data)

def load_test(num_requests=100, concurrency=10):
    print(f"--- Starting Load Test: {num_requests} requests, {concurrency} threads ---")
    sender = EventSender()
    
    start_time = time.time()
    
    threads = []
    for i in range(num_requests):
        t = threading.Thread(target=send_dummy_event, args=(sender, i))
        threads.append(t)
        t.start()
        
        if len(threads) >= concurrency:
            for t in threads:
                t.join()
            threads = []
            
    # Join remaining
    for t in threads:
        t.join()
        
    total_time = time.time() - start_time
    print(f"\nTotal Time: {total_time:.2f}s")
    print(f"Throughput: {num_requests / total_time:.2f} req/s")

if __name__ == "__main__":
    load_test()
