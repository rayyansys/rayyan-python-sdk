# Rayyan Python SDK

A Python SDK for Rayyan [HTTP APIs](https://github.com/rayyansys/rayyan-api-docs).
## Installation

To install the latest stable release of Rayyan Python SDK, execute the following command:

```shell
pip install rayyan-sdk
```

For the nightly builds, execute the following command:

```shell
pip install -i https://test.pypi.org/simple/ rayyan-sdk
```

## Usage

To use the SDK, you need to have a credentials file in JSON format like the one below.
You can retrieve such file by signing in to your Rayyan account and going to My Account page.

```json
// creds.json
{
    "access_token": "9c2b0fe74ab7cd8d1227cd2fd",
    "refresh_token": "b40e325a1a7f53831ec3c09fffc7"
}
```

Import Rayyan main class and pass the credentials file to it like this:

```python
rayyan = Rayyan("cred.json")
```

> Note: The credentials file should be kept secret and not shared with anyone.
It acts as a password to your Rayyan account.

To get the authenticated user info:

```python
user = rayyan.user.get_info()
```

## Documentation

The full documentation for Rayyan Python SDK is available on
[GitHub](https://github.com/rayyansys/rayyan-api-py/tree/master/docs).
You can also find a Juptyer notebook with examples here: `rayyan-api.ipynb`.

## Development

To build Rayyan Python SDK from source, execute the following command in a terminal:

```shell
git clone https://github.com/rayyansys/rayyan-api-py
cd rayyan-api-py
python setup.py develop
```

## Support

If you have any questions or problems with the SDK,
please create an issue on [GitHub](https://github.com/rayyansys/rayyan-api-py).
For questions about Rayyan itself, please use the Rayyan [Help Center](https://help.rayyan.ai/).
