# ThirdPartyAuth Class Documentation

The `ThirdPartyAuth` class offers methods to connect and authenticate with the third-party provider within the Rayyan system.

## Constructor

### `ThirdPartyAuth(rayyan: Rayyan, third_party: str)`

Create a new `ThirdPartyAuth` instance for connecting with the third-party provider.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.
- `third_party` (type: str): The name of the third-party provider you can import it from conf file.
> to see all third-party providers available you can import ALLOWED_PROVIDERS from third_party

**Example**:

```python
from rayyan.rayyan import Rayyan
from rayyan.conf import MENDELEY
rayyan = Rayyan("cred.json")
third_party = rayyan.third_party_auth(rayyan, MENDELEY)
```

## Methods

### `get_auth_link() -> Dict[str, str]`

Get the authorization link for connecting with Provider.

**Returns**: A dictionary containing the authorization link.

**Example**:

```python
auth_link = third_party.get_auth_link()
print(auth_link)
```

### `get_access_token() -> Dict[str, str]`

Get the access token for Provider authentication.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token = third_party.get_access_token()
print(access_token)
```

### `get_access_token_from_code(code: str) -> Dict[str, str]`

Exchange an authorization code for an access token from Provider.

- `code` (type: str): The authorization code.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token_from_code = third_party.get_access_token_from_code("authorization_code_here")
print(access_token_from_code)
```
