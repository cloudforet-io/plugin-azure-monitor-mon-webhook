import logging
from datetime import datetime

from spaceone.core import utils
from plugin.manager.event_parser_manager.base_manager import EventParserManager

_LOGGER = logging.getLogger("spaceone")


class LogAlertManager(EventParserManager):

    schema_id = "MonitorActivityLogAlert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:

        response = {
            "event_key": self.get_event_key(data),
            "event_type": "ALERT",
            "title": data.get("AlertRuleName"),
            "description": self.make_description(data),
            "severity": self.get_severity(data.get("Severity")),
            "resource": self.get_resource_info(data),
            "rule": data.get("SearchQuery"),
            "image_url": data.get("LinkToSearchResults", ""),
            "occurred_at": utils.datetime_to_iso8601(datetime.utcnow()),
            "additional_info": {},
        }
        return [response]

    @staticmethod
    def get_event_key(data: dict) -> str:
        alert_rule_name = data.get("AlertRuleName")

        return f"{alert_rule_name}-{datetime.utcnow()}"

    @staticmethod
    def make_description(data: dict) -> str:
        description = data.get("Description")

        return f"Description: {description}\nSearchResult: {data.get('SearchResult')}"

    @staticmethod
    def get_severity(severity: str) -> str:
        if severity == "0":
            return "CRITICAL"
        elif severity == "1":
            return "ERROR"
        elif severity == "2":
            return "WARNING"
        elif severity == "3":
            return "INFO"
        elif severity == "4":
            return "INFO"
        else:
            return "NOT_AVAILABLE"

    @staticmethod
    def get_resource_info(data: dict) -> dict:
        return {
            "resource_id": data.get("ResourceId"),
            "name": data.get("ResourceId")
        }

