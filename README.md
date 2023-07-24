# Rayyan SDK

## Table of Contents

- [Rayyan SDK](#rayyan-sdk)
  - [Table of Contents](#table-of-contents)
  - [Docs](#docs)
  - [Build](#build)
  - [Installation](#installation)
  - [Usage](#usage)

## Docs

- [rayyan](/docs/rayyan.md)
- [user](/docs/user.md)

## Build

To Build Rayyan Python SDK, simply execute the following command
in a terminal using make file:

```shell
make build
```

or simply execute the following command
in a terminal

```shell
python setup.py sdist
```

## Installation

To install Rayyan Python SDK, simply execute the following command
in a terminal after you build the sdk first:

```shell
pip install ./dist/rayyan-sdk-0.1.tar.gz
```

## Usage

To use Rayyan Python SDK, you will need to have a credentials file in JSON format like the one below. You can retrieve such file by signing in to your Rayyan account and going to My Account page.

```json
// creds.json
{
    "access_token": "9c2b0fe74ab7cd8d1227cd2fd",
    "token_type": "bearer",
    "refresh_token": "b40e325a1a7f53831ec3c09fffc7"
}
```

Import Rayyan main class and pass the credentials file to it like this:

```python
rayyan = Rayyan("cred.json")
```

to get user info

```python
user = rayyan.user.get_info()
```
