import requests

# Backend base URL 
BASE_URL = "http://localhost:8080/api"

class login_user:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None  # Optional 

    def signup(self, email, password):
        url = f"{BASE_URL}/public/signup"
        payload = {
            "email": email,
            "password": password
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()  
        except requests.RequestException as e:
            print(f"[Signup Error] {e}")
            return None

    def login(self, email, password):
        url = f"{BASE_URL}/public/login"
        try:
            response = self.session.post(url, auth=(email, password))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[Login Error] {e}")
            return None

    def send_selected_data(self, selected_list):
        url = f"{BASE_URL}/private/send-data"
        try:
            response = self.session.post(url, json=selected_list)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[Data Send Error] {e}")
            return None

    def send_email_with_attachments(self, email_payload):
        url = f"{BASE_URL}/private/send-emails"
        try:
            response = self.session.post(url, json=email_payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[Email Send Error] {e}")
            return None
