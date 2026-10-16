from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EquipTrack API"
    database_url: str = "postgresql+psycopg://EquipTrack:EquipTrack@localhost:5432/EquipTrack"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
