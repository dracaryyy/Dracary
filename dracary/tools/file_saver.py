import os
import aiofiles
from dracary.config.load import ConfigLoader


class File_Saver:
    """
    A utility class for saving content to a file.
    """

    async def execute(self, content: str, file_path: str, mode: str = "w") -> str:
        """
        Save content to a file at the specified path.

        Args:
            content (str): The content to save to the file.
            file_path (str): The path where the file should be saved.
            mode (str, optional): The file opening mode. Default is 'w' for write. Use 'a' for append.

        Returns:
            str: A message indicating the result of the operation.
        """
        config_loader = ConfigLoader()

        try:
            # Retrieve the workspace directory from the configuration
            workspace = config_loader.get("dir.workspace")
            if not isinstance(workspace, str):
                raise ValueError(f"Invalid workspace path. Expected a string, got {type(workspace)}: {workspace}")

            # Determine the full path of the file
            if os.path.isabs(file_path):
                file_name = os.path.basename(file_path)
                full_path = os.path.join(workspace, file_name)
            else:
                full_path = os.path.join(workspace, file_path)

            # Ensure the directory exists
            directory = os.path.dirname(full_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write content to the file asynchronously
            async with aiofiles.open(full_path, mode, encoding="utf-8") as file:
                await file.write(content)

            return f"Content successfully saved to {full_path}"

        except ValueError as ve:
            # Handle invalid workspace path errors
            return f"Error: {str(ve)}"

        except OSError as oe:
            # Handle file system-related errors
            return f"File system error: {str(oe)}"

        except Exception as e:
            # Handle all other exceptions
            return f"Unexpected error: {str(e)}"