
import os
import re
import requests

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

    def create_directory(self, path: str) -> dict:
        """
        Args:
            path (str): Directory path (e.g., '/a')

        Returns:
            dict: Response for the creating dir.
        """
        path = self._normalize_path(path)

        # Root always exists
        if path == "/":
            return {"message": "Root directory already exists."}

        return self.__rayyan__.request.request_handler(
            method="POST",
            path=path + "/",
        )

    def download_file(self, path: str) -> dict:
        """
        Download a file from My Library.

        Args:
            path (str): Path to the file (e.g., '/a.txt').
                        Must NOT have a trailing slash.

        Returns:
            dict: Response from the My Library API.
        """
        if not path:
            raise ValueError("File path cannot be empty.")

        # Normalize path: collapse slashes, remove trailing slash, ensure leading slash
        path = self._normalize_path(path)

        if path.endswith("/"):
            raise ValueError("File path must not have a trailing slash.")

        return self.__rayyan__.request.request_handler(
            method="GET",
            path=path,
        )

    def upload_file(self, path: str, local_file_path: str) -> dict:
        """
        Upload a file to My Library using a presigned URL, automatically creating
        any missing parent directories.

        Steps:
            1. Ensure all parent directories exist.
            2. Read the local file into memory.
            3. Request presigned URL from My Library.
            4. Immediately POST the file using the presigned URL.

        Args:
            path (str): Path to the file in My Library (e.g., '/a/b/c.txt').
                        Must NOT have a trailing slash.
            local_file_path (str): Local path to the file to upload.

        Returns:
            dict: Response including presigned URL info and upload result.
        """
        if not path:
            raise ValueError("File path cannot be empty.")

        # Normalize file path
        path = self._normalize_path(path)
        if path.endswith("/"):
            raise ValueError("File path must not have a trailing slash.")

        presigned_url, fields = self.get_presigned_url(path)
        if not presigned_url or not fields:
            raise RuntimeError("Invalid presigned URL response from server.")

        with open(local_file_path, "rb") as f:
            files = {"file": (os.path.basename(local_file_path), f)}
            response = requests.post(presigned_url, data=fields, files=files, timeout=4)

            if not response.ok:
                raise RuntimeError(
                    f"File upload failed: {response.status_code} {response.text}"
                )

        return {
            "message": f"File '{path}' uploaded successfully.",
            "upload_response": response.text
        }

    def copy_or_move_file(self, path: str, new_path: str, move: bool = False) -> dict:
        """
        Copy or move a file or directory in My Library.

        Args:
            path (str): Source file or directory path (must not have trailing slash).
            new_path (str): Target full path (must include filename or directory name, no trailing slash).
            move (bool): True to move, False to copy.

        Returns:
            dict: Structured response including API response.
        """
        if not path or not new_path:
            raise ValueError("Both 'path' and 'new_path' must be provided.")

        # Normalize paths
        path = self._normalize_path(path)
        new_path = self._normalize_path(new_path)

        if path.endswith("/") or new_path.endswith("/"):
            raise ValueError("Paths must not have trailing slashes.")

        # Perform copy or move via PUT request
        params = {"new_path": new_path, "move": str(move).lower()}
        api_response = self.__rayyan__.request.request_handler(
            method="PUT",
            path=path,
            params=params
        )

        return {
            "operation": "move" if move else "copy",
            "source": path,
            "destination": new_path,
            "api_response": api_response
        }


    def get_presigned_url(self, path: str) -> dict:
        """
        Obtain a presigned URL for uploading a file to My Library.

        Args:
            path (str): Target file path in My Library (e.g., '/a/b/c.txt').
        Returns:
            dict: Response containing presigned URL and fields.
        """

        # Request presigned URL
        presign_resp = self.__rayyan__.request.request_handler(
            method="POST",
            path=path,
            headers={"accept": "application/json"}
        )

        presigned_url = presign_resp.get("url")
        fields = presign_resp.get("fields")
        return presigned_url, fields

    def _normalize_path(self, path: str) -> str:
        """
        Normalize a path:
        - Collapses multiple slashes
        - Removes trailing slashes (except '/')
        - Ensures a single leading slash
        """
        if not path:
            return "/"
        path = re.sub(r"/+", "/", path.strip())  # collapse multiple slashes
        path = path.rstrip("/") if path != "/" else "/"
        if not path.startswith("/"):
            path = "/" + path
        return path