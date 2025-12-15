import requests
import json
import time
from jose import jwt
from datetime import datetime, timedelta
from agent_config import config
from crypto import CryptoUtils

class EventSender:
    def __init__(self):
        self.backend_url = config.BACKEND_URL
        self.crypto = CryptoUtils()
        
    def generate_token(self):
        # Simulate generating a token signed with agent secret
        # In real world, might exchange cert for token, or use long-lived token
        payload = {
            "sub": config.AGENT_ID,
            "role": "agent",
            "exp": datetime.utcnow() + timedelta(minutes=5)
        }
        token = jwt.encode(payload, config.AGENT_SECRET_KEY, algorithm="HS256")
        return token

    def send_event(self, incident_data):
        url = f"{self.backend_url}/incident/report"
        
        # 1. Encrypt payload
        payload_str = json.dumps(incident_data)
        encrypted_payload = self.crypto.encrypt_payload(payload_str)
        
        # 2. Prepare Request
        token = self.generate_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "agent_id": config.AGENT_ID,
            "encrypted_payload": encrypted_payload,
            "timestamp": datetime.utcnow().isoformat(),
            "model_version": "1.0.0"
        }
        
        # 3. Send with Retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=body, headers=headers)
                if response.status_code in [200, 201]:
                    print(f"Event sent successfully: {response.json()}")
                    return True
                else:
                    print(f"Failed to send event (Attempt {attempt+1}): {response.text}")
            except Exception as e:
                print(f"Connection error (Attempt {attempt+1}): {e}")
            
            time.sleep(2)
            
        print("Giving up on sending event.")
        return False

if __name__ == "__main__":
    sender = EventSender()
    # sender.send_event({"test": "data"}) # Will fail if backend not running
