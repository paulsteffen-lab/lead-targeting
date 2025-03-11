from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    data_url: str = (
        "https://github.com/navid-aub/LinkedIn-Dataset/raw/main/LinkedIn_Dataset.pcl"
    )
    data_filename: str = "LinkedIn_Dataset.pcl"
    data_path: Path = Path("data")
    structured_db_url: str = "sqlite:///data/database.db"
    vector_db_path: Path = Path("data/vector_db")
    model_name: str = "all-MiniLM-L6-v2"


settings = Settings()
