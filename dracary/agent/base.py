from openai import OpenAI
from dracary.tools.toolkit import Toolkit
from dracary.config.load import ConfigLoader


class BaseAgent:
    """Base Agent Class: Includes common configuration and tool initialization"""

    def __init__(self):
        # Initialize the configuration loader
        config_loader = ConfigLoader()
        
        self.type = config_loader.get("llm.type")
        # Retrieve API Key and Base URL
        self.api_key = config_loader.get("openai.api_key")
        self.base_url = config_loader.get("openai.base_url")

        # Retrieve LiteLLM configuration
        self.litellm_key = config_loader.get("litellm.key")
        self.litellm_model = config_loader.get("litellm.model")
        
        # Initialize the DeepSeek client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        # Initialize the Toolkit
        self.toolkit = Toolkit()
        self.tools = self.toolkit.get_tools()
        self.available_functions = self.toolkit.available_functions