# APIService `User Documentation`

## Overview

`APIService` is a set of classes (`ApiService`, `ExternalApi`, and `InternalApi`) that allow interaction with internal and external APIs, as well as API request validation. 

### Importing

You can import the classes as follows:

```python
from nexler.services import ApiService, ExternalApi, InternalApi
```

## ApiService

This class provides methods for verifying API requests. It maintains a count of the monthly access per referer and verifies that the number of requests does not exceed the set limit.

### Usage

```python
from nexler.services import ApiService

api_service = ApiService()
is_verified = api_service.verified
```

### Properties and Methods

- `verified`: a boolean property that verifies if the request is allowed or not.
- `verify_request()`: verifies the API key and referer from the request. It also checks the monthly access limit for the referer.

## ExternalApi

This class is for making HTTP requests to external APIs. The function is asynchronous. So usage is a little bit different

### Usage

```python
import asyncio
from nexler.services import ExternalApi

external_api = ExternalApi("http://api.example.com")
data = asyncio.run(external_api.fetch("get"))
```

### Properties and Methods

- `fetch(method)`: makes an HTTP request using the specified method (`'get'`, `'post'`, `'put'`, or `'delete'`). It JSON-encodes the data if the content type is 'application/json'.
- `parse_response()`: parses the response of the HTTP request. It treats any status code from 200 to 299 as a success.

## InternalApi

This class is for making HTTP requests to internal APIs. It extends `ExternalApi` class. For making internal apis gateway components should be described in `.env` as in .env-example
If another internal service is used you should have a `service-name.json` in `app/config` folder. The file should be like below.

```json
{
  "API_KEY": "my-api-key",
  "API_URL": "my-internal-api-url built according to nexler API concept"
}
```

### Usage

```python
import asyncio
from nexler.services import InternalApi

internal_api = InternalApi(service='gateway', path="")
data = asyncio.run(internal_api.fetch("get"))
```

### Properties and Methods

- Inherits all properties and methods from `ExternalApi`.
- When instantiated, the constructor accepts an optional `service` argument (defaulting to `'gateway'`). Based on the provided service, it sets up the headers and URL for API requests.
