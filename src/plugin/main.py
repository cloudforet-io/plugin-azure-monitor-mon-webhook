import logging
from typing import Dict

from spaceone.monitoring.plugin.webhook.lib.server import WebhookPluginServer
from .manager.event_parser_manager.base_manager import EventParserManager

_LOGGER = logging.getLogger("spaceone")

app = WebhookPluginServer()


@app.route("Webhook.init")
def webhook_init(params: dict) -> dict:
    """init plugin by options

    Args:
        params (WebhookInitRequest): {
            'options': 'dict'      # Required
        }

    Returns:
        WebhookResponse: {
            'metadata': 'dict'
        }
    """
    return {}


@app.route("Webhook.verify")
def webhook_verify(params: dict) -> None:
    """Verifying webhook plugin

    Args:
        params (WebhookVerityRequest): {
            'options': 'dict',      # Required
            'secret_data': 'dict',  # Required
            'schema': 'str',
            'domain_id': 'str'      # Required
        }

    Returns:
        None
    """
    pass


@app.route("Event.parse")
def event_parse(params: dict) -> Dict[str, list]:
    """Parsing Event Webhook

    Args:
        params (EventRequest): {
            'options': 'dict',  # Required
            'data': 'dict'      # Required
        }

    Returns:
        Dict(EventsResponse)
        {
            results: List[EventResponse]
                'event_key': 'str',         # Required
                'event_type': 'str',        # Required
                'title': 'str',
                'description': 'str',
                'severity': 'str',
                'resource': 'dict',
                'rule': 'str',              # Required
                'occurred_at': 'datetime',  # Required
                'additional_info': 'dict',
                'image_url': 'str'
        }
    """
    data = params["data"]
    options = params["options"]

    # schemaId is now exists some cases

    if data.get("schemaId") is None:
        data["schemaId"] = "MonitorActivityLogAlert"

    event_parse_mgr = EventParserManager.get_manager_by_schema_id(data["schemaId"])

    event_responses = {}

    if data["schemaId"] == "MonitorActivityLogAlert":
        event_responses.update(
            {"results": event_parse_mgr.event_parse(options=options, data=data)}
        )
    else:
        event_responses.update(
            {
                "results": event_parse_mgr.event_parse(
                    options=options, data=data.get("data", {})
                )
            }
        )

    return event_responses
