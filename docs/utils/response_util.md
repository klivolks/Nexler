# `response_util.py` User Documentation

The `response_util.py` module provides a set of utility functions to return HTTP responses with appropriate status codes. This helps to ensure consistency in the way your application responds to requests. Here are the details of each function:

## Functions

- **check_data(data)**: This function checks if the provided data is of type dict or list. If not, it raises a TypeError.

### Success Responses

- **success(data, status_code=200)**: Returns a success response with provided data and a 200 status code.

- **created(data, status_code=201)**: Returns a success response indicating that the resource was successfully created. It returns a 201 status code and the created resource as data.

- **accepted(data=None, status_code=202)**: Returns a success response indicating that the request has been accepted for processing, but the processing has not been completed. The function optionally takes a data parameter that it includes in the response.

- **no_content(status_code=204)**: Returns a success response with a 204 status code indicating that the request has been successfully processed and there is no additional content to send in the response.

### Error Responses

- **error(message, status_code=400)**: Returns an error response with a provided message and a 400 status code.

- **bad_request(message='Bad Request')**: Returns a 400 error response indicating a bad request. The function takes an optional message parameter that defaults to 'Bad Request'.

- **unauthorized(message='Unauthorized')**: Returns a 401 error response indicating that the request requires user authentication. The function takes an optional message parameter that defaults to 'Unauthorized'.

- **forbidden(message='Forbidden')**: Returns a 403 error response indicating that the server understood the request, but it refuses to authorize it. The function takes an optional message parameter that defaults to 'Forbidden'.

- **not_found(message='Not found')**: Returns a 404 error response indicating that the server could not find the requested resource. The function takes an optional message parameter that defaults to 'Not found'.

- **method_not_allowed(message='Method not allowed')**: Returns a 405 error response indicating that the method specified in the request is not allowed for the resource identified by the request URI. The function takes an optional message parameter that defaults to 'Method not allowed'.

- **conflict(message='Conflict')**: Returns a 409 error response indicating that the request could not be completed due to a conflict with the current state of the resource. The function takes an optional message parameter that defaults to 'Conflict'.

- **unsupported_media_type(message='Unsupported Media Type')**: Returns a 415 error response indicating that the request's media type is not supported by the server or resource. The function takes an optional message parameter that defaults to 'Unsupported Media Type'.

- **server_error(message='Internal Server Error')**: Returns a 500 error response indicating an internal server error. The function takes an optional message parameter that defaults to 'Internal Server Error'.

- **not_implemented(message='Not Implemented')**: Returns a 501 error response indicating that the server does not support the functionality required to fulfill the request. The function takes an optional message parameter that defaults to 'Not Implemented'.

## Usage

To use these utility functions, simply import the required functions from the `app.utils.response_util` module and use them in your code where needed.

For example:

```python
from app.utils.response_util import success, bad_request

def get(self):
    try:
        data = retrieve_data()  # some function to retrieve data
        return success(data)
    except Exception as e:
        return bad_request(str(e))
```

In this example, the `success` function is used to return the retrieved data with a 

200 status code. If an exception is raised during data retrieval, the `bad_request` function is used to return an error message with a 400 status code.