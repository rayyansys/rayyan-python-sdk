from .base import ReviewBase
from .samples import ReviewSamples
from .criteria import ReviewCriteria
from .questions import ReviewQuestions
from .exports import ReviewExports
from .importers import ReviewImporters
from .ai_screeners import ReviewAiScreeners
from .articles import ReviewArticles
from .customizations import ReviewCustomizations
from .metadata import ReviewMetadata
from .fulltext import ReviewFulltext
from rayyan.duplicates import Duplicates

class Review(
    ReviewBase,
    ReviewSamples,
    ReviewCriteria,
    ReviewQuestions,
    ReviewExports,
    ReviewImporters,
    ReviewAiScreeners,
    ReviewArticles,
    ReviewCustomizations,
    ReviewMetadata,
    ReviewFulltext,
    Duplicates,
):
    """Facade combining all review-related mixins into a single client class.

    Usage:
        from rayyan import RayyanClientProtocol
        review = Review(rayyan_client)

    All methods delegate to the underlying rayyan client's request handler.
    """

    pass