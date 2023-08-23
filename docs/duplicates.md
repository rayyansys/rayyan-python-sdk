# Duplicates Class Documentation

The `Duplicates` class provides methods to manage duplicate articles within a review in the Rayyan system.

## Constructor

### `Duplicates(rayyan: Rayyan)`

Create a new `Duplicates` instance.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.

**Example**:

```python
from rayyan import Rayyan
from rayyan.duplicates import Duplicates

rayyan = Rayyan(credentials_file_path="cred.json", url="https://staging.rayyan.ai")
duplicates_instance = Duplicates(rayyan)
```

## Methods

### `get_duplicate(id, article_id) -> Dict[str, str]`

Retrieve information about a duplicate article within a review.

- `id` (type: any): The review identifier.
- `article_id` (type: any): The ID of the article to get duplicate information for.

**Returns**: A dictionary containing information about the duplicate article.

**Example**:

```python
duplicate_info = duplicates_instance.get_duplicate(id=123, article_id=456)
print(duplicate_info)
```

### `add_duplicate(id) -> Dict[str, str]`

Add a new duplicate article to a review.

- `id` (type: any): The review identifier.

**Returns**: A dictionary confirming the addition of the duplicate article.

**Example**:

```python
add_confirmation = duplicates_instance.add_duplicate(id=123)
print(add_confirmation)
```

### `update_duplicate(id, article_id, duplicate_action: int, isDeletedArticle: bool = False) -> Dict[str, str]`

Update the status of a duplicate article within a review.

- `id` (type: any): The review identifier.
- `article_id` (type: any): The ID of the article to update duplicate status for.
- `duplicate_action` (type: int): The action to perform on the duplicate article.
- `isDeletedArticle` (type: bool, optional): Indicates if the article is deleted.

**Returns**: A dictionary confirming the update of the duplicate article status.

**Example**:

```python
update_confirmation = duplicates_instance.update_duplicate(id=123, article_id=456, duplicate_action=2, isDeletedArticle=True)
print(update_confirmation)
```
