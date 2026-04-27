# mcps/supply_chain_mcp.py
from skills.sap_inventory_skill import SAPInventorySkill
from skills.whatsapp_alert_skill import WhatsAppAlertSkill

class SupplyChainMCP:
    """
    Supply Chain Orchestrator.
    Integrates SAP inventory monitoring with automated WhatsApp alerting.
    """
    META = {
        "name": "supply_chain_mcp",
        "version": "1.0.0",
        "pipeline": ["sap_inventory_skill", "whatsapp_alert_skill"]
    }

    def __init__(self):
        self.inventory = SAPInventorySkill()
        self.alert = WhatsAppAlertSkill()

    def run(self, input_data):
        # 1. Check current inventory levels
        stock = self.inventory.run({
            "sap_url": input_data["sap_url"],
            "material_id": input_data["material_id"],
            "api_key": input_data["api_key"]
        })
        
        results = {"inventory": stock, "alert_sent": False}
        
        # 2. Threshold check and alerting
        if stock["stock_qty"] < input_data.get("threshold", 100):
            msg = (f"⚠️ LOW STOCK ALERT\n"
                   f"Material: {input_data['material_id']}\n"
                   f"Qty: {stock['stock_qty']} {stock['unit']}\n"
                   f"Plant: {stock['plant']}")
                   
            alert = self.alert.run({
                "phone_number": input_data["alert_phone"],
                "message": msg,
                "wa_token": input_data["wa_token"],
                "wa_phone_id": input_data["wa_phone_id"]
            })
            
            results["alert_sent"] = True
            results["alert_id"] = alert["message_id"]
            
        return results
