class InvalidCredentialsError(Exception):
    pass


class RefreshTokenExpiredError(Exception):
    pass


class ReviewNotLiveError(Exception):
    """The review is archived or otherwise not live, so it can't be read or changed."""
