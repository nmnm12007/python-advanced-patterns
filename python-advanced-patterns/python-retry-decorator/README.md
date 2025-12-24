## Retry Decorator with Idempotency

### Features

- Retry on specific exceptions
- Exponential backoff
- Idempotency enforcement
- Pluggable callbacks

### Usage

```python
@retry(
    retries=4,
    retry_on=(ValueError,),
    idempotent=True
)
def flaky():
    ...
````

### Design Notes

* Callbacks follow Strategy Pattern
* Safe for production workloads

```
