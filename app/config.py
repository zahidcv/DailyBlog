from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str 
    secret_key: str 
    algorithm :str
    access_token_expiration_minutes: int

    class config():
        env_file = ".env"
    
settings = Settings()

print("****************from config.py *************", settings.database_hostname)
    