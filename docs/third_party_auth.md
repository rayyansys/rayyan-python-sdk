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
from rayyan import Rayyan
from rayyan.third_party_auth import ThirdPartyAuth
from rayyan.conf import MENDELEY

rayyan = Rayyan(credentials_file_path="cred.json", url="https://staging.rayyan.ai")
third_party_auth_instance = ThirdPartyAuth(rayyan, MENDELEY)

```

## Methods

### `get_auth_link() -> Dict[str, str]`

**Returns**: A dictionary containing the authorization link.

> Get the authorization link for connecting with Provider.
> This method will fetch the OAuth URL. You should redirect the end user to this URL to complete linking his Third party auth account with Rayyan.
> If you are a mobile client:
> You should open the link in an in-app browser tab and check for the HTTP status code for this tab.
> If you are a web client:
> You should open the link in a new tab and listen when the URL changes to the rayyan.ai URL, then check for the HTTP status code for this tab.
> If you got 200 OK, you should extract the code param from the browser tab and request with the code to get_access_token_from_code method.
> If you got 201 Created, it means that Rayyan already generated an access token, and there is no need to capture the code and call the get_access_token_from_code method. Instead, you should call the get_access_token method to get a valid access token.

**Example**:

```python
auth_link = third_party.get_auth_link()
print(auth_link)
```

### `get_access_token_from_code(code: str) -> Dict[str, str]`

Generate a valid provider access token from an OAuth code.

- `code` (type: str): The authorization code.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token_from_code = third_party.get_access_token_from_code("authorization_code_here")
print(access_token_from_code)
```

### `get_access_token() -> Dict[str, str]`

Get the access token for Provider authentication.

**Returns**: A dictionary containing the access token.

**Example**:

```python
access_token = third_party.get_access_token()
print(access_token)
```
