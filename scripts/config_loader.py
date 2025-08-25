import os
import yaml
import requests
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Check if the given string is a valid HTTP/HTTPS URL."""
    try:
        result = urlparse(url)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except Exception:
        return False


def load_config_from_url(url: str) -> dict:
    """Load YAML configuration from a URL."""
    if not is_valid_url(url):
        raise ValueError(f"Invalid URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return yaml.safe_load(response.text)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch config from URL {url}: {e}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML from URL {url}: {e}")


def load_config_from_file(file_path: str) -> dict:
    """Load YAML configuration from a local file."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {file_path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML from file {file_path}: {e}")


def load_labels_config() -> dict:
    """Load labels configuration from URL or local file based on environment variables."""
    yaml_url = os.environ.get("YAML_URL")
    yaml_file = os.environ.get("YAML_FILE", ".github/labels.yml")
    
    if yaml_url:
        print(f"Loading labels config from URL: {yaml_url}")
        return load_config_from_url(yaml_url)
    else:
        print(f"Loading labels config from file: {yaml_file}")
        return load_config_from_file(yaml_file)
