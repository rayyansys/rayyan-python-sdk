from typing import TYPE_CHECKING

from .paths import REVIEWS_ROUTE


if TYPE_CHECKING:
    from rayyan.rayyan import Rayyan
else:
    Rayyan = None


class Search:
    def __init__(self, rayyan: Rayyan):
        self.__rayyan__ = rayyan

    def pre_signed_url(self, review_id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="GET", path=f"{REVIEWS_ROUTE}/{review_id}/searches/new"
        )

    def upload_search_file(
        self,
        key: str,
        credential: str,
        algorithm: str,
        date: str,
        signature: str,
        policy: str,
        success_action_status: int,
        url: str,
        file: str,
    ) -> dict:
        file_name = file.split("/")[-1]
        return self.__rayyan__.request.file_uploader(
            url=url,
            params=
            {
                "key": key,
                "x-amz-credential": credential,
                "x-amz-algorithm": algorithm,
                "x-amz-date": date,
                "x-amz-signature": signature,
                "policy": policy,
                "success_action_status": success_action_status,
                "file": (file_name, open(file, 'rb'))
            }
        )

    def create(self, review_id: int, s3_key: str, original_filename: str) -> dict:
        return self.__rayyan__.request.request_handler(
            method="POST",
            path=f"{REVIEWS_ROUTE}/{review_id}/searches",
            payload={
                "search": {"s3_key": s3_key, "original_filename": original_filename}
            },
        )

    def delete(self, review_id: int, id: int) -> dict:
        return self.__rayyan__.request.request_handler(
            method="DELETE", path=f"{REVIEWS_ROUTE}/{review_id}/searches/{id}"
        )
