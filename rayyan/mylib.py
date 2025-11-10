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
        """List files/folders in My Library with optional filters."""
        if limit is None:
            limit = 1 if current_dir else 25

        params = {
            "current_dir": str(current_dir).lower(),
            "order_by": order_by,
            "order_dir": order_dir,
            "limit": limit
        }

        for k, v in [
            ("offset_token", offset_token),
            ("filter_name", filter_name),
            ("filter_value", filter_value),
            ("filter_value_min", filter_value_min),
            ("filter_value_max", filter_value_max),
            ("title", title)
        ]:
            if v is not None:
                params[k] = v

        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"/ls/{path}",
            params=params
        )

    def create_directory(self, path: str) -> dict:
        """Create a directory at the given path."""
        path = self._normalize_path(path)
        if path == "/":
            return {"message": "Root directory already exists."}
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=path + "/"
        )

    def download_file(self, path: str) -> dict:
        """Download a file from My Library."""
        if not path:
            raise ValueError("File path cannot be empty.")
        path = self._normalize_path(path)
        if path.endswith("/"):
            raise ValueError("File path must not have a trailing slash.")
        return self.__rayyan__.request.request_handler(
            method="GET",
            path=path
        )

    def upload_file(self, path: str, local_file_path: str) -> dict:
        """Upload a local file to My Library using a presigned URL."""
        if not path:
            raise ValueError("File path cannot be empty.")
        path = self._normalize_path(path)

        presigned_url, fields = self.get_presigned_url(path)
        if not presigned_url or not fields:
            raise RuntimeError("Empty presigned URL response.")

        with open(local_file_path, "rb") as f:
            files = {"file": (os.path.basename(local_file_path), f)}
            response = requests.post(presigned_url, data=fields, files=files, timeout=4)
            if not response.ok:
                raise RuntimeError(f"Upload failed: {response.status_code} {response.text}")

        return {
            "message": f"File '{path}' uploaded successfully.",
            "upload_response": response.text
        }

    def copy_or_move_file(self, path: str, new_path: str, move: bool = False) -> dict:
        """Copy or move a file/directory in My Library."""
        if not path or not new_path:
            raise ValueError("Both 'path' and 'new_path' are required.")

        path = self._normalize_path(path)
        new_path = self._normalize_path(new_path)

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

    def get_presigned_url(self, path: str) -> tuple[str, dict]:
        """Get a presigned URL and fields for uploading a file."""
        resp = self.__rayyan__.request.request_handler(
            method="POST",
            path=path,
            headers={"accept": "application/json"}
        )
        return resp.get("url"), resp.get("fields")

    def _normalize_path(self, path: str) -> str:
        """Normalize a path: collapse slashes, remove trailing slash, ensure leading slash."""
        if not path:
            return "/"
        path = re.sub(r"/+", "/", path.strip())
        path = path.rstrip("/") if path != "/" else "/"
        if not path.startswith("/"):
            path = "/" + path
        return path
