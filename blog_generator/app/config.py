from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    groq_key: str
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
