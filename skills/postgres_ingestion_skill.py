# skills/postgres_ingestion_skill.py
import psycopg2, pandas as pd
from skills.base_skill import BaseSkill

class PostgresIngestionSkill(BaseSkill):
    """
    PostgreSQL data ingestion skill for ML pipeline processing.
    """
    META = {
        "name": "postgres_ingestion_skill",
        "version": "1.0.0",
        "inputs": ["host", "port", "dbname", "user", "password", "query"],
        "outputs": ["dataframe", "row_count", "columns"],
        "dependencies": ["psycopg2-binary", "pandas"]
    }

    def run(self, input_data):
        conn = psycopg2.connect(
            host=input_data["host"], port=input_data["port"],
            dbname=input_data["dbname"], user=input_data["user"],
            password=input_data["password"]
        )
        
        df = pd.read_sql_query(input_data["query"], conn)
        conn.close()
        
        return {
            "dataframe": df.to_dict(orient="records"),
            "row_count": len(df),
            "columns": list(df.columns)
        }
