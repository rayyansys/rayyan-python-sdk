# MendeleyConnect Class Documentation

The `MendeleyConnect` class offers methods to connect and authenticate with the Mendeley third-party provider within the Rayyan system.

## Constructor

### `MendeleyConnect(rayyan: Rayyan, third_party: str)`

Create a new `MendeleyConnect` instance for connecting with the Mendeley provider.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.
- `third_party` (type: str): The name of the third-party provider (e.g., "mendeley").

**Example**:

```python
from rayyan.rayyan import Rayyan
rayyan = Rayyan("cred.json")
mendeley_instance = rayyan.mendeley_connect(rayyan, "mendeley")
```

## Methods

### `get_auth_link() -> Dict[str, str]`

Get the authorization link for connecting with Mendeley.

**Returns**: A dictionary containing the authorization link.

**Example**:

```python
auth_link = mendeley_instance.get_auth_link()
print(auth_link)
```

### `get_access_token() -> Dict[str, str]`

Get the access token for Mendeley authentication.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token = mendeley_instance.get_access_token()
print(access_token)
```

### `get_access_token_from_code(code: str) -> Dict[str, str]`

Exchange an authorization code for an access token from Mendeley.

- `code` (type: str): The authorization code.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token_from_code = mendeley_instance.get_access_token_from_code("authorization_code_here")
print(access_token_from_code)
```

---

Replace `"mendeley"` and `"authorization_code_here"` with real values according to your specific use case.
