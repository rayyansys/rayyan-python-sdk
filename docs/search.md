# Search Class

The `Search` class provides methods to interact with search-related functionality in the Rayyan API.

## Constructor

### `__init__(self, rayyan: Rayyan) -> None`

Creates an instance of the `Search` class.

#### Parameters

- `rayyan` (Rayyan): An instance of the `Rayyan` class.

#### Example Usage

```python
from rayyan import Rayyan
from rayyan.search import Search

rayyan = Rayyan(credentials_file_path="cred.json")
search_instance = Search(rayyan)
```

## Methods

### `pre_signed_url(self,review_id) -> dict`

generating a pre-signed URL to upload searches to S3.

The validity of the URL is one hour from time of creation. Additionally, multiple files can be uploaded to the same pre-signed URL where it acts as a prefix (folder).

#### Example Usage

```python
pre_signed_url = search_instance.pre_signed_url(1)
```


### `upload_search_file(self,key: str,credential: str,algorithm: str,date: str,signature: str,policy: str,success_action_status: int,url: str,file: str) -> dict`

upload a search file to S3 using the data you got from pre_signed_url method

#### Example Usage

```python
upload_search_file = search_instance.upload_search_file(key: str,credential: str,algorithm: str,date: str,signature: str,policy: str,success_action_status: int,url: str,file: str)
```

### `create(self, review_id: int, s3_key: str, original_filename: str) -> dict`

creates a search on the backend and kick-starts a job that parses the search file for articles.
the s3_key is the same key that you get from the upload_search_file method

#### Example Usage

```python
search = search_instance.create(review_id: int, s3_key: str, original_filename: str)
```
### `delete(self, review_id: int, id: int) -> dict`

used to delete a search. Specify the id of the search to delete in the URL.
you can get the id from the create method response

#### Example Usage

```python
search = search_instance.delete(review_id: int, id: int)
```
