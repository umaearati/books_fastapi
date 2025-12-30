# config is used to use .env variable    
# pip install pydantic-settings - to handle .env 
#  SettingsConfigDict is used to direct the path of .env file
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_case_sensitive=False  # allows DATABASE_URL → database_url
    )
    
# go to python3   
# from src.config import Settings

# s = Settings()
# s.database_url OR s.DATABASE_URL       
        
config = Settings() 