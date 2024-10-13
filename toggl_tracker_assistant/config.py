from pydantic_settings import BaseSettings
from typing import List

class AppConfig(BaseSettings):
    TOGGL_WORKSPACE: str
    TOGGL_API_KEY: str
    PROJECTS_LIST: List[str]

    class Config:
        env_file = ".env"  # Specify the environment file to load variables from
        env_file_encoding = "utf-8"

    def save_to_env(self):
        """
        Save the current status of the object to the .env file.
        """
        env_data = []
        for field, value in self.model_dump().items():
            if isinstance(value, list):
                value = str(value).replace("'",'"')
            env_data.append(f"{field}={value}")
        
        with open(self.Config.env_file, "w", encoding=self.Config.env_file_encoding) as f:
            f.write("\n".join(env_data))