from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Prompt-Studio"
    DATABASE_URL : str
    GROQ_API_KEY :str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()