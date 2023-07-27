# Rayyan Class

The `Rayyan` class provides an interface for interacting with the Rayyan API. It manages user credentials and provides access to user-related functionality.

## Constructor

### `__init__(self, credentials_file_path: str, url: str = "https://staging.rayyan.ai") -> None`

Creates an instance of the `Rayyan` class.
 > it uses the staging enviroment by default but you can override the url at any time you needed to.

#### Parameters

- `credentials_file_path` (str): The file path to the JSON file containing the user credentials.

#### Example Usage

```python
rayyan_instance = Rayyan("/path/to/credentials.json")
```
