# skills/xgboost_trainer_skill.py
import xgboost as xgb
import pandas as pd, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from skills.base_skill import BaseSkill

class XGBoostTrainerSkill(BaseSkill):
    """
    XGBoost model training skill for specialized classification tasks.
    """
    META = {
        "name": "xgboost_trainer_skill",
        "version": "1.0.0",
        "inputs": ["data", "target_col", "model_path", "params"],
        "outputs": ["f1_score", "model_path", "feature_importance"],
        "dependencies": ["xgboost", "scikit-learn", "joblib", "pandas"]
    }

    def run(self, input_data):
        df = pd.DataFrame(input_data["data"])
        X = df.drop(columns=[input_data["target_col"]])
        y = df[input_data["target_col"]]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        params = input_data.get("params", {"n_estimators": 100, "max_depth": 6})
        model = xgb.XGBClassifier(**params, eval_metric="logloss")
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        score = f1_score(y_test, preds, average="weighted")
        
        path = os.path.expanduser(input_data["model_path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(model, path)
        
        return {
            "f1_score": round(float(score), 4),
            "model_path": path,
            "feature_importance": dict(zip(X.columns, model.feature_importances_.tolist()))
        }
