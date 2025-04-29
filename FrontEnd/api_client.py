import requests

BASE_URL = "http://localhost:8080/api"

class LoginUser:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None

    def signup(self, email, password):
        url = f"{BASE_URL}/auth/signup"
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
        url = f"{BASE_URL}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.auth_token = data.get("token")  # Save the JWT token
            return data
        except requests.RequestException as e:
            print(f"[Login Error] {e}")
            return None

    def _authorized_headers(self):
        if not self.auth_token:
            raise Exception("No auth token found. Please login first.")
        return {
            "Authorization": f"Bearer {self.auth_token}"
        }

    def send_selected_data(self, selected_list):
        url = f"{BASE_URL}/private/send-data"
        try:
            response = self.session.post(url, json=selected_list, headers=self._authorized_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[Data Send Error] {e}")
            return None

    def send_email_with_attachments(self, email_payload):
        url = f"{BASE_URL}/private/send-emails"
        try:
            response = self.session.post(url, json=email_payload, headers=self._authorized_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[Email Send Error] {e}")
            return None
