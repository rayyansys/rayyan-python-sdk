
from rayyan.types import RayyanProtocol as Rayyan


class MyLib:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def list_directory(
        self,
        path: str,
        current_dir: bool = False,
        order_by: str = "file_name",
        order_dir: str = "asc",
        limit: int | None = None,
        offset_token: str | None = None,
        filter_name: str | None = None,
        filter_value: str | None = None,
        filter_value_min: float | None = None,
        filter_value_max: float | None = None,
        title: str | None = None
    ) -> dict:
        """List files and folders in the user's My Library with advanced filtering and sorting.

        Args:
            path (str): Directory path (e.g., '/' for root).
            current_dir (bool): Whether to list contents under 'path' or return the directory itself.
            order_by (str): Field to sort by. Ignored if a filter is applied.
            order_dir (str): Sort direction ('asc' or 'desc').
            limit (int, optional): Max results to return. Defaults to 25 when current_dir=False, or 1 when True.
            offset_token (str, optional): Pagination token from a previous response.
            filter_name (str, optional): Field to filter by.
            filter_value (str, optional): Filter value (required for file_name, file_type, key_prefix).
            filter_value_min (float, optional): Minimum value for file_size/upload_time filters.
            filter_value_max (float, optional): Maximum value for file_size/upload_time filters.
            title (str, optional): Search by file title across all directories.

        Returns:
            dict: Response in the format:
            {
                "items": [
                    {
                        "key": "string",
                        "file_size": 0,
                        "upload_time": "2025-10-15T00:57:16.940Z",
                        "file_type": "string",
                        "metadata": {
                            "metadata_signature": "string",
                            "total_articles": 0,
                            "error": "string",
                            "warnings": ["string"]
                        },
                        "titles": ["string"]
                    }
                ],
                "total": 0,
                "offset_token": "string"
            }
        """
        # Determine default limit
        if limit is None:
            limit = 1 if current_dir else 25

        params = {
            "current_dir": str(current_dir).lower(),
            "order_by": order_by,
            "order_dir": order_dir,
            "limit": limit
        }

        # Optional query params
        if offset_token:
            params["offset_token"] = offset_token
        if filter_name:
            params["filter_name"] = filter_name
        if filter_value:
            params["filter_value"] = filter_value
        if filter_value_min is not None:
            params["filter_value_min"] = filter_value_min
        if filter_value_max is not None:
            params["filter_value_max"] = filter_value_max
        if title:
            params["title"] = title

        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"/ls/{path}",
            params=params
        )
