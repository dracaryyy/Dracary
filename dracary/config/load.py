import tomllib
import os
from typing import Dict, Any


class ConfigLoader:
    """Configuration Loader: Responsible for loading and providing configuration"""

    def __init__(self, file_name: str = "dracary\\config\\config.toml"):
        """
        Initialize the configuration loader.
        Args:
            file_name (str): The relative path to the configuration file.
        """
        self.file_name = file_name
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load the .toml configuration file."""
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(project_root, self.file_name)

        with open(file_path, "rb") as f:
            return tomllib.load(f)

    def get(self, key: str, default=None) -> Any:
        """
        Retrieve a configuration item.
        Args:
            key (str): The key of the configuration item, supports nested keys (e.g., "openai.api_key").
            default (Any): The default value to return if the key does not exist.
        Returns:
            Any: The value of the configuration item.
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                break
        return value