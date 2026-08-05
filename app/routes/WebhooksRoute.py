from email.policy import default

from flask_restx import Api, fields, Namespace
from app.components import Webhooks

webhooks_namespace = Namespace('webhooks', 'Edit routes to add description')


def register(api: Api):
    api.add_namespace(webhooks_namespace)
    webhooks_namespace.add_resource(Webhooks, '/webhooks/kgate')

    payload_model = api.model('WebhookPayload', {
        "event": fields.String(required=False, description="event name"),
        "data": fields.Raw(required=False, description="event data")
    })

    post_request_model = api.model('WebhooksPostPayload', {
        "Type": fields.String(
            required=True,
            description='type of event',
            default='event'
        ),
        "Channel": fields.String(
            required=True,
            description='channel name'
        ),
        "MessageID": fields.String(
            required=True,
            description='message id'
        ),
        "Payload": fields.Nested(
            payload_model,
            required=True,
            description='payload'
        ),
        "Timestamp": fields.DateTime(
            required=True,
            description='timestamp'
        )
    })

    # Register models with API
    api.add_model('WebhooksPostRequest', post_request_model)
    