# skills/sap_inventory_skill.py
import requests
from skills.base_skill import BaseSkill

class SAPInventorySkill(BaseSkill):
    """
    SAP inventory monitoring skill for supply chain visibility.
    """
    META = {
        "name": "sap_inventory_skill",
        "version": "1.0.0",
        "inputs": ["sap_url", "material_id", "api_key"],
        "outputs": ["stock_qty", "unit", "plant", "last_updated"],
        "dependencies": ["requests"]
    }

    def run(self, input_data):
        url = f"{input_data['sap_url']}/api/v1/stock/{input_data['material_id']}"
        headers = {"Authorization": f"Bearer {input_data['api_key']}"}
        
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        return {
            "stock_qty": data.get("quantity", 0),
            "unit": data.get("unit", "EA"),
            "plant": data.get("plant", ""),
            "last_updated": data.get("timestamp", "")
        }
