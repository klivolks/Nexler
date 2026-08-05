````markdown
## kGate Service Documentation

This documentation provides guidance on setting up and using the kGate service in a Python-based application. The kGate service provides real-time messaging capabilities through WebSocket connections and HTTP APIs.

The service allows applications to:

- Subscribe to kGate messenger channels
- Receive messages automatically in the background
- Dispatch received events to application handlers
- Publish messages to channels
- Receive webhook notifications for failed message delivery

---

## Enabling kGate in the Application

To enable kGate, add the following configuration to your environment settings (e.g., `.env` file or environment variables):

```ini
# kGate Configuration
KGATE_WS_URL=ws://localhost:8080
KGATE_HTTP_URL=http://localhost:8080
KGATE_CLIENT_ID=your-client-id
SERVICE_NAME=my-service
````

### Configuration Parameters

* `KGATE_WS_URL`

  * WebSocket endpoint of the kGate messenger service.
  * Used for subscribing and receiving real-time messages.

* `KGATE_HTTP_URL`

  * HTTP endpoint of the kGate service.
  * Used for publishing messages.

* `KGATE_CLIENT_ID`

  * Client identifier issued by kGate.
  * Used for authentication.

* `SERVICE_NAME`

  * Name of the application using kGate.
  * Sent as the request origin for identification.

---

# KGateService Class

The `KGateService` class provides communication between a Python application and kGate messenger.

It handles:

* WebSocket connection management
* Channel subscriptions
* Message receiving
* Automatic acknowledgement
* HTTP message publishing

---

## KGateService Initialization

The service automatically loads configuration when initialized.

Example:

```python
from nexler.services import KGateService

kgate = KGateService()
```

---

# Subscribe to Channel

### `subscribe(channel)`

Creates a WebSocket connection and listens continuously for messages from a channel.

Parameters:

* `channel`

  * Name of the kGate messenger channel to subscribe.

Example:

```python
await kgate.subscribe("notifications")
```

Once subscribed, the service automatically waits for incoming messages.

Example received message:

```json
{
    "type": "event",
    "channel": "notifications",
    "message_id": "msg_12345",
    "payload": {
        "user_id": "100",
        "message": "Welcome"
    },
    "timestamp": 1720000000
}
```

The service performs:

1. Receive message from kGate
2. Dispatch message payload
3. Send acknowledgement to kGate

---

# Message Dispatch

Received messages are passed to the application using:

```python
despatch(channel, payload)
```

The dispatch function allows applications to handle different channels independently.

Example:

```python
def despatch(channel, payload):

    if channel == "email":
        process_email(payload)

    elif channel == "notification":
        process_notification(payload)
```

Example:

```json
{
    "channel": "email",
    "payload": {
        "to": "user@example.com",
        "subject": "Welcome"
    }
}
```

---

# Running kGate Subscriber Automatically

For long-running applications such as Flask services, kGate subscriptions should run in a background thread.

Example:

```python
from threading import Thread
import asyncio


def consume_kgate_events():

    kgate = KGateService()

    async def runner():

        await asyncio.gather(
            kgate.subscribe("email"),
            kgate.subscribe("notification")
        )

    asyncio.run(runner())


def start_kgate():

    thread = Thread(
        target=consume_kgate_events,
        daemon=True
    )

    thread.start()
```

The subscriber:

* Starts with the application
* Maintains WebSocket connections
* Waits continuously for messages
* Automatically processes incoming events

---

# Publishing Messages

### `publish(channel, payload)`

Publishes a message to a kGate channel using HTTP.

Parameters:

* `channel`

  * Target messenger channel.

* `payload`

  * Message data.

Example:

```python
kgate.publish(
    "notification",
    {
        "title": "New User",
        "message": "User registered"
    }
)
```

Request:

```http
POST /messenger/publish
```

Headers:

```http
X-Client-Id: your-client-id
Origin: your-service-name
Content-Type: application/json
```

Body:

```json
{
    "channel": "notification",
    "payload": {
        "title": "New User",
        "message": "User registered"
    }
}
```

---

# Webhook Notifications

When kGate cannot deliver a message to an active subscriber, it can notify the application through a webhook endpoint.

Webhook payload:

```json
{
    "Type": "message.failed",
    "Channel": "notification",
    "MessageID": "msg_12345",
    "Payload": {
        "reason": "subscriber unavailable"
    },
    "Timestamp": "2026-08-05T20:00:00Z"
}
```

Applications can use this to:

* Retry delivery
* Store failed messages
* Notify administrators
* Trigger fallback processing

---

# Webhook Signature Validation

Webhook requests contain:

```http
X-Signature
```

The signature is generated using HMAC SHA256.

Example validation:

```python
import hmac
import hashlib


def verify_signature(secret, body, signature):

    expected = hmac.new(
        secret.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected,
        signature
    )
```

---

# Application Lifecycle

The recommended lifecycle:

```
Application Start
        |
        v
Initialize KGateService
        |
        v
Start Subscriber Thread
        |
        v
Connect WebSocket
        |
        v
Subscribe Channels
        |
        v
Wait For Messages
        |
        v
Dispatch Events
        |
        v
Acknowledge Messages
```

Shutdown:

```
SIGTERM / SIGINT
        |
        v
Stop Subscriber
        |
        v
Close WebSocket
```

---

# Troubleshooting

### HTTP 401 Unauthorized

Possible causes:

* Invalid `KGATE_CLIENT_ID`
* Client not registered in kGate
* Incorrect origin configuration

### WebSocket Connection Failed

Check:

* `KGATE_WS_URL`
* Network connectivity
* kGate messenger service status

### Messages Not Received

Verify:

* Channel name matches kGate configuration
* Client has permission for the channel
* Subscriber thread is running

### Webhook Not Triggered

Check:

* Webhook URL configuration
* Signature validation
* kGate connectivity

---

# Notes

1. **Persistent Connections**

kGate uses WebSocket connections for real-time delivery. The subscriber remains connected and waits for incoming messages.

2. **Message Acknowledgement**

Messages are acknowledged only after successful dispatch to the application.

3. **Scaling**

For multiple application instances:

* Use separate client IDs
* Subscribe only required channels
* Handle duplicate events if multiple consumers receive the same channel

4. **Production Deployment**

For Docker/Kubernetes:

* Start kGate subscriber with application startup
* Handle SIGTERM gracefully
* Use `wss://` and `https://` endpoints in production
* Store client credentials securely

---

This documentation covers the configuration, subscription model, publishing, webhook handling, and lifecycle management of the kGate Python service client.
