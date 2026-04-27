# tests/test_skills.py
import pytest
import os
import sys

# Ensure paths are correct
sys.path.append(os.path.expanduser("~/hermuxclaw"))

from skills.base_skill import BaseSkill
from skills.ast_extractor_skill import ASTExtractorSkill

def test_base_skill_abstract():
    """Verify that BaseSkill cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseSkill()

def test_ast_extractor_logic():
    """Test function extraction from source code."""
    extractor = ASTExtractorSkill()
    source = "def hello():\n    return 'world'"
    res = extractor.run({"source_code": source, "target_function": "hello"})
    assert "def hello():" in res["extracted_code"]
    assert "ExtractedSkill" in res["skill_template"]

# Add basic mocks for external API skills
def test_sap_inventory_import():
    from skills.sap_inventory_skill import SAPInventorySkill
    skill = SAPInventorySkill()
    assert skill.META["name"] == "sap_inventory_skill"

def test_whatsapp_alert_import():
    from skills.whatsapp_alert_skill import WhatsAppAlertSkill
    skill = WhatsAppAlertSkill()
    assert "wa_token" in skill.META["inputs"]

def test_xgboost_trainer_import():
    from skills.xgboost_trainer_skill import XGBoostTrainerSkill
    skill = XGBoostTrainerSkill()
    assert "xgboost" in skill.META["dependencies"]
