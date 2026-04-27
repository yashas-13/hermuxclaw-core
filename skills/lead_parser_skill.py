# skills/lead_parser_skill.py
import re
from skills.base_skill import BaseSkill

class LeadParserSkill(BaseSkill):
    """
    Deterministic HTML/Text Parser for Lead Extraction.
    Identifies patterns in raw browser output to isolate business entities.
    """
    META = {
        "name": "lead_parser_skill",
        "version": "1.0.0",
        "inputs": ["raw_data", "target_services"],
        "outputs": ["structured_leads"],
        "dependencies": []
    }

    def run(self, input_data):
        raw_text = input_data.get("raw_data", "")
        targets = input_data.get("target_services", ["Digital Twin", "ML", "SAP"])
        
        print(f"[*] LeadParser: Analyzing {len(raw_text)} bytes of raw data...")
        
        leads = []
        # Pattern: Look for capitalized names near service keywords
        for service in targets:
            # Simple regex search for demonstration; in production uses AST/LLM parsing
            matches = re.finditer(rf"([A-Z][\w\s]+)\s.*({service})", raw_text)
            for match in matches:
                leads.append({
                    "company": match.group(1).strip(),
                    "service_match": match.group(2),
                    "confidence": 0.85
                })
        
        # Deduplicate and sort
        unique_leads = {v['company']: v for v in leads}.values()
        sorted_leads = sorted(unique_leads, key=lambda x: x['company'])
        
        return {
            "status": "success",
            "structured_leads": list(sorted_leads),
            "count": len(sorted_leads)
        }

if __name__ == "__main__":
    parser = LeadParserSkill()
    test_data = "Reliance Industries is looking for Digital Twin solutions. Tata Group needs ML Automation."
    print(parser.run({"raw_data": test_data}))
