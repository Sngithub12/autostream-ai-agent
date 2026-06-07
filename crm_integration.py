"""
CRM Integration (Salesforce, HubSpot, Pipedrive)
"""
import os
import requests
import logging

logger = logging.getLogger(__name__)

class SalesforceIntegration:
    def __init__(self, instance_url: str, client_id: str, client_secret: str):
        self.instance_url = instance_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
    
    def authenticate(self):
        """Authenticate with Salesforce"""
        try:
            response = requests.post(
                f"{self.instance_url}/services/oauth2/token",
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )
            self.access_token = response.json()['access_token']
            return True
        except Exception as e:
            logger.error(f"Salesforce auth error: {e}")
            return False
    
    def create_lead(self, name: str, email: str, company: str = None) -> bool:
        """Create lead in Salesforce"""
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            data = {
                'LastName': name,
                'Email': email,
                'Company': company or 'Unknown'
            }
            response = requests.post(
                f"{self.instance_url}/services/data/v57.0/sobjects/Lead",
                json=data,
                headers=headers
            )
            logger.info(f"Lead created in Salesforce: {name}")
            return response.status_code == 201
        except Exception as e:
            logger.error(f"Salesforce lead creation error: {e}")
            return False

class HubSpotIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
    
    def create_contact(self, email: str, firstname: str, lastname: str) -> bool:
        """Create contact in HubSpot"""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            data = {
                'properties': [
                    {'name': 'firstname', 'value': firstname},
                    {'name': 'lastname', 'value': lastname},
                    {'name': 'email', 'value': email}
                ]
            }
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/contacts",
                json=data,
                headers=headers
            )
            logger.info(f"Contact created in HubSpot: {email}")
            return response.status_code == 201
        except Exception as e:
            logger.error(f"HubSpot contact creation error: {e}")
            return False

class PipedriveIntegration:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.pipedrive.com/v1"
    
    def create_person(self, name: str, email: str) -> bool:
        """Create person in Pipedrive"""
        try:
            params = {'api_token': self.api_token}
            data = {'name': name, 'email': [{'value': email, 'primary': True}]}
            response = requests.post(
                f"{self.base_url}/persons",
                json=data,
                params=params
            )
            logger.info(f"Person created in Pipedrive: {name}")
            return response.json().get('success', False)
        except Exception as e:
            logger.error(f"Pipedrive person creation error: {e}")
            return False
