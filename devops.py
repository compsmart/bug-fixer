#!/usr/bin/env python
"""
Azure DevOps Work Item API Script

This script imports bug data from bugs.json and provides it in a format similar to Azure DevOps work items.
It takes a bug ID as a parameter and returns the corresponding bug information.

Usage:
    python devops.py BUG-001

Where BUG-001 is the ID of the bug you want to retrieve.
"""

import sys
import json
import argparse
import datetime
import os
from typing import Dict, Any, Optional

# Load bugs from bugs.json


def load_bugs_from_json() -> Dict[str, Dict]:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bugs_file_path = os.path.join(script_dir, 'bugs.json')

        with open(bugs_file_path, 'r') as f:
            data = json.load(f)

        # Convert the list of bugs to a dictionary with bug ID as the key
        bugs_dict = {}
        for bug in data.get('bugs', []):
            bug_id = bug.get('id')
            if bug_id:
                bugs_dict[bug_id] = bug

        return bugs_dict
    except Exception as e:
        print(f"Error loading bugs.json: {e}")
        return {}


# Load bugs from the JSON file
BUGS = load_bugs_from_json()

# Sample work items structure to maintain compatibility with existing code
SAMPLE_WORK_ITEMS = {
    "12345": {
        "id": 12345,
        "rev": 5,
        "fields": {
            "System.Id": 12345,
            "System.Title": "Fix pagination issue on record list",
            "System.State": "Active",
            "System.CreatedDate": "2025-05-15T09:30:45.123Z",
            "System.CreatedBy": {
                "displayName": "Brad Johnson",
                "uniqueName": "brad.johnson@company.com",
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            },
            "System.AssignedTo": {
                "displayName": "Brad Johnson",
                "uniqueName": "brad.johnson@company.com",
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            },
            "System.WorkItemType": "User Story",
            "System.Description": "Users are reporting that the pagination controls don't work correctly on the record list page. When clicking to the next page, the same records are shown again.",
            "System.Tags": "Bug, Frontend, UI",
            "Microsoft.VSTS.Common.Priority": 2,
            "Microsoft.VSTS.Common.Severity": "2 - Medium",
            "Custom.Department": "Engineering",
            "Custom.EstimatedHours": 4.5
        },
        "relations": [
            {
                "rel": "System.LinkTypes.Hierarchy-Forward",
                "url": "https://dev.azure.com/organization/project/_apis/wit/workItems/12346",
                "attributes": {
                    "name": "Child"
                }
            }
        ],
        "_links": {
            "self": {
                "href": "https://dev.azure.com/organization/project/_apis/wit/workItems/12345"
            },
            "workItemUpdates": {
                "href": "https://dev.azure.com/organization/project/_apis/wit/workItems/12345/updates"
            },
            "html": {
                "href": "https://dev.azure.com/organization/project/_workitems/edit/12345"
            }
        },
        "url": "https://dev.azure.com/organization/project/_apis/wit/workItems/12345"
    },
    "54321": {
        "id": 54321,
        "rev": 3,
        "fields": {
            "System.Id": 54321,
            "System.Title": "Implement user authentication with OAuth",
            "System.State": "New",
            "System.CreatedDate": "2025-05-10T14:22:33.456Z",
            "System.CreatedBy": {
                "displayName": "Jane Smith",
                "uniqueName": "jane.smith@company.com",
                "id": "z9y8x7w6-v5u4-3210-9876-543210fedcba"
            },
            "System.AssignedTo": {
                "displayName": "Brad Johnson",
                "uniqueName": "brad.johnson@company.com",
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
            },
            "System.WorkItemType": "Feature",
            "System.Description": "Implement OAuth 2.0 authentication flow for the application to allow users to sign in with their Google, Microsoft, or Facebook accounts.",
            "System.Tags": "Security, Authentication, Backend",
            "Microsoft.VSTS.Common.Priority": 1,
            "Microsoft.VSTS.Common.Severity": "1 - Critical",
            "Custom.Department": "Security",
            "Custom.EstimatedHours": 16.0
        },
        "relations": [
            {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": "https://dev.azure.com/organization/project/_apis/wit/workItems/54310",
                "attributes": {
                    "name": "Parent"
                }
            }
        ],
        "_links": {
            "self": {
                "href": "https://dev.azure.com/organization/project/_apis/wit/workItems/54321"
            },
            "workItemUpdates": {
                "href": "https://dev.azure.com/organization/project/_apis/wit/workItems/54321/updates"
            },
            "html": {
                "href": "https://dev.azure.com/organization/project/_workitems/edit/54321"
            }
        },
        "url": "https://dev.azure.com/organization/project/_apis/wit/workItems/54321"
    }
}


def get_work_item(bug_id: str, organization: str = "organization", project: str = "project", pat: Optional[str] = None) -> Dict[str, Any]:
    """
    Get bug details converted to Azure DevOps work item format.

    Args:
        bug_id: The ID of the bug to retrieve
        organization: Azure DevOps organization name (for API URL construction)
        project: Azure DevOps project name (for API URL construction)
        pat: Personal Access Token for authentication (not used in this implementation)

    Returns:
        Dictionary containing bug details in a work item format
    """
    # Check if the bug ID exists in our loaded bugs
    if bug_id in BUGS:
        bug = BUGS[bug_id]

        # Convert bug format to match Azure DevOps work item format
        work_item = {
            "id": bug_id,
            "rev": 1,
            "fields": {
                "System.Id": bug_id,
                "System.Title": bug.get("title", "No Title"),
                "System.State": bug.get("status", "Unknown"),
                "System.CreatedDate": datetime.datetime.now().isoformat(),
                "System.CreatedBy": {
                    "displayName": "Bug Creator",
                    "uniqueName": "bug.creator@company.com",
                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
                },
                "System.AssignedTo": {
                    "displayName": bug.get("assignedTo", "Unassigned"),
                    "uniqueName": f"{bug.get('assignedTo', 'unassigned').lower().replace(' ', '.')}@company.com",
                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
                },
                "System.WorkItemType": "Bug",
                "System.Description": bug.get("description", "No description"),
                "System.Tags": bug.get("severity", "Unknown"),
                "Microsoft.VSTS.Common.Priority": _map_severity_to_priority(bug.get("severity", "Unknown")),
                "Microsoft.VSTS.Common.Severity": bug.get("severity", "Unknown"),
                "Custom.Location": bug.get("location", "Unknown"),
                "Custom.LineNumbers": bug.get("lineNumbers", []),
                "Custom.ExpectedBehavior": bug.get("expectedBehavior", "Unknown"),
                "Custom.ActualBehavior": bug.get("actualBehavior", "Unknown"),
                "Custom.Steps": bug.get("steps", []),
                "Custom.Fix": bug.get("fix", "No fix proposed")
            },
            "_links": {
                "self": {
                    "href": f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{bug_id}"
                },
                "html": {
                    "href": f"https://dev.azure.com/{organization}/{project}/_workitems/edit/{bug_id}"
                }
            },
            "url": f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{bug_id}"
        }
        return work_item
    elif bug_id in SAMPLE_WORK_ITEMS:
        # Return from the original sample work items if bug not found but ID matches
        return SAMPLE_WORK_ITEMS[bug_id]
    else:
        # Generate a fake work item if ID doesn't match any known bug or sample
        return {
            "id": bug_id,
            "rev": 1,
            "fields": {
                "System.Id": bug_id,
                "System.Title": f"Unknown bug {bug_id}",
                "System.State": "New",
                "System.CreatedDate": datetime.datetime.now().isoformat(),
                "System.CreatedBy": {
                    "displayName": "System",
                    "uniqueName": "system@company.com",
                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
                },
                "System.WorkItemType": "Bug",
                "System.Description": f"No bug found with ID {bug_id}.",
                "Microsoft.VSTS.Common.Priority": 3
            },
            "_links": {
                "self": {
                    "href": f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{bug_id}"
                }
            }
        }


def _map_severity_to_priority(severity: str) -> int:
    """Map severity string to a priority number"""
    severity_map = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }
    # Default to 3 (Medium) if severity not recognized
    return severity_map.get(severity, 3)


def main():
    """Main function to handle command-line arguments and fetch bug data."""
    parser = argparse.ArgumentParser(
        description='Retrieve bug information from bugs.json')
    parser.add_argument('bug_id', nargs='?',
                        help='ID of the bug to retrieve (e.g., BUG-001)')
    parser.add_argument('--organization', '-o', default='organization',
                        help='Azure DevOps organization name (for URL construction)')
    parser.add_argument('--project', '-p', default='project',
                        help='Azure DevOps project name (for URL construction)')
    parser.add_argument(
        '--pat', help='Personal Access Token (not used in this implementation)')
    parser.add_argument('--format', choices=['json', 'summary'], default='json',
                        help='Output format (json or summary)')
    parser.add_argument('--list', action='store_true',
                        help='List all available bugs')

    args = parser.parse_args()

    # If --list flag is provided, list all available bugs
    if args.list:
        if not BUGS:
            print("No bugs found in bugs.json")
            return

        print("\nAvailable Bugs:")
        print("-" * 80)
        for bug_id, bug in BUGS.items():
            print(f"{bug_id}: {bug.get('title', 'No Title')} - {bug.get('severity', 'Unknown')} - {bug.get('status', 'Unknown')}")
        print()
        return

    # Ensure bug_id is provided if not using --list
    if not args.bug_id:
        parser.error("bug_id is required unless --list is specified")

    # Get the bug data
    work_item = get_work_item(
        args.bug_id, args.organization, args.project, args.pat)

    # Output based on chosen format
    if args.format == 'summary':
        try:
            fields = work_item['fields']
            # Print a summary of the work item
            print(f"\nBug #{fields['System.Id']} - {fields['System.Title']}")
            print("-" * 80)
            print(f"Status:      {fields.get('System.State', 'Unknown')}")
            print(
                f"Severity:    {fields.get('Microsoft.VSTS.Common.Severity', 'Unknown')}")
            print(
                f"Assigned to: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
            print(f"Location:    {fields.get('Custom.Location', 'Unknown')}")
            if 'Custom.LineNumbers' in fields and fields['Custom.LineNumbers']:
                print(
                    f"Line(s):     {', '.join(map(str, fields['Custom.LineNumbers']))}")

            print("\nDescription:")
            print(fields.get('System.Description', 'No description'))

            if 'Custom.Steps' in fields and fields['Custom.Steps']:
                print("\nSteps to Reproduce:")
                for i, step in enumerate(fields['Custom.Steps'], 1):
                    print(f"{i}. {step}")

            print("\nExpected Behavior:")
            print(fields.get('Custom.ExpectedBehavior', 'Not specified'))

            print("\nActual Behavior:")
            print(fields.get('Custom.ActualBehavior', 'Not specified'))

            print("\nProposed Fix:")
            print(fields.get('Custom.Fix', 'No fix proposed'))

        except KeyError as e:
            print(f"Error parsing bug data: {e}")
    else:
        # Print full JSON output
        print(json.dumps(work_item, indent=2))


if __name__ == "__main__":
    main()
