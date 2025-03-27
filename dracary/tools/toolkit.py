from dracary.tools.file_saver import File_Saver
from dracary.tools.python_excutor import python_executor
from dracary.tools.search import baidu_search


class Toolkit:
    """Toolkit class: Encapsulates tool configurations and available function mappings"""

    def __init__(self):
        # Tool configurations
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "file_saver",
                    "description": "Save content to a local file at a specified path.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "(required) The content to save to the file.",
                            },
                            "file_path": {
                                "type": "string",
                                "description": "(required) The path where the file should be saved, including filename and extension.",
                            },
                            "mode": {
                                "type": "string",
                                "description": "(optional) The file opening mode. Default is 'w' for write. Use 'a' for append.",
                                "enum": ["w", "a"],
                                "default": "w",
                            },
                        },
                        "required": ["content", "file_path"],
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "python_executor",
                    "description": "Execute a piece of Python code and return the output.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The Python code to execute, which must be a safe expression or computation logic."
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "baidu_search",
                    "description": "Perform a search using Baidu and retrieve results.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search keyword.",
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "The number of results to return.",
                                "default": 10,
                            },
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

        # Available function mappings
        self.available_functions = {
            "file_saver": File_Saver().execute,
            "python_executor": python_executor,
            "baidu_search": baidu_search,
        }

    def get_tools(self, filter_by: dict = None):
        """
        Retrieve tool configurations with optional filtering.

        Args:
            filter_by (dict): Filtering conditions, e.g., {"type": "function", "name": "file_saver"} 
                            or {"name": ["file_saver", "google_search"]}

        Returns:
            list: A list of tools matching the conditions.
        """
        if not filter_by:
            return self.tools

        # Filter tools based on conditions
        filtered_tools = []
        for tool in self.tools:
            match = True
            for key, value in filter_by.items():
                # Check if the tool's attributes match the filtering conditions
                if key == "name":
                    # If value is a list, check if the tool name is in the list
                    if isinstance(value, list):
                        if tool["function"].get("name") not in value:
                            match = False
                    # If value is a string, directly match
                    elif tool["function"].get("name") != value:
                        match = False
                
            if match:
                filtered_tools.append(tool)

        return filtered_tools

    def get_function(self):
        """
        Retrieve the corresponding available function by its name.

        Args:
            function_name (str): The name of the function.

        Returns:
            Callable: The corresponding function.
        """
        return self.available_functions