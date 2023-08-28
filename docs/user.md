# User Class

The `User` class provides methods to interact with user-related functionality in the Rayyan API.

## Constructor

### `__init__(self, rayyan: Rayyan) -> None`

Creates an instance of the `User` class.

#### Parameters

- `rayyan` (Rayyan): An instance of the `Rayyan` class.

#### Example Usage

```python
from rayyan import Rayyan
from rayyan.user import User

rayyan = Rayyan(credentials_file_path="cred.json")
user_instance = User(rayyan)
```

## Methods

### `get_info(self) -> Dict[str, Union[int, str, Dict[str, str]]]`

Retrieves information about the user.

Returns a dictionary containing user information, including user ID, username, and additional metadata.

#### Example Usage

```python
user_info = user_instance.get_info()
```

### `delete(self) -> Dict[str, Union[int, str, Dict[str, str]]]`

Deletes the user account.

Returns a dictionary containing the status and message indicating the result of the deletion operation.

#### Example Usage

```python
delete_result = user_instance.delete()
```

### `revoke_token(self) -> Dict[str, Union[int, str, Dict[str, str]]]`

Revokes the access token associated with the user.

Returns a dictionary containing the status and message indicating the result of the token revocation.

#### Example Usage

```python
revoke_result = user_instance.revoke_token()
```
