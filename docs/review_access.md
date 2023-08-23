# ReviewAccess Class Documentation

The `ReviewAccess` class offers methods to control access to reviews in the Rayyan system.

## Constructor

### `ReviewAccess(rayyan: Rayyan)`

Create a new `ReviewAccess` instance.

- `rayyan` (type: Rayyan): The Rayyan instance used for making requests.

**Example**:

```python
from rayyan import Rayyan
from rayyan.review import Review

rayyan = Rayyan(credentials_file_path="cred.json", url="https://staging.rayyan.ai")
review_instance = Review(rayyan)
```

## Methods

### `delete_access(id: int, user_id: int) -> dict`

Delete access for a user from a specific review.

- `id` (type: int): The review identifier.
- `user_id` (type: int): The ID of the user whose access needs to be revoked.

**Returns**: A dictionary confirming the deletion of access.

**Example**:

```python
delete_confirmation = review_access_instance.delete_access(id=123, user_id=456)
print(delete_confirmation)
```

### `update_access(id: int, role_id: int, user_emails: list) -> dict`

Update access roles for multiple users in a review.

- `id` (type: int): The review identifier.
- `role_id` (type: int): The ID of the new role to assign to users.
- `user_emails` (type: list): List of user emails to update.

**Returns**: A dictionary confirming the update of access.

**Example**:

```python
update_confirmation = review_access_instance.update_access(id=123, role_id=789, user_emails=["user1@example.com", "user2@example.com"])
print(update_confirmation)
```

### `invite(id: int, user_id: int, user_emails: list, user_reason: str) -> dict`

Invite users to collaborate on a review.

- `id` (type: int): The review identifier.
- `user_id` (type: int): The ID of the user initiating the invitation.
- `user_emails` (type: list): List of user emails to invite.
- `user_reason` (type: str): The reason for inviting users.

**Returns**: A dictionary confirming the invitation.

**Example**:

```python
invite_confirmation = review_access_instance.invite(id=123, user_id=456, user_emails=["user3@example.com"], user_reason="Collaboration on data analysis.")
print(invite_confirmation)
```

### `revoke(id: int, user_id: int) -> dict`

Revoke a user's access to a specific review.

- `id` (type: int): The review identifier.
- `user_id` (type: int): The ID of the user whose access needs to be revoked.

**Returns**: A dictionary confirming the access revocation.

**Example**:

```python
revoke_confirmation = review_access_instance.revoke(id=123, user_id=456)
print(revoke_confirmation)
```
