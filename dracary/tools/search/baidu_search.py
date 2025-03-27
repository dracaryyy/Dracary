from baidusearch.baidusearch import search
from typing import List, Dict


class BaiduSearchTool:
    """Baidu Search Tool Class"""

    @staticmethod
    async def search(query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Perform a search using Baidu and retrieve results.

        Args:
            query (str): The search keyword.
            num_results (int): The number of results to return. Default is 10.

        Returns:
            List[Dict[str, str]]: A list of search results, where each result contains 'title', 'abstract', and 'url'.
        """
        try:
            results = search(query, num_results=num_results)
            return results
        except Exception as e:
            print(f"Error occurred during Baidu search: {e}")
            return []