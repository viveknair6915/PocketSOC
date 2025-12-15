import requests
import sys

def verify_admin():
    base_url = "http://localhost:8000"
    
    # 1. Login as Admin
    print("Logging in as Admin...")
    resp = requests.post(f"{base_url}/auth/token", data={"username": "admin", "password": "admin"})
    if resp.status_code != 200:
        print("Login failed")
        sys.exit(1)
        
    token = resp.json()["access_token"]
    print("Admin Token acquired.")
    
    # 2. Get Incidents
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{base_url}/incident/all", headers=headers)
    
    if resp.status_code == 200:
        incidents = resp.json()
        print(f"Successfully retrieved {len(incidents)} incidents from DB.")
        if incidents:
            print("Latest Incident:", incidents[-1])
    else:
        print(f"Failed to fetch incidents: {resp.text}")

if __name__ == "__main__":
    verify_admin()
