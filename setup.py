# setup.py
from setuptools import setup, find_packages

setup(
    name="hermuxclaw-pravidhi-skills",
    version="1.0.0",
    description="HermuXclaw Production Skills for ML and Supply Chain Orchestration",
    author="Pravidhi Solutions",
    packages=find_packages(),
    install_requires=[
        "requests",
        "psycopg2-binary",
        "pandas",
        "xgboost",
        "scikit-learn",
        "joblib",
        "fastapi",
        "uvicorn",
        "flask",
        "python-dotenv",
        "openai"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
