# mcps/crm_automation_mcp.py
from skills.zoho_crm_skill import ZohoCRMSkill
from skills.whatsapp_alert_skill import WhatsAppAlertSkill

class CRMAutomationMCP:
    """
    CRM + Messaging Orchestrator.
    Automates: Lead Creation -> Sales Notification via WhatsApp.
    """
    META = {
        "name": "crm_automation_mcp",
        "version": "1.0.0",
        "pipeline": ["zoho_crm_skill", "whatsapp_alert_skill"]
    }

    def __init__(self):
        self.crm = ZohoCRMSkill()
        self.alert = WhatsAppAlertSkill()

    def run(self, input_data):
        # 1. Create Lead in Zoho CRM
        result = self.crm.run({
            "action": "create_lead",
            "access_token": input_data["zoho_token"],
            "payload": input_data["lead_data"]
        })
        
        # 2. Notify Sales Team
        msg = (f"🎯 New Lead Created\n"
               f"Name: {input_data['lead_data'].get('Last_Name')}\n"
               f"Company: {input_data['lead_data'].get('Company')}\n"
               f"CRM ID: {result['record_id']}")
               
        self.alert.run({
            "phone_number": input_data["sales_phone"],
            "message": msg,
            "wa_token": input_data["wa_token"],
            "wa_phone_id": input_data["wa_phone_id"]
        })
        
        return {"lead_id": result["record_id"], "notified": True}
