#!/usr/bin/env python
"""
GitHub Issue Creator

This script converts bugs from bugs.json to GitHub issues and sends them to a GitHub repository.
It reads GitHub token and repository URL from the .env file.

Usage:
    python github_issues.py [--dry-run] [--ids BUG-001 BUG-002 ...]

Requirements:
    - requests library: pip install requests
    - python-dotenv library: pip install python-dotenv
"""

import json
import os
import argparse
import sys
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

# Check if required libraries are installed
missing_libs = []
try:
    import requests
except ImportError:
    missing_libs.append("requests")

try:
    import dotenv
except ImportError:
    missing_libs.append("python-dotenv")

if missing_libs:
    print(
        f"Error: The following libraries are required but not installed: {', '.join(missing_libs)}")
    print("Please install required libraries using:")
    print(f"  pip install {' '.join(missing_libs)}")
    sys.exit(1)


def load_bugs_from_json() -> List[Dict[str, Any]]:
    """Load bugs from bugs.json file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bugs_file_path = os.path.join(script_dir, 'bugs.json')

        with open(bugs_file_path, 'r') as f:
            data = json.load(f)

        return data.get('bugs', [])
    except Exception as e:
        print(f"Error loading bugs.json: {e}")
        return []


def convert_bug_to_github_issue(bug: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a bug from bugs.json format to GitHub issue format."""
    # Create labels from severity and status
    labels = [bug.get('severity', ''), bug.get('status', '')]
    labels = [label for label in labels if label]  # Remove empty labels

    # Format the location and line numbers
    location = f"{bug.get('location', 'Unknown')}"
    if 'lineNumbers' in bug and bug['lineNumbers']:
        line_str = ', '.join(map(str, bug['lineNumbers']))
        location += f" (Lines: {line_str})"

    # Format steps to reproduce
    steps_to_reproduce = ""
    if 'steps' in bug and bug['steps']:
        steps_to_reproduce = "\n### Steps to Reproduce\n"
        for i, step in enumerate(bug['steps'], 1):
            steps_to_reproduce += f"{i}. {step}\n"

    # Create the issue body
    body = f"""## Bug Description
{bug.get('description', 'No description provided')}

### Location
{location}

{steps_to_reproduce}
### Expected Behavior
{bug.get('expectedBehavior', 'Not specified')}

### Actual Behavior
{bug.get('actualBehavior', 'Not specified')}

### Proposed Fix
{bug.get('fix', 'No fix proposed')}

### Assigned To
{bug.get('assignedTo', 'Unassigned')}
"""

    # Create the GitHub issue object
    issue = {
        "title": f"{bug.get('id', 'BUG')}: {bug.get('title', 'Untitled Bug')}",
        "body": body,
        "labels": labels
    }

    return issue


def create_github_issue(repo: str, token: str, issue_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a GitHub issue with the provided data."""
    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.post(url, json=issue_data, headers=headers)

    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error creating issue: {response.status_code}")
        print(response.text)
        return {}


def create_github_labels(repo: str, token: str, bugs: List[Dict[str, Any]]) -> None:
    """Create GitHub labels for bug severities and statuses if they don't exist."""
    # Extract unique labels from bugs
    labels = set()
    for bug in bugs:
        if 'severity' in bug and bug['severity']:
            labels.add(bug['severity'])
        if 'status' in bug and bug['status']:
            labels.add(bug['status'])

    # Define label colors
    label_colors = {
        "Critical": "ff0000",  # Red
        "High": "d93f0b",      # Dark Orange
        "Medium": "fbca04",    # Yellow
        "Low": "0e8a16",       # Green
        "Open": "c2e0c6",      # Light Green
        "In Progress": "0052cc",  # Blue
        "Resolved": "5319e7",  # Purple
        "Closed": "bfdadc"     # Gray
    }

    # Create labels in the repository
    url = f"https://api.github.com/repos/{repo}/labels"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get existing labels
    response = requests.get(url, headers=headers)
    existing_labels = set()
    if response.status_code == 200:
        existing_labels = {label['name'] for label in response.json()}

    # Create new labels as needed
    for label in labels:
        if label not in existing_labels:
            # Default color if not defined
            color = label_colors.get(label, "cccccc")
            data = {
                "name": label,
                "color": color,
                "description": f"Bug {label.lower()} level"
            }

            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                print(f"Created label: {label}")
            else:
                print(
                    f"Error creating label '{label}': {response.status_code}")
                print(response.text)


def load_env_variables():
    """Load environment variables from .env file and extract GitHub repository information."""
    # Load .env file
    dotenv.load_dotenv()

    # Get GitHub token and repository URL
    token = os.getenv("GITHUB_TOKEN")
    repo_url = os.getenv("GITHUB_REPO")

    if not token:
        print("Error: GITHUB_TOKEN not found in .env file")
        return None, None

    if not repo_url:
        print("Error: GITHUB_REPO not found in .env file")
        return None, None

    # Extract owner/repo from the GitHub repository URL
    # Expected format: https://github.com/owner/repo.git
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')

    if len(path_parts) < 2:
        print(f"Error: Invalid GitHub repository URL format: {repo_url}")
        print("Expected format: https://github.com/owner/repo.git")
        return None, None

    owner = path_parts[0]
    repo = path_parts[1]

    # Remove .git extension if present
    if repo.endswith('.git'):
        repo = repo[:-4]

    return token, f"{owner}/{repo}"


def main():
    parser = argparse.ArgumentParser(
        description='Convert bugs to GitHub issues')
    parser.add_argument('--repo',
                        help='GitHub repository in the format owner/repo (overrides .env)')
    parser.add_argument('--token',
                        help='GitHub personal access token (overrides .env)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show issues that would be created without actually creating them')
    parser.add_argument('--ids', nargs='+',
                        help='Specific bug IDs to convert (default: all bugs)')

    args = parser.parse_args()

    # Load GitHub token and repository from .env if not provided as arguments
    if not args.token or not args.repo:
        env_token, env_repo = load_env_variables()
        if not args.token:
            args.token = env_token
        if not args.repo:
            args.repo = env_repo

    # Validate GitHub token and repository
    if not args.token:
        print("Error: GitHub token not provided. Use --token option or set GITHUB_TOKEN in .env file.")
        return

    if not args.repo:
        print("Error: GitHub repository not provided. Use --repo option or set GITHUB_REPO in .env file.")
        return

    # Load bugs from JSON file
    bugs = load_bugs_from_json()
    if not bugs:
        print("No bugs found in bugs.json")
        return

    # Filter bugs by ID if specified
    if args.ids:
        bugs = [bug for bug in bugs if bug.get('id') in args.ids]
        if not bugs:
            print(
                f"No bugs found with the specified IDs: {', '.join(args.ids)}")
            return

    # Create labels in GitHub repository
    if not args.dry_run:
        print(f"Creating labels in {args.repo}...")
        create_github_labels(args.repo, args.token, bugs)

    # Convert bugs to GitHub issues and create them
    print(f"\nConverting {len(bugs)} bugs to GitHub issues...")
    for bug in bugs:
        issue_data = convert_bug_to_github_issue(bug)

        if args.dry_run:
            print(f"\n{'-' * 80}")
            print(f"Would create issue: {issue_data['title']}")
            print(f"Labels: {', '.join(issue_data['labels'])}")
            print(f"\nBody:\n{issue_data['body']}")
        else:
            print(f"Creating issue for {bug.get('id')}: {bug.get('title')}")
            result = create_github_issue(args.repo, args.token, issue_data)
            if result:
                print(f"  Created: {result.get('html_url')}")

    if args.dry_run:
        print(f"\n{'-' * 80}")
        print("DRY RUN - No issues were actually created")
    else:
        print("\nAll bugs have been converted to GitHub issues.")


if __name__ == "__main__":
    main()
