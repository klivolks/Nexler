# TextLocal User Documentation

## Overview

TextLocal is a messaging service tool that sends SMS (Short Message Service) messages using the TextLocal SMS API. 

## Setup

Before you can use TextLocal, you need to set up the TextLocal API Key in the configuration file or `.env` file. This API Key is used to authenticate requests to the TextLocal API.

## Class and Methods

TextLocal provides a method:

- `send_sms`: This method sends an SMS to the phone number specified. If a `template` is provided during the initialization of the class, it will read the respective template file, replace shortcodes with provided values, and send it as the SMS body.

This method takes various arguments that guide the SMS sending process.

## Usage

First, initialize a `TextLocal` instance:

```python
sms = TextLocal(template='otp', sender='EXMPLE', phone=9847402244)
```
The `template` parameter corresponds to the template file that will be used to compose the message, the `sender` parameter sets the sender ID for the message, and the `phone` parameter is the phone number to which the message will be sent. 

Next, call the `send_sms` method and provide the dynamic content for the message:

```python
result = sms.send_sms(otp=123456, expiry=10)
```

The `send_sms` method replaces placeholders (like `{otp}` and `{expiry}`) in the template file with the provided values.

## Considerations

The TextLocal SMS service has various quotas and restrictions, such as a maximum sending rate. Make sure to comply with these requirements to prevent issues with the SMS sending.

Also, ensure that you use the correct TextLocal API Key to successfully connect to the TextLocal API. Remember that the API Key should be kept secure and not shared or exposed publicly. 

SMS content should always be formatted correctly to ensure that they are displayed correctly on all devices. Consider testing the SMS sending feature and verifying the SMS content on various devices.
