import warnings
from rayyan.reviews import Review

__all__ = ["Review"]

warnings.warn(
    "Importing from 'review' is deprecated. Use 'reviews.Review' instead.",
    DeprecationWarning,
    stacklevel=2,
)