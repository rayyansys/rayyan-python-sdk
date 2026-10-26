# Review Class

This class provides methods for interacting with reviews in the Rayyan application.

## Constructor

```python
class Review:
    def __init__(self, rayyan: Rayyan):
```

- `rayyan` (`Rayyan`): An instance of the `Rayyan` class for API communication.

### Example Usage

```python
from rayyan import Rayyan
from rayyan.reviews import Review

rayyan = Rayyan("cred.json")
review_instance = Review(rayyan)
```

## Methods

### Get All Reviews

```python
def get_all(self) -> Dict[str, str]:
```

Retrieve information about all reviews.

**Example:**

```python
review_data = review_instance.get_all()
print(review_data)
```

### Get Review by ID

```python
def get(self, id: int) -> Dict[str, str]:
```

Retrieve information about a specific review by ID.

**Example:**

```python
review_id = 123
review_info = review_instance.get(review_id)
print(review_info)
```

### Create Review

```python
def create(self, review: dict) -> Dict[str, str]:
```

Create a new review with the provided details.

**Example:**

```python
new_review = {
    "title": "Sample Review",
    "description": "This is a sample review.",
    "metadata_attributes": {
        "research_question": "What is the impact of X?",
        "research_field": "Social Sciences",
    },
    "team_id": 456
}
created_review = review_instance.create(new_review)
print(created_review)
```

### Export Review

```python
def export(self, review_id: int, export_format: str, filters: Optional[ExportFilters] = None) -> Dict[str, Any]:
```

Start an export of a review in one of the formats `csv`, `ris`, `bib` or `enw`.

The export runs in the background. The call returns `{"status": "OK"}` once the job is queued, not the exported content. When the job finishes, the file appears in the user's My Library and the user receives an email with a link to it.

`filters` (optional) controls what the export contains. Each flag takes `0` or `1`:

| Filter | Effect |
|---|---|
| `author_format` | `"lf"` (Last, First) or `"fl"` (First Last) |
| `include_abstracts`, `include_decisions`, `include_labels`, `include_exclusion_reasons`, `include_user_notes`, `include_fulltexts`, `include_questions` | Include that information for your own account |
| `all_decisions`, `all_labels`, `all_notes` | Include decisions, labels or notes from every reviewer, not just your own |
| `include_exclusion_reasons_col` | Put exclusion reasons in their own column per user. Only works together with `all_decisions` |
| `include_fields` | List of CSV columns to keep, e.g. `["key", "title", "year", "authors", "doi"]` |

**Example:**

```python
result = review_instance.export(
    789,
    "csv",
    filters={"all_decisions": 1, "include_exclusion_reasons_col": 1, "author_format": "fl"},
)
print(result)  # {"status": "OK"}; the file arrives in My Library later
```

### Copy Review

```python
def copy(self, id: int, review: dict) -> Dict[str, str]:
```

Create a copy of a review with specified details.

**Example:**

```python
source_review_id = 123
copy_details = {
    "target_review": 456,
    "start": 0,
    "length": 10,
    # ... other copy parameters ...
}
copied_review = review_instance.copy(source_review_id, copy_details)
print(copied_review)
```

### Get Review Results

```python
def results(self, id: int, params: dict) -> Dict[str, str]:
```

Retrieve the results of a review based on specified parameters.

**Example:**

```python
review_id = 789
result_params = {
    "start": 0,
    "length": 20,
    "order[0][column]": 1,
    "order[0][dir]": "asc",
    # ... other result parameters ...
}
review_results = review_instance.results(review_id, result_params)
print(review_results)
```

### Customize Review

```python
def customize(self, id: int, article_id: int, plan: dict) -> Dict[str, str]:
```

Customize a review by specifying inclusion/exclusion details for an article.

**Example:**

```python
review_id = 123
article_id = 456
customization_plan = {
    "included": 1,
    "label1": "Included"
}
customized_result = review_instance.customize(review_id, article_id, customization_plan)
print(customized_result)
```

### Get Review Articles

```python
def articles(self, id: int, start: int, length: int) -> Dict[str, str]:
```

Retrieve articles associated with a review, with optional pagination.

**Example:**

```python
review_id = 789
start_index = 0
batch_length = 10
review_articles = review_instance.articles(review_id, start_index, batch_length)
print(review_articles)
```

### Bulk Customizations

```python
def bulk_customizations(self,id: int,key: str,value: int,article_ids: str,) -> Dict[str, str]:
```

Apply bulk customizations to a review for specified article types.

**Example:**

```python
key = "xyz"
value = 1
article_ids = "1,2,3"
id = 1
bulk_custom_result = review_instance.bulk_customizations(id,key, value, article_ids)
print(bulk_custom_result)
```

### Get Customizations

```python
def get_customizations(self, id: int, params: dict) -> Dict[str, str]:
```

Retrieve customizations for a review based on specified parameters.

**Example:**

```python
review_id = 789
customization_params = {
    "start_id": 100,
    "end_id": 150,
    "types[]": ["inclusion_decisions", "labels","exclusion_reasons"],
}
customization_data = review_instance.get_customizations(review_id, customization_params)
print(customization_data)
```

### Get Facets

```python
def facets(self, id: int, params: dict) -> Dict[str, str]:
```

Retrieve facet information for a review based on specified parameters.

**Example:**

```python
review_id = 123
facet_params = {
    "facets[inclusion_counts]": "1",
    "facets[decision_counts]": "1",
    # ... other facet parameters ...
}
facet_info = review_instance.facets(review_id, facet_params)
print(facet_info)
```

### Inclusion Counts

```python
def inclusion_counts(self, id: int, user_id: int) -> Dict[str, str]:
```

Get inclusion counts for a review, optionally specifying a user ID.

**Example:**

```python
review_id = 789
user_identifier = 12345
inclusion_counts = review_instance.inclusion_counts(review_id, user_identifier)
print(inclusion_counts)
```

### Calculate Ratings

```python
def calculate_ratings(self, id: int) -> Dict[str, str]:
```

Calculate and retrieve ratings for a review.

**Example:**

```python
review_id = 123
rating_result = review_instance.calculate_ratings(review_id)
print(rating_result)
```

### Archive Review

```python
def archive(self, id: int) -> Dict[str, str]:
```

Archive a review.

**Example:**

```python
review_id = 456
archive_result = review_instance.archive(review_id)
print(archive_result)
```

### Unarchive Review

```python
def unarchive(self, id: int) -> Dict[str, str]:
```

Unarchive a review.

**Example:**

```python
review_id = 456
unarchive_result = review_instance.unarchive(review_id)
print(unarchive_result)
```

### Blind Review

```python
def blind(self, id: int) -> Dict[str, Any]:
```

Toggle blind mode on a review. Each call flips the current state and returns the new value as a boolean, e.g. `{"is_blind": True}`. Works on archived reviews too.

**Example:**

```python
review_id = 123
blind_result = review_instance.blind(review_id)
print(blind_result)  # {"is_blind": True}
```

### Set Blind Mode

```python
def set_blind(self, id: int, enabled: bool) -> Dict[str, Any]:
```

Turn blind mode on (`enabled=True`) or off. Unlike `blind()`, it reads the review first and only toggles when the state differs. Returns `{"is_blind": bool, "changed": bool}`.

- It is safe to retry, but not safe to run concurrently: two simultaneous calls can both read the old state and both toggle it.
- It raises `TypeError` if `enabled` is not a bool, so strings such as `"false"` are rejected rather than toggling the review.
- It raises `rayyan.errors.ReviewNotLiveError` on an archived review, because reading an archived review fails. Unarchive it first; `blind()` itself still works on archived reviews.

**Example:**

```python
result = review_instance.set_blind(123, enabled=False)
print(result)  # {"is_blind": False, "changed": True}
```

### Create AI Screener

```python
def create_ai_screener(self, review_id: int, extra: Dict[str, Any], ai_model_name: Optional[str] = None) -> Dict[str, Any]:
```

Start an AI screener job on a review. `extra` holds the article filters, in the same form as other review filters.

`ai_model_name` (optional) picks the screener model, e.g. `"gpt-4.1-mini"`; leave it out to use the default model. The accepted names are listed in `LlmBotsLoader::SUPPORTED_MODELS` in rayyan-ruby. Rayyan returns 400 if the model is unsupported, or if the `ai_screener_model_change` feature is not enabled for the user.

**Example:**

```python
result = review_instance.create_ai_screener(123, extra={}, ai_model_name="gpt-4.1-mini")
print(result)
```
