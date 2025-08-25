import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from config_loader import (
    is_valid_url, 
    load_config_from_url, 
    load_config_from_file, 
    load_labels_config
)


class TestConfigLoader(unittest.TestCase):

    def test_is_valid_url_valid_urls(self):
        """Test that valid URLs return True."""
        valid_urls = [
            "https://example.com/labels.yml",
            "http://github.com/repo/labels.yaml",
            "https://raw.githubusercontent.com/user/repo/main/labels.yml"
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_url(url))

    def test_is_valid_url_invalid_urls(self):
        """Test that invalid URLs return False."""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            "//example.com",
            "example.com/path"
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_url(url))

    @patch('config_loader.requests.get')
    def test_load_config_from_url_success(self, mock_get):
        """Test successful URL config loading."""
        mock_response = MagicMock()
        mock_response.text = "- name: bug\n  color: d73a4a\n  description: Something isn't working"
        mock_get.return_value = mock_response
        
        result = load_config_from_url("https://example.com/labels.yml")
        
        expected = [{"name": "bug", "color": "d73a4a", "description": "Something isn't working"}]
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with("https://example.com/labels.yml", timeout=30)

    @patch('config_loader.requests.get')
    def test_load_config_from_url_invalid_url(self, mock_get):
        """Test loading config from invalid URL raises ValueError."""
        with self.assertRaises(ValueError):
            load_config_from_url("not-a-url")

    @patch('config_loader.requests.get')
    def test_load_config_from_url_request_error(self, mock_get):
        """Test loading config handles request errors."""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        with self.assertRaises(RuntimeError):
            load_config_from_url("https://example.com/labels.yml")

    def test_load_config_from_file_success(self):
        """Test successful file config loading."""
        yaml_content = "- name: bug\n  color: d73a4a\n  description: Something isn't working"
        
        with patch('builtins.open', mock_open(read_data=yaml_content)):
            result = load_config_from_file("labels.yml")
        
        expected = [{"name": "bug", "color": "d73a4a", "description": "Something isn't working"}]
        self.assertEqual(result, expected)

    def test_load_config_from_file_not_found(self):
        """Test loading config from non-existent file raises FileNotFoundError."""
        with patch('builtins.open', side_effect=FileNotFoundError()):
            with self.assertRaises(FileNotFoundError):
                load_config_from_file("nonexistent.yml")

    @patch.dict(os.environ, {"YAML_URL": "https://example.com/labels.yml"})
    @patch('config_loader.load_config_from_url')
    def test_load_labels_config_from_url(self, mock_load_url):
        """Test that load_labels_config prefers URL when available."""
        mock_load_url.return_value = [{"name": "test"}]
        
        result = load_labels_config()
        
        mock_load_url.assert_called_once_with("https://example.com/labels.yml")
        self.assertEqual(result, [{"name": "test"}])

    @patch.dict(os.environ, {"YAML_FILE": "custom/labels.yml"}, clear=True)
    @patch('config_loader.load_config_from_file')
    def test_load_labels_config_from_file(self, mock_load_file):
        """Test that load_labels_config falls back to file when no URL."""
        mock_load_file.return_value = [{"name": "test"}]
        
        result = load_labels_config()
        
        mock_load_file.assert_called_once_with("custom/labels.yml")
        self.assertEqual(result, [{"name": "test"}])

    @patch.dict(os.environ, {}, clear=True)
    @patch('config_loader.load_config_from_file')
    def test_load_labels_config_default_file(self, mock_load_file):
        """Test that load_labels_config uses default file path."""
        mock_load_file.return_value = [{"name": "test"}]
        
        result = load_labels_config()
        
        mock_load_file.assert_called_once_with(".github/labels.yml")
        self.assertEqual(result, [{"name": "test"}])


if __name__ == '__main__':
    unittest.main()
