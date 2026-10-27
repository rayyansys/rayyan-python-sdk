import re

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

    def _normalize_path(self, path: str) -> str:
        """Normalize a path: collapse slashes, remove trailing slash, ensure leading slash."""
        if not path:
            return "/"
        path = re.sub(r"/+", "/", path.strip())
        path = path.rstrip("/") if path != "/" else "/"
        if not path.startswith("/"):
            path = "/" + path
        return path
