#!/usr/bin/env python
"""
Azure DevOps Work Item API Script

This script mimics making an API request to Azure DevOps to retrieve work item information.
It takes a work item ID as a parameter and returns a sample JSON response.

Usage:
    python devops.py 12345

Where 12345 is the ID of the work item you want to retrieve.
"""

import sys
import json
import argparse
import datetime
from typing import Dict, Any, Optional

# Sample work items to mimic API response
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

def get_work_item(work_item_id: str, organization: str = "organization", project: str = "project", pat: Optional[str] = None) -> Dict[str, Any]:
    """
    Get work item details from Azure DevOps.
    
    Args:
        work_item_id: The ID of the work item to retrieve
        organization: Azure DevOps organization name
        project: Azure DevOps project name
        pat: Personal Access Token for authentication
        
    Returns:
        Dictionary containing work item details
    """
    # In a real implementation, this would make an actual API call to Azure DevOps
    # For demonstration purposes, we'll return sample data instead
    
    # This is how you would make an actual API call (using the requests library):
    # url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
    # headers = {"Content-Type": "application/json"}
    # auth = (username, pat)  # PAT is used as password with empty username
    # response = requests.get(url, headers=headers, auth=auth)
    # return response.json() if response.status_code == 200 else {"error": f"Failed: {response.status_code}"}
    
    # Instead, return simulated data
    if work_item_id in SAMPLE_WORK_ITEMS:
        return SAMPLE_WORK_ITEMS[work_item_id]
    else:
        # Generate a fake work item if ID doesn't match samples
        return {
            "id": int(work_item_id),
            "rev": 1,
            "fields": {
                "System.Id": int(work_item_id),
                "System.Title": f"Sample work item {work_item_id}",
                "System.State": "New",
                "System.CreatedDate": datetime.datetime.now().isoformat(),
                "System.CreatedBy": {
                    "displayName": "Brad Johnson",
                    "uniqueName": "brad.johnson@company.com",
                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
                },
                "System.WorkItemType": "Task",
                "System.Description": f"This is a generated sample work item with ID {work_item_id}.",
                "Microsoft.VSTS.Common.Priority": 3
            },
            "_links": {
                "self": {
                    "href": f"https://dev.azure.com/organization/project/_apis/wit/workItems/{work_item_id}"
                }
            }
        }

def main():
    """Main function to handle command-line arguments and fetch work item data."""
    parser = argparse.ArgumentParser(description='Retrieve work item information from Azure DevOps')
    parser.add_argument('work_item_id', help='ID of the work item to retrieve')
    parser.add_argument('--organization', '-o', default='organization', 
                        help='Azure DevOps organization name')
    parser.add_argument('--project', '-p', default='project', 
                        help='Azure DevOps project name')
    parser.add_argument('--pat', help='Personal Access Token for Azure DevOps authentication')
    parser.add_argument('--format', choices=['json', 'summary'], default='json',
                        help='Output format (json or summary)')
    
    args = parser.parse_args()
    
    # Get the work item data
    work_item = get_work_item(args.work_item_id, args.organization, args.project, args.pat)
    
    # Output based on chosen format
    if args.format == 'summary':
        try:
            # Print a summary of the work item
            print(f"\nWork Item #{work_item['id']} - {work_item['fields']['System.Title']}")
            print("-" * 80)
            print(f"Type:        {work_item['fields'].get('System.WorkItemType', 'Unknown')}")
            print(f"State:       {work_item['fields'].get('System.State', 'Unknown')}")
            print(f"Assigned to: {work_item['fields'].get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
            print(f"Priority:    {work_item['fields'].get('Microsoft.VSTS.Common.Priority', 'Not set')}")
            print(f"Created:     {work_item['fields'].get('System.CreatedDate', 'Unknown')}")
            print("\nDescription:")
            print(work_item['fields'].get('System.Description', 'No description'))
        except KeyError as e:
            print(f"Error parsing work item data: {e}")
    else:
        # Print full JSON output
        print(json.dumps(work_item, indent=2))

if __name__ == "__main__":
    main()
