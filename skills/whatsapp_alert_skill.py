# skills/whatsapp_alert_skill.py
import requests
from skills.base_skill import BaseSkill

class WhatsAppAlertSkill(BaseSkill):
    """
    WhatsApp Business API alert skill — sends stock/anomaly alerts to teams.
    """
    META = {
        "name": "whatsapp_alert_skill",
        "version": "1.0.0",
        "inputs": ["phone_number", "message", "wa_token", "wa_phone_id"],
        "outputs": ["message_id", "status"],
        "dependencies": ["requests"]
    }

    def run(self, input_data):
        url = f"https://graph.facebook.com/v18.0/{input_data['wa_phone_id']}/messages"
        headers = {
            "Authorization": f"Bearer {input_data['wa_token']}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": input_data["phone_number"],
            "type": "text",
            "text": {"body": input_data["message"]}
        }
        
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
        
        return {
            "message_id": r.json()["messages"][0]["id"], 
            "status": "sent"
        }
