from github_requests import (send_github_request, LabelAction)
from label import Label
from config_loader import load_labels_config


if __name__ == "__main__":
    """
    Manage GitHub labels automatically with ease.

    Create, Update, and Delete labels at a repository level
    using yaml file or URL to define your labels for the repository.
    """

    # Fetch current labels from the repository
    current_labels = send_github_request(LabelAction.FETCH)
    if current_labels is None:
        print("Error: Could not fetch labels from the repo")
        exit(1)
    current_label_names = {label["name"] for label in current_labels}

    # Load the new label definitions from URL or file
    try:
        new_labels = load_labels_config()
    except Exception as e:
        print(f"Error loading labels config: {e}")
        exit(1)

    # Handle the different label actions based on the new labels
    for label in new_labels:
        label = Label.from_dict(label)

        if label.name in current_label_names:
            send_github_request(LabelAction.UPDATE, label)
        else:
            send_github_request(LabelAction.CREATE, label)

    # Delete all labels which are within the current set of
    # labels, but are not within the newly defined set of labels.
    for current_label in current_labels:
        current_label = Label.from_dict(current_label)

        if current_label.name not in {l["name"] for l in new_labels}:
            send_github_request(LabelAction.DELETE, current_label)
