# skills/model_drift_monitor_skill.py
import joblib, pandas as pd, os
from sklearn.metrics import f1_score
from skills.base_skill import BaseSkill

class ModelDriftMonitorSkill(BaseSkill):
    """
    ML Model Maintenance Skill.
    Detects accuracy drift in deployed models and recommends retraining cycles.
    """
    META = {
        "name": "model_drift_monitor_skill",
        "version": "1.0.0",
        "inputs": ["model_path", "new_data", "target_col", "threshold"],
        "outputs": ["current_f1", "drift_detected", "retrain_recommended"],
        "dependencies": ["joblib", "scikit-learn", "pandas"]
    }

    def run(self, input_data):
        model_path = os.path.expanduser(input_data["model_path"])
        
        # 1. Load the active model
        model = joblib.load(model_path)
        
        # 2. Prepare verification data
        df = pd.DataFrame(input_data["new_data"])
        X = df.drop(columns=[input_data["target_col"]])
        y = df[input_data["target_col"]]
        
        # 3. Calculate current performance
        preds = model.predict(X)
        current_f1 = round(f1_score(y, preds, average="weighted"), 4)
        
        # 4. Detect Drift
        threshold = input_data.get("threshold", 0.85)
        drift = current_f1 < threshold
        
        return {
            "current_f1": float(current_f1),
            "drift_detected": bool(drift),
            "retrain_recommended": bool(drift)
        }
