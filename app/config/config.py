from typing import Optional, Literal

from beanie import init_beanie

from pydantic_settings import BaseSettings
import app.models as models

class Settings(BaseSettings):
    #LOG_LEVEL: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"]
    # database configurations
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        from_attributes = True


async def initiate_database(client):
    await init_beanie(
        database=client.basketse, document_models=models.__all__
    )