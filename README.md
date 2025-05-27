# Bug Fixer Project

This is a simple Task Manager web application intentionally created with bugs for educational purposes. The application includes several common programming errors and implementation issues that need to be fixed.

The workflow and setup for the GITHUB copilot agent can be seen here.
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/cb48g2gcD6M/0.jpg)](https://www.youtube.com/watch?v=cb48g2gcD6M)

## Project Structure

- `index.html` - Main HTML file
- `static/styles.css` - CSS styles for the application
- `static/app.js` - JavaScript code with intentional bugs
- `bugs.json` - Documentation of all known bugs in the application

## Task Manager Features

- Add new tasks
- Mark tasks as completed
- Delete tasks
- Filter tasks (All, Active, Completed)
- Count of remaining tasks

## Bug Challenge

This project is intended as a learning exercise. The challenge is to:

1. Identify and understand each bug documented in the `bugs.json` file
2. Fix the bugs one by one
3. Test your fixes to ensure they work properly
4. Document your process and solutions

## How to Run the Application

1. Clone the repository
2. Open `index.html` in your browser
3. Start identifying and fixing the bugs!

## Running the Web Server

The project includes a simple Python web server that can be used to serve the application:

```bash
# Start the web server
python server.py

# Access the application
# Open your browser and go to: http://localhost:8000
```

You can also use the VS Code task we've created:

1. Press `Ctrl+Shift+P` to open the command palette
2. Type "Tasks: Run Task" and select it
3. Choose the "Start Web Server" task

This will start the Python server in the background, and you can access the application at http://localhost:8000.

## Learning Objectives

- Understand common JavaScript bugs
- Practice debugging skills
- Learn about web storage, event handling, and DOM manipulation
- Experience the software development lifecycle, including bug tracking and fixing

## Tools

### DevOps Bug Viewer

The `devops.py` script allows you to view bug information in an Azure DevOps-style format:

```bash
# List all bugs
python devops.py --list

# View a specific bug with details
python devops.py BUG-001 --format summary

# Get JSON representation of a bug
python devops.py BUG-001
```

### GitHub Issue Creator

The `github_issues.py` script converts bugs from `bugs.json` to GitHub issues:

```bash
# Prerequisites
pip install requests python-dotenv

# Using environment variables (.env file)
# Create a .env file with:
# GITHUB_TOKEN=your_github_personal_access_token
# GITHUB_REPO=https://github.com/username/repository.git

# Create GitHub issues from all bugs (using .env file)
python github_issues.py

# Create GitHub issues with explicit parameters
python github_issues.py --repo username/repository --token YOUR_GITHUB_TOKEN

# Preview without creating (dry run)
python github_issues.py --dry-run

# Create issues for specific bugs only
python github_issues.py --ids BUG-001 BUG-002
```

Note: You'll need to create a [GitHub Personal Access Token](https://github.com/settings/tokens) with the `repo` scope to use this script.

Good luck with the bug fixing challenge!
