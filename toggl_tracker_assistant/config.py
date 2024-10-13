from pydantic_settings import BaseSettings
from typing import List

class AppConfig(BaseSettings):
    TOGGL_WORKSPACE: str
    TOGGL_API_KEY: str
    PROJECTS_LIST: List[str]

    class Config:
        env_file = ".env"  # Specify the environment file to load variables from
        env_file_encoding = "utf-8"