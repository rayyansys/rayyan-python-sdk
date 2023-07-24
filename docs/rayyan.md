# Rayyan Class

The `Rayyan` class provides an interface for interacting with the Rayyan API. It manages user credentials and provides access to user-related functionality.

## Constructor

### `__init__(self, credentials_file_path: str) -> None`

Creates an instance of the `Rayyan` class.

#### Parameters

- `credentials_file_path` (str): The file path to the JSON file containing the user credentials.

#### Example Usage

```python
rayyan_instance = Rayyan("/path/to/credentials.json")
```
