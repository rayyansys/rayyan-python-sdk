# Rayyan Python SDK

A Python SDK for [Rayyan](https://www.rayyan.ai/), the popular systematic reviews platform.
It is a wrapper around the [HTTP APIs](https://github.com/rayyansys/rayyan-api-docs) of Rayyan.
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
You can retrieve such file by signing in to your Rayyan account
(create a free account if you don't have one) and visiting My Account page.

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

The full documentation for Rayyan Python SDK is available in the
[docs](https://github.com/rayyansys/rayyan-python-sdk/tree/master/docs) folder on GitHub.
You can also find a Juptyer notebook with examples in
[rayyan-api.ipynb](https://github.com/rayyansys/rayyan-python-sdk/blob/master/rayyan-api.ipynb).

## Development

To build Rayyan Python SDK from source, execute the following command in a terminal:

```shell
git clone https://github.com/rayyansys/rayyan-python-sdk
cd rayyan-python-sdk
python setup.py develop
```

## Support

If you have any questions or problems with the SDK,
please check existing issues on [GitHub](https://github.com/rayyansys/rayyan-python-sdk/issues),
or open a new issue if needed.
For questions about Rayyan itself, please use the Rayyan [Help Center](https://help.rayyan.ai/).
