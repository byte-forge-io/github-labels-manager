# GitHub Labels Manager

Automatically manage GitHub labels with ease.

Create, Update, and Delete your repositories 
labels via a custom yaml configuration file or URL,
and this action will take care of the rest.

This is especially useful when scaffolding
org level labels into a new repository, or
sharing a centralized label configuration
across multiple repositories.

## Features

- **Local Configuration**: Define labels in a YAML file within your repository
- **Remote Configuration**: Fetch label definitions from a centralized URL
- **Automatic Sync**: Create, update, and optionally delete labels
- **GitHub Actions Integration**: Works seamlessly as a GitHub Action

## Usage

### With Local Configuration File

```yaml
- uses: byte-forge-io/github-label-sync@v1
  with:
    yaml-path: ".github/labels.yml"  # Optional, this is the default
    prune: "true"  # Optional, delete labels not in config
```

### With Remote Configuration URL

```yaml
- uses: byte-forge-io/github-label-sync@v1
  with:
    yaml-url: "https://raw.githubusercontent.com/your-org/label-configs/main/standard-labels.yml"
    prune: "true"  # Optional, delete labels not in config
```

**Note**: When both `yaml-url` and `yaml-path` are provided, the URL takes precedence.

## Configuration Format

Your YAML configuration should be an array of label objects:

```yaml
- name: "bug"
  color: "d73a4a"
  description: "Something isn't working"

- name: "enhancement"
  color: "a2eeef" 
  description: "New feature or request"

- name: "documentation"
  color: "0075ca"
  description: "Improvements or additions to documentation"
```
