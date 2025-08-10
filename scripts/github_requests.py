import os
import requests
from enum import Enum
from dataclasses import asdict
from label import Label 

# Extract environment variables
TOKEN = os.environ["GH_TOKEN"]
REPO = os.environ["REPO"]

class LabelAction(Enum):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    FETCH = "Fetch"

def send_github_request(action: LabelAction, label: Label | None = None) -> dict | None:
    """Send a request to githubs repo label API."""

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    match action:
        case LabelAction.FETCH:
            return requests.get(
                f"https://api.github.com/repos/{REPO}/labels",
                headers=headers
            ).json()
        case LabelAction.CREATE:
            if label is None:
                print("Error: can't create a label when the label is null")
                return None

            print(f"Creating Label: {label.name}")
            requests.post(
                f"https://api.github.com/repos/{REPO}/labels",
                headers=headers,
                json=asdict(label)
            )
        case LabelAction.UPDATE:
            if label is None:
                print("Error: can't update a label when the label is null")
                return None

            print(f"Updating Label: {label.name}")
            requests.patch(
                f"https://api.github.com/repos/{REPO}/labels/{label.name}",
                headers=headers,
                json=asdict(label)
            )
        case LabelAction.DELETE:
            if label is None:
                print("Error: can't delete a label when the label is null")
                return None

            print(f"Deleting Label: {label.name}")
            requests.delete(
                f"https://api.github.com/repos/{REPO}/labels/{label.name}",
                headers=headers
            )




