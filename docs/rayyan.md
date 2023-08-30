# Rayyan Class

The `Rayyan` class provides an interface for interacting with the Rayyan API. It manages user credentials and provides access to user-related functionality.

## Constructor

### `__init__(self, credentials_file_path: str, url: str = "https://rayyan.ai") -> None`

Creates an instance of the `Rayyan` class.

> it uses the production enviroment by default but you can override the url at any time you needed to.

#### Parameters

- `credentials_file_path` (str): The file path to the JSON file containing the user credentials.
- `url` (str): The main url that the sdk will be using.

#### Example Usage

```python
rayyan_instance = Rayyan(credentials_file_path = "/path/to/credentials.json")
```
