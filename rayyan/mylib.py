
from rayyan.types import RayyanProtocol as Rayyan


class MyLib:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def list_directory(self, path) -> dict:
        """List all files in the user's My Library.

        Returns:
            dict: A dictionary containing the list of files in My Library.
        """
        return self.__rayyan__.request.request_handler(
            method="GET",
            path=f"/ls/{path}"
        )