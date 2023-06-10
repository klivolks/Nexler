# AWSEmailService User Documentation

## Overview

AWSEmailService is an email service tool. It uses Amazon Web Services (AWS) Simple Email Service (SES) to send emails and manage contact lists.

## Setup

Before you can use AWSEmailService, you need to set up AWS Access Key ID, Secret Access Key, and the AWS Region in the `.env` file. These credentials are used to authenticate requests to the AWS SES API.

## Classes and Methods

AWSEmailService provides several methods:

- `send_email`: This method sends an email to the `receiver_email` provided. It can send both text and HTML emails based on the `email_type` property. If `template_name` is provided, it will read the respective template file, replace shortcodes with provided values, and send it as the email body.

- `create_contact_list`: This method creates a new contact list with the provided `contact_list_name`.

- `add_contact_to_list`: This method adds a new contact to an existing contact list. It needs `contact_list_name`, `contact_email`, and optionally the `contact_first_name` and `contact_last_name`.

Each of these methods takes various arguments that guide the email sending or contact management process.

## Usage

First, initialize an `AWSEmailService` instance:

```python
service = AWSEmailService()
```

Set the sender email, receiver email, subject, and body properties as needed:

```python
service.sender_email = "no-reply@example.com"
service.receiver_email = "user@example.com"
service.subject = "Subject of the email"
service.body = "Body of the email"
```

Call the appropriate method for your task:

```python
# To send an email
response = service.send_email()

# To create a new contact list
service.create_contact_list('TestContactList')

# To add a contact to a list
service.add_contact_to_list('TestContactList', 'newcontact@example.com', 'FirstName', 'LastName')
```

## Considerations

The AWS SES service has various quotas and restrictions, such as a maximum sending rate and a verification requirement for the sender and receiver email addresses in a sandbox environment. Always make sure to comply with these requirements to prevent issues with the email sending and contact list management.

Additionally, ensure that you use the correct AWS credentials and region to successfully connect to the AWS SES API. Remember that AWS credentials should be kept secure and not shared or exposed publicly. 

Email content should always be formatted correctly, especially for HTML emails, to ensure that they are displayed correctly in all email clients. Consider testing the email sending feature and verifying the email content in various email clients.