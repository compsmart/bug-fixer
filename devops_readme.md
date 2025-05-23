# Azure DevOps Work Item API Script

This script mimics making API requests to Azure DevOps to retrieve work item information. It's designed to be used as a utility in Git workflows to associate commits with work items.

## Features

- Retrieve work item details by ID
- Parse and display work item information
- Support for JSON or summary output formats
- Ready to integrate with Git commit workflows

## Usage

### Basic Usage

```powershell
# Get work item details in JSON format
python devops.py 12345

# Get a readable summary of a work item
python devops.py 12345 --format summary
```

### Git Integration Example

```powershell
# Get work item title for a commit message
$workitem = "12345"
$title = python devops.py $workitem --format summary | Select-String -Pattern "Work Item #\d+ - (.+)" | ForEach-Object { $_.Matches.Groups[1].Value }
git commit -m "#$workitem $title"
```

### Advanced Options

```powershell
# Specify organization and project
python devops.py 12345 --organization yourorg --project yourproject

# Use a personal access token (PAT) for authentication
python devops.py 12345 --pat yourpersonalaccesstoken
```

## Sample Work Items

The script includes sample data for two work items:

1. **Work Item #12345**: "Fix pagination issue on record list"
2. **Work Item #54321**: "Implement user authentication with OAuth"

For any other ID, the script will generate a sample work item with that ID.

## Real API Integration

The script includes commented code that shows how to make real API calls to Azure DevOps. To use it:

1. Set the conditional `if False:` to `if True:` in the `get_work_item()` function
2. Provide a valid Personal Access Token (PAT) with the `--pat` argument
3. Specify your organization and project names

## Requirements

- Python 3.6+
- `requests` library (for real API calls)

## Installation

```powershell
# Install required packages
pip install requests
```
