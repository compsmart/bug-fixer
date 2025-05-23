#!/usr/bin/env python
"""
Simple script to verify that bugs.json can be properly loaded and processed
"""

import json
import os
import sys


def load_bugs_from_json():
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


def main():
    bugs = load_bugs_from_json()
    if not bugs:
        print("No bugs found in bugs.json")
        return

    print(f"Successfully loaded {len(bugs)} bugs from bugs.json")
    for bug in bugs:
        print(f"- {bug.get('id')}: {bug.get('title')} ({bug.get('severity')})")


if __name__ == "__main__":
    main()
