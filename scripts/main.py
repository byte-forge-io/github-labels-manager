import yaml
from github_requests import (send_github_request, LabelAction)
from label import Label


if __name__ == "__main__":
    """
    Manage GitHub labels automatically with ease.

    Create, Update, and Delete labels at a repository level
    using yaml file to define your labels for the repository.
    """

    # Fetch current labels from the repository
    current_labels = send_github_request(LabelAction.FETCH)
    if current_labels is None:
        print("Error: Could not fetch labels from the repo")
        exit(1)
    current_label_names = {label["name"] for label in current_labels}

    # Read the new label definitions yaml file that was just updated
    with open(".github/labels.yml", "r") as f:
        new_labels = yaml.safe_load(f)

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
