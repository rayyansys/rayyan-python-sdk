from typing import TYPE_CHECKING

from .paths import ADMIN_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Admin:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def lis_full_texts(self) -> dict:
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
    def lis_searches(self) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/searches.json"
        )

    def delete_searches(self, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{ADMIN_ROUTE}/searches{id}.json"
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

    def list_reviews(
        self, is_blind_eq: bool, title_cont: str, total_articles_gt_any: int
    ) -> dict:
        params = {
            "q[is_blind_eq]": is_blind_eq,
            "q[title_cont]": title_cont,
            "q[total_articles_gt_any]": total_articles_gt_any,
        }
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
        self, id: int, name: str, capacity: str, new_collaborator_emails: str
    ) -> dict:
        return self.__rayyan__.request.request_handler(
            method="PUT",
            path=f"{ADMIN_ROUTE}/teams/{id}.json",
            params={
                "team[name]": name,
                "team[capacity]": capacity,
                "team[new_collaborator_emails]": new_collaborator_emails,
            },
        )

    def create_team(self, name: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{ADMIN_ROUTE}/teams.json",
            payload={"team[name]": name},
        )

    def list_teams(self) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{ADMIN_ROUTE}/teams.json"
        )
