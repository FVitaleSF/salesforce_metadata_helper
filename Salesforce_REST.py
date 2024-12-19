import requests
import streamlit as st
from urllib.parse import urljoin


class Salesforce_REST:

    AUTH_HEADER = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json", 
        }
    def __init__(self,params):
        self.domain = params['domain']
        self.client_id = params["client_id"]
        self.client_secret = params["client_secret"]
        self.base_url = self.make_endpoint()
        self.access_token = self.authenticate()
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def authenticate(self):       
        headers = Salesforce_REST.AUTH_HEADER
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        auth_endpoint = f"{self.base_url}/services/oauth2/token"
        response = requests.post(auth_endpoint, data=body, headers=headers)
        response.raise_for_status()  
        access_token = response.json().get("access_token")
        if response.status_code == 200:
            return access_token

    def revoke_auth(self):
        auth_endpoint = f"{self.base_url}/services/oauth2/revoke"
        headers = Salesforce_REST.AUTH_HEADER
        body = {}
        body['token'] = self.access_token
        requests.post(auth_endpoint,data = body, headers=headers)
    
    def do_get(self,endpoint,query):
        
        full_endpoint = full_endpoint = urljoin(self.base_url, endpoint)
        try:
            params = {'q': query}
            result = requests.get(full_endpoint,
                        headers=self.headers,
                        params=params)
            return result.json()
        
        except Exception as e:
            st.error(e)    

    def do_post(self,endpoint,body):
        full_endpoint = full_endpoint = urljoin(self.base_url, endpoint)

        try:
            result = requests.post(
                full_endpoint,
                headers = self.headers,
                json = body
            )
            return result.json()
        except Exception as e:
            st.error(e)

    def make_endpoint(self):
        return f"https://{self.domain}.my.salesforce.com"
