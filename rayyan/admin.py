from typing import TYPE_CHECKING

from .paths import ADMIN_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Admin:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def list_full_texts(self) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/fulltexts.json"
        )

    def delete_full_texts(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{ADMIN_ROUTE}/fulltexts/{id}.json"
        )

    def show_full_text(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/fulltexts/{id}.json"
        )

    # __________________search________________
    def list_searches(self) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/searches.json"
        )

    def delete_searches(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{ADMIN_ROUTE}/searches/{id}.json"
        )

    def show_search(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/searches/{id}.json"
        )

    # __________________reviews________________
    def unarchive_review(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST", path=f"{ADMIN_ROUTE}/reviews/{id}/unarchive.json"
        )

    def archive_review(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST", path=f"{ADMIN_ROUTE}/reviews/{id}/archive.json"
        )

    def list_reviews(self, params: dict) -> dict:
        params = {f"q[{key}]": value for key, value in filters.items()}
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/reviews.json", params=params
        )

    def delete_review(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{ADMIN_ROUTE}/reviews/{id}.json"
        )

    def edit_review(self, id: int, title: str, description: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="PUT",
            path=f"{ADMIN_ROUTE}/reviews/{id}.json",
            params={"title": title, "description": description},
        )

    def show_review(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/reviews/{id}.json"
        )

    # __________________teams________________
    def show_team(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/teams/{id}.json"
        )

    def delete_team(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{ADMIN_ROUTE}/teams/{id}.json"
        )

    def edit_team(
        self,
        id: int,
        name: str,
        capacity: int,
        new_collaborator_emails: str,
        new_admin_emails: str,
        new_viewer_emails: str,
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="PUT",
            path=f"{ADMIN_ROUTE}/teams/{id}.json",
            params={
                "team[name]": name,
                "team[capacity]": capacity,
                "team[new_collaborator_emails]": new_collaborator_emails,
                "team[new_admin_emails]": new_admin_emails,
                "team[new_viewer_emails]": new_viewer_emails,
            },
        )

    def create_team(self, name: str, capacity=None) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{ADMIN_ROUTE}/teams.json",
            payload={
                "team[name]": name,
                "team[capacity]": capacity,
            },
        )

    def list_teams(self) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/teams.json"
        )
