# mcps/ml_pipeline_mcp.py
from skills.postgres_ingestion_skill import PostgresIngestionSkill
from skills.xgboost_trainer_skill import XGBoostTrainerSkill
from skills.fastapi_serving_skill import FastAPIServingSkill

class MLPipelineMCP:
    """
    End-to-End Machine Learning Orchestrator.
    Automates: Data Ingestion -> Model Training -> Real-time Serving.
    """
    META = {
        "name": "ml_pipeline_mcp",
        "version": "1.0.0",
        "pipeline": ["postgres_ingestion_skill", "xgboost_trainer_skill", "fastapi_serving_skill"]
    }

    def __init__(self):
        self.ingest = PostgresIngestionSkill()
        self.train = XGBoostTrainerSkill()
        self.serve = FastAPIServingSkill()

    def run(self, input_data):
        # 1. Ingest Data from PostgreSQL
        data = self.ingest.run(input_data["db_config"])
        
        # 2. Train Model with XGBoost
        train_result = self.train.run({
            "data": data["dataframe"],
            "target_col": input_data["target_col"],
            "model_path": input_data["model_path"],
            "params": input_data.get("params", {})
        })
        
        # 3. Serve Model via FastAPI
        serve_result = self.serve.run({
            "model_path": train_result["model_path"],
            "port": input_data.get("serve_port", 8080)
        })
        
        return {
            "pipeline": "complete",
            "f1_score": train_result["f1_score"],
            "endpoint": serve_result["endpoint_url"],
            "feature_importance": train_result["feature_importance"]
        }
