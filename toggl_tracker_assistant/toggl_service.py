import requests
from datetime import datetime, timezone
from base64 import b64encode
from pydantic import BaseModel
from typing import Optional, List


class TimeEntryData(BaseModel):
    # Model representing the data of the current time entry
    id: int
    wid: int
    pid: Optional[int] = None
    billable: bool
    start: datetime
    duration: int
    description: Optional[str] = None
    at: str
    client_name: Optional[str] = None
    duronly: Optional[bool] = None
    permissions: Optional[List[str]] = None
    project_active: Optional[bool] = None
    project_billable: Optional[bool] = None
    project_color: Optional[str] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    shared_with: Optional[List[dict]] = None
    stop: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    task_id: Optional[int] = None
    task_name: Optional[str] = None
    tid: Optional[int] = None
    uid: Optional[int] = None
    user_avatar_url: Optional[str] = None
    user_id: int
    user_name: Optional[str] = None
    workspace_id: int

class TimeEntryCreateData(BaseModel):
    # Model representing the payload for creating a new time entry
    billable: Optional[bool] = False
    created_with: str
    description: Optional[str] = None
    duration: int
    event_metadata: Optional[dict] = None
    pid: Optional[int] = None
    project_id: Optional[int] = None
    shared_with_user_ids: Optional[List[int]] = None
    start: str
    start_date: Optional[str] = None
    stop: Optional[str] = None
    tag_action: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    task_id: Optional[int] = None
    tid: Optional[int] = None
    uid: Optional[int] = None
    user_id: Optional[int] = None
    wid: Optional[int] = None
    workspace_id: int

class ProjectUserData(BaseModel):
    """Pydantic model representing the project user data."""
    id: int
    group_id: Optional[int] = None
    gid: Optional[int] = None
    labor_cost: Optional[float] = None
    labor_cost_last_updated: Optional[str] = None
    manager: bool
    project_id: int
    rate: Optional[float] = None
    rate_last_updated: Optional[str] = None
    user_id: int
    workspace_id: int
    at: str

class RecurringParameters(BaseModel):
    """Pydantic model for project recurring parameters."""
    custom_period: Optional[int] = None
    estimated_seconds: Optional[int] = None
    parameter_end_date: Optional[str] = None
    parameter_start_date: Optional[str] = None
    period: Optional[str] = None
    project_start_date: Optional[str] = None


class CurrentPeriod(BaseModel):
    """Pydantic model for current project period (premium feature)."""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    recurring_parameters: Optional[List[RecurringParameters]] = None


class ProjectData(BaseModel):
    """Pydantic model representing the data of a project."""
    id: int
    wid: int
    workspace_id: int
    cid: Optional[int] = None
    client_id: Optional[int] = None
    name: str
    color: Optional[str] = None
    active: bool
    actual_hours: Optional[int] = None
    actual_seconds: Optional[int] = None
    auto_estimates: Optional[bool] = None
    billable: Optional[bool] = None
    can_track_time: Optional[bool] = None
    created_at: Optional[str] = None
    currency: Optional[str] = None
    current_period: Optional[CurrentPeriod] = None
    end_date: Optional[str] = None
    estimated_hours: Optional[int] = None
    estimated_seconds: Optional[int] = None
    fixed_fee: Optional[float] = None
    integration_provider: Optional[str] = None
    is_private: Optional[bool] = None
    is_shared: Optional[bool] = None
    pinned: Optional[bool] = None
    rate: Optional[float] = None
    rate_last_updated: Optional[str] = None
    recurring: Optional[bool] = None
    shared_at: Optional[str] = None
    shared_hash: Optional[str] = None
    start_date: Optional[str] = None
    status: Optional[str] = None
    template: Optional[bool] = None
    template_id: Optional[int] = None
    at: str  # Last updated timestamp



class TogglAPI:
    """Basic class to interact with Toggl API using API key and workspace ID."""
    
    def __init__(self, api_key: str, workspace_id: str):
        """
        Initialize the TogglAPI class with the API key and workspace ID.
        
        :param api_key: Your Toggl API key
        :param workspace_id: The ID of the workspace to log time entries in.
        """
        self.base_url = "https://api.track.toggl.com/api/v9"
        self.api_key = api_key
        self.workspace_id = workspace_id
        auth_string = self.api_key+":api_token"
        self.auth_header = {
            'Authorization': 'Basic %s' %  b64encode(auth_string.encode()).decode("ascii"),
            'Content-Type': 'application/json'
        }

    def get_headers(self) -> dict:
        """Return the authentication headers."""
        return self.auth_header

    def start_entry(self, description: str) -> TimeEntryData:
        """
        Start a new time entry in the workspace provided during initialization.
        The start time is set to the current datetime in ISO 8601 format.

        :param description: The description of the time entry.
        :return: The JSON response from the API.
        """
        url = f"{self.base_url}/workspaces/{self.workspace_id}/time_entries"
        current_time = datetime.now(timezone.utc).isoformat()
        payload = TimeEntryCreateData(
            created_with="toggl_service",
            description=description,
            duration=-1, # For on going time entry
            start=current_time,
            workspace_id=int(self.workspace_id)
        )
        response = requests.post(url, json=payload.dict(), headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for HTTP error codes
        return TimeEntryData(**response.json())  # Return the started entry as a Pydantic model

    def get_current_track(self) -> TimeEntryData:
        """
        Get the currently running time entry for the authenticated user.

        :return: The parsed Pydantic model with the current time entry data.
        """
        url = f"{self.base_url}/me/time_entries/current"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for HTTP error codes
        response_data = response.json()
        # If the response is None, return None
        if not response_data:
            return None
        # If there is a current time entry, return it as a Pydantic model
        return TimeEntryData(**response_data)
    
    def stop_time_entry(self, time_entry_id: int) -> TimeEntryData:
        # Stop a workspace time entry by its ID
        url = f"{self.base_url}/workspaces/{self.workspace_id}/time_entries/{time_entry_id}/stop"
        response = requests.patch(url, headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for HTTP error codes
        return TimeEntryData(**response.json())  # Return the stopped entry as a Pydantic model

    def stop_running_entry(self) -> TimeEntryData:
        # Stop the currently running time entry for the authenticated user
        current_track = self.get_current_track()
        # Raise an error if there is no running time entry
        if current_track is None or current_track.duration >= 0:
            raise ValueError("No running time entry found.")
        return self.stop_time_entry(current_track.id)  # Stop the running time entry
    
    def get_user_projects(self) -> List[ProjectUserData]:
        """
        Get the project users for the current workspace.

        :return: A list of ProjectUserData models parsed from the response.
        """
        url = f"{self.base_url}/workspaces/{self.workspace_id}/project_users"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for HTTP error codes

        # Parse the response into a list of Pydantic models
        return [ProjectUserData(**item) for item in response.json()]
    
    def get_projects(self) -> List[ProjectData]:
        """
        Get the projects for the current workspace.

        :return: A list of ProjectData models parsed from the response.
        """
        url = f"{self.base_url}/workspaces/{self.workspace_id}/projects"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()  # Raises an exception for HTTP error codes

        # Parse the response into a list of Pydantic models
        return [ProjectData(**item) for item in response.json()]

if __name__ == "__main__":
    # Example usage
    api_key = "your_api_key_here"  # Replace with your actual Toggl API key
    workspace_id = 123456  # Replace with your actual workspace ID
    description = "Hello Toggl"
    start_time = "1984-06-08T11:02:53.000Z"  # Replace with your actual start time in ISO 8601 format

    # Initialize the TogglAPI with the API key and workspace ID
    toggl_api = TogglAPI(api_key, workspace_id)

    # Start a new time entry
    try:
        time_entry_response = toggl_api.start_entry(description, start_time)
        print("Time Entry Response:", time_entry_response)
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
