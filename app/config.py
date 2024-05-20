from pydantic_settings import BaseSettings
from pydantic import Field, validator, ValidationError

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
    
    @validator('access_token_expiration_minutes', pre=True)
    def validate_access_token_expiration_minutes(cls, value):
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ValidationError("access_token_expiration_minutes must be an integer")
        return value
    
settings = Settings()

print("****************from config.py *************", settings.database_hostname)
    