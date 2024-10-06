# Toggl Tracker Assistant

## Project Overview
Toggl Tracker Assistant is a simple Python-based tool with a minimal GUI that helps you track your tasks using a start button. The project is designed to be easy to build and run, with Docker and Python environments for development.

## Project Structure
- **.build**: Contains the build script for creating the Windows executable.
- **.devcontainer**: Docker configurations for development environments, both Linux and Windows.
- **src**: The main application source code.
- **tests**: Directory for tests.
- **pyproject.toml**: Project configuration file, managing dependencies using Poetry.
- **README.md**: This file.

## Building the Project
### Linux Development Environment
1. Open the project in VSCode.
2. Use the provided `.devcontainer` setup for a ready-made Python development environment.
3. To run the app: `poetry run python src/main.py`.

### Building the Windows Executable
1. Navigate to the `.build` directory.
2. Run the `build_exe.sh` script: `./build_exe.sh`.
3. The executable will be created in the `.build` folder.

## Testing
Tests can be added to the `tests` directory and run using your preferred test framework.
