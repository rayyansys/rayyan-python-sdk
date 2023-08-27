# Highlight Class Documentation

The `Highlight` class provides methods to create and delete highlights in articles for a review within the Rayyan system.

## Constructor

### `Highlight(rayyan: Rayyan)`

Create a new `Highlight` instance.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.

**Example**:

```python
from rayyan import Rayyan
from rayyan.highlight import Highlight

rayyan = Rayyan(credentials_file_path="cred.json")
highlight_instance = Highlight(rayyan)
```

## Methods

### `create_highlight(id: int, category_id: int, keyword: str) -> dict`

Create a new highlight in an article for a review.

- `id` (type: int): The review identifier.
- `category_id` (type: int): The category ID for the highlight.
- `keyword` (type: str): The keyword to highlight.

**Returns**: A dictionary containing information about the created highlight.

**Example**:

```python
highlight_data = highlight_instance.create_highlight(id=123, category_id=456, keyword="important term")
print(highlight_data)
```

### `delete_highlight(id: int, category_id: int, body_id: int) -> dict`

Delete a highlight from an article within a review.

- `id` (type: int): The review identifier.
- `category_id` (type: int): The category ID of the highlight to delete.
- `body_id` (type: int): The ID of the highlighted content.

**Returns**: A dictionary confirming the deletion of the highlight.

**Example**:

```python
delete_confirmation = highlight_instance.delete_highlight(id=123, category_id=456, body_id=789)
print(delete_confirmation)
```
