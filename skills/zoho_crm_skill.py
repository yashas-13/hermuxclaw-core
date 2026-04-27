# skills/zoho_crm_skill.py
import requests
from skills.base_skill import BaseSkill

class ZohoCRMSkill(BaseSkill):
    """
    Zoho CRM integration skill for lead management and automated follow-ups.
    """
    META = {
        "name": "zoho_crm_skill",
        "version": "1.0.0",
        "inputs": ["action", "access_token", "payload"],
        "outputs": ["record_id", "status", "data"],
        "dependencies": ["requests"]
    }
    BASE = "https://www.zohoapis.in/crm/v3"

    def run(self, input_data):
        headers = {
            "Authorization": f"Zoho-oauthtoken {input_data['access_token']}",
            "Content-Type": "application/json"
        }
        action = input_data["action"]
        
        if action == "create_lead":
            r = requests.post(
                f"{self.BASE}/Leads",
                json={"data": [input_data["payload"]]}, 
                headers=headers
            )
            r.raise_for_status()
            data = r.json()
            return {
                "record_id": data["data"][0]["details"]["id"],
                "status": "created", 
                "data": data
            }
        elif action == "get_leads":
            r = requests.get(f"{self.BASE}/Leads", headers=headers)
            r.raise_for_status()
            return {
                "record_id": None, 
                "status": "fetched", 
                "data": r.json()
            }
            
        raise ValueError(f"Unknown action: {action}")
