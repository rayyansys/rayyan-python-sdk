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
from rayyan.rayyan import Rayyan
rayyan = Rayyan("cred.json")
review_instance = rayyan.review(rayyan)
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
def export(self, id: int) -> Dict[str, str]:
```

Export the content of a review by ID.

**Example:**

```python
review_id = 789
exported_content = review_instance.export(review_id)
print(exported_content)
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

Of course! Here's the continuation of the documentation with examples for the remaining methods:

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
def bulk_customizations(self, id: int, types: list, start_id: int) -> Dict[str, str]:
```

Apply bulk customizations to a review for specified article types.

**Example:**

```python
review_id = 123
article_types = ["Type1", "Type2"]
start_article_id = 100
bulk_custom_result = review_instance.bulk_customizations(review_id, article_types, start_article_id)
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
def blind(self, id: int) -> Dict[str, str]:
```

Blind a review.

**Example:**

```python
review_id = 123
blind_result = review_instance.blind(review_id)
print(blind_result)
```
