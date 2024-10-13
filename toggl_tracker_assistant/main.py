from loguru import logger

import typer
from pydantic import BaseModel

from toggl_service import TogglAPI
from start_ui import TogglStartUI
from config_ui import TogglConfigUI
from config import AppConfig

app = typer.Typer()

@app.command()
def start():

    projects_list = toggl_service.get_projects()
    if app_config.PROJECTS_LIST:
        projects_list = [project for project in projects_list if project.name.lower() in app_config.PROJECTS_LIST]
    
    # # Create and run the UI
    toggl_app = TogglStartUI(project_names=[project.name for project in projects_list])
    user_input = toggl_app.run()
    if user_input is None:
        logger.info("Cancel operation")
        return
    project_id = [project.id for project in projects_list if project.name==user_input.project][0]
    track_id = toggl_service.start_entry(description=user_input.description, project_id=project_id)
    
    logger.info(f"Started tracking a new entry: {track_id.id}. Project: {project_id}({user_input.project}). Description: {user_input.description}")

@app.command()
def stop():
    logger.info(f"Stopped a new track: {toggl_service.stop_running_entry().id}")

@app.command()
def config(setup:bool=False):
    # List of projects to populate the listbox
    
    projects=[]
    current_config=None
    try:
        if setup==False:
            projects = [project.name for project in toggl_service.get_projects()]
            current_config = AppConfig()
    except Exception as err:
        pass    

    # Create and run the UI
    setting_app = TogglConfigUI(projects, current_config=current_config)
    new_app_config = setting_app.run() # TODO: Add a way to refresh the projects for first configuration process
    if new_app_config is None:
        logger.info("Cancel operation")
        return
    
    new_toggl_service = TogglAPI(api_key=new_app_config.TOGGL_API_KEY, workspace_id=new_app_config.TOGGL_WORKSPACE)
    try:
        projects = [project.name for project in new_toggl_service.get_projects()]
    except Exception as err:
        raise PermissionError(f"Can't access toggl service, can't save the configuration details") from err

    new_app_config.save_to_env()
    logger.info("Updated env file")


try:
    app_config = AppConfig()
except Exception as err:
    config(setup=True)
    app_config = AppConfig()

toggl_service = TogglAPI(api_key=app_config.TOGGL_API_KEY, workspace_id=app_config.TOGGL_WORKSPACE)

if not app_config.PROJECTS_LIST:
    config()
    app_config = AppConfig()

if __name__ == "__main__":
    app()
