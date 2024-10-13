
import pytest
from datetime import datetime
from unittest.mock import patch, ANY
from toggl_tracker_assistant.toggl_service import TogglAPI, TimeEntryData  # Adjust this import based on your module structure

from base64 import b64encode

@pytest.fixture
def toggl_api():
    """Fixture for initializing the TogglAPI class."""
    return TogglAPI(api_key="dummy_api_key", workspace_id="123456")

def test_get_headers(toggl_api):
    """Test if the headers are generated correctly."""
    headers = toggl_api.get_headers()
    
    expected_auth = 'Basic ' + b64encode("dummy_api_key:api_token".encode()).decode("ascii")
    assert headers['Authorization'] == expected_auth
    assert headers['Content-Type'] == 'application/json'

@patch('requests.post')
def test_start_entry(mock_post, toggl_api):
    """Test the start_entry function with a mock POST request."""
    # Mock response for the POST request
    mock_response = {
        "id": 123456789,
        "description": "Test Entry",
        "duration": -1,
        "start": datetime.now().isoformat() + "Z"
    }
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response
    
    # Call the start_entry method
    result = toggl_api.start_entry(description="Test Entry")
    
    # Verify the POST request was made with correct URL and data
    mock_post.assert_called_once_with(
        "https://api.track.toggl.com/api/v9/workspaces/123456/time_entries",
        json={
            "created_with": "API example code",
            "description": "Test Entry",
            "tags": [],
            "billable": False,
            "workspace_id": 123456,
            "duration": -1,
            "start": ANY,
            "stop": None
        },
        headers=toggl_api.get_headers()
    )
    
    # Verify the response matches the mock
    assert result == mock_response

@patch('requests.get')
def test_get_current_track(mock_get, toggl_api):
    """Test the get_current_track function with a mock GET request."""
    # Mock response for the GET request

    mock_response = {"id":3638271532,
                     "workspace_id":8172681,
                     "project_id":None,
                     "task_id":None,
                     "billable":False,
                     "start":"2024-10-08T23:08:22+00:00",
                     "stop":None,
                     "duration":-1,
                     "description":"Creating Quick Toggle APP",
                     "tags":[],
                     "tag_ids":[],
                     "duronly":True,
                     "at":"2024-10-08T21:08:22+00:00",
                     "server_deleted_at":None,
                     "user_id":10527779,
                     "uid":10527779,
                     "wid":8172681,
                     "permissions":None}

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    # Call the get_current_track method
    result = toggl_api.get_current_track()
    
    # Verify the GET request was made with the correct URL
    mock_get.assert_called_once_with(
        "https://api.track.toggl.com/api/v9/me/time_entries/current",
        headers=toggl_api.get_headers()
    )
    
    # Verify the response is parsed correctly as a Pydantic model
    assert result.id == 3638271532
    assert result.description == "Creating Quick Toggle APP"
    assert result.start == datetime.fromisoformat("2024-10-08T23:08:22+00:00")

