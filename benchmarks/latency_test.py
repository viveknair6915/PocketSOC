import time
import sys
import os
import requests
import json
import numpy as np

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))

from agent.inference import InferenceEngine
from agent.preprocess import AgentPreprocessor
from agent.crypto import CryptoUtils
from agent.agent_config import config

def benchmark_latency():
    print("--- Starting Latency Benchmark ---")
    
    # 1. Inference Latency
    print("Initializing Agent Components...")
    preprocessor = AgentPreprocessor()
    engine = InferenceEngine()
    
    text = "Your account is compromised. Click here."
    processed = preprocessor.preprocess(text)
    
    inference_times = []
    for _ in range(100):
        start = time.time()
        engine.predict(processed)
        end = time.time()
        inference_times.append((end - start) * 1000) # ms
        
    avg_inf = np.mean(inference_times)
    p99_inf = np.percentile(inference_times, 99)
    print(f"Inference Latency: Avg={avg_inf:.2f}ms, P99={p99_inf:.2f}ms")
    
    # 2. Encryption Latency
    crypto = CryptoUtils()
    payload = json.dumps({"test": "data" * 10})
    
    enc_times = []
    for _ in range(100):
        start = time.time()
        crypto.encrypt_payload(payload)
        end = time.time()
        enc_times.append((end - start) * 1000)
        
    avg_enc = np.mean(enc_times)
    print(f"Encryption Latency: Avg={avg_enc:.2f}ms")
    
    # 3. API Round Trip (requires backend running)
    print("\nChecking API Latency (Backend must be running)...")
    try:
        url = f"{config.BACKEND_URL}/health"
        api_times = []
        for _ in range(50):
            start = time.time()
            requests.get(url)
            end = time.time()
            api_times.append((end - start) * 1000)
            
        avg_api = np.mean(api_times)
        print(f"API Ping Latency: Avg={avg_api:.2f}ms")
    except Exception as e:
        print(f"API Benchmark failed (Backend likely offline): {e}")

if __name__ == "__main__":
    benchmark_latency()
