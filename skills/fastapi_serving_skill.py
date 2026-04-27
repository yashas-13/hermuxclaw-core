# skills/fastapi_serving_skill.py
import subprocess, os, textwrap
from skills.base_skill import BaseSkill

class FastAPIServingSkill(BaseSkill):
    """
    Serves trained machine learning models via a FastAPI REST endpoint.
    """
    META = {
        "name": "fastapi_serving_skill",
        "version": "1.0.0",
        "inputs": ["model_path", "port", "host"],
        "outputs": ["endpoint_url", "status", "pid"],
        "dependencies": ["fastapi", "uvicorn", "joblib"]
    }

    def run(self, input_data):
        model_path = os.path.expanduser(input_data["model_path"])
        port = input_data.get("port", 8080)
        host = input_data.get("host", "0.0.0.0")
        
        # Programmatically generate the FastAPI application code
        app_code = textwrap.dedent(f"""
            from fastapi import FastAPI
            import joblib, pandas as pd
            app = FastAPI()
            model = joblib.load('{model_path}')
            @app.post("/predict")
            def predict(data: dict):
                df = pd.DataFrame([data])
                pred = model.predict(df)
                return {{"prediction": int(pred[0])}}
        """)
        
        app_file = f"/tmp/hx_serving_{port}.py"
        os.makedirs("/tmp", exist_ok=True)
        with open(app_file, "w") as f:
            f.write(app_code)
            
        # Launch the server in a separate background process
        proc = subprocess.Popen(
            ["uvicorn", f"hx_serving_{port}:app",
             "--host", host, "--port", str(port)],
            cwd="/tmp"
        )
        
        return {
            "endpoint_url": f"http://{host}:{port}/predict",
            "status": "running", 
            "pid": proc.pid
        }
