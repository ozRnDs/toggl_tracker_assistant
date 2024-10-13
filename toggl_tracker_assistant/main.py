from loguru import logger

import typer
from pydantic import BaseModel

from toggl_service import TogglAPI
from start_ui import TogglStartUI
from config_ui import TogglConfigUI
from config import AppConfig

app = typer.Typer()

app_config = AppConfig()
toggl_service = TogglAPI(api_key=app_config.TOGGL_API_KEY, workspace_id=app_config.TOGGL_WORKSPACE)

@app.command()
def start():

    projects_list = toggl_service.get_projects()
    if app_config.PROJECTS_LIST:
        projects_list = [project for project in projects_list if project.name.lower() in app_config.PROJECTS_LIST]
    
    # # Create and run the UI
    app = TogglStartUI(project_names=[project.name for project in projects_list])
    user_input = app.run()
    project_id = [project.id for project in projects_list if project.name==user_input.project][0]
    track_id = toggl_service.start_entry(description=user_input.description, project_id=project_id)
    
    logger.info(f"Started tracking a new entry: {track_id.id}. Project: {project_id}({user_input.project}). Description: {user_input.description}")

@app.command()
def stop():
    logger.info(f"Stopped a new track: {toggl_service.stop_running_entry().id}")

@app.command()
def config():
    # List of projects to populate the listbox
    projects = ["Project A", "Project B", "Project C"]

    # Create and run the UI
    app = TogglConfigUI(projects)
    app_config = app.run()
    print(f"Selected Projects: {app_config.PROJECTS_LIST}")
    print(f"Workspace ID: {app_config.TOGGL_WORKSPACE}")
    print(f"API Key: {app_config.TOGGL_API_KEY}")

if __name__ == "__main__":
    app()
