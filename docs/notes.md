# Notes Class Documentation

The `Notes` class provides methods to manage notes related to articles in the Rayyan system.

## Constructor

### `Notes(rayyan: Rayyan)`

Create a new `Notes` instance.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.

**Example**:

```python
from rayyan.rayyan import Rayyan
rayyan = Rayyan("cred.json")
notes_instance = rayyan.notes(rayyan)
```

## Methods

### `create_note(review_id: int, article_id: int, text: str) -> dict`

Create a new note for a specific article within a review.

- `review_id` (type: int): The ID of the review.
- `article_id` (type: int): The ID of the article for which the note is being created.
- `text` (type: str): The content of the note.

**Returns**: A dictionary containing information about the created note.

**Example**:

```python
note_data = notes_instance.create_note(review_id=123, article_id=456, text="This article needs further analysis.")
print(note_data)
```

### `update_note(review_id: int, article_id: int, note_id: int, text: str) -> dict`

Update an existing note for a specific article within a review.

- `review_id` (type: int): The ID of the review.
- `article_id` (type: int): The ID of the article associated with the note.
- `note_id` (type: int): The ID of the note to be updated.
- `text` (type: str): The new content for the note.

**Returns**: A dictionary containing information about the updated note.

**Example**:

```python
updated_note_data = notes_instance.update_note(review_id=123, article_id=456, note_id=789, text="Updated analysis: new findings.")
print(updated_note_data)
```

### `delete_note(review_id: int, article_id: int, note_id: int) -> dict`

Delete a note associated with a specific article within a review.

- `review_id` (type: int): The ID of the review.
- `article_id` (type: int): The ID of the article associated with the note.
- `note_id` (type: int): The ID of the note to be deleted.

**Returns**: A dictionary confirming the deletion of the note.

**Example**:

```python
delete_confirmation = notes_instance.delete_note(review_id=123, article_id=456, note_id=789)
print(delete_confirmation)
```
