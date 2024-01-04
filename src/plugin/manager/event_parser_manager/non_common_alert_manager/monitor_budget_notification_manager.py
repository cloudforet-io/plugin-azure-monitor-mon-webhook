import logging
import json
from datetime import datetime

from spaceone.core import utils
from plugin.manager.event_parser_manager.base_manager import EventParserManager

_LOGGER = logging.getLogger("spaceone")


class BudgetNotificationManager(EventParserManager):

    schema_id = "AIP Budget Notification"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:

        response = {
            "event_key": utils.datetime_to_iso8601(datetime.utcnow()),
            "event_type": "ALERT",
            "title": data.get("BudgetName"),
            "description": self.make_description(data),
            "severity": "ERROR",
            "resource": self.get_resource_info(data),
            "rule": data.get("BudgetName"),
            "image_url": "",
            "occurred_at": utils.datetime_to_iso8601(datetime.utcnow()),
            "additional_info": {},
        }
        return [response]

    @staticmethod
    def make_description(data: dict) -> str:
        return f"{json.dumps(data, indent=2)}"

    @staticmethod
    def get_resource_info(data: dict) -> dict:
        return {
            "name": data.get("BudgetName"),
            "resource_type": data.get("BudgetType")
        }
