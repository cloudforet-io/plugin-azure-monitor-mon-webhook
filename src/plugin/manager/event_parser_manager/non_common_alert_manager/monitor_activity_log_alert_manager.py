import json
from typing import List
from datetime import datetime

from spaceone.core import utils
from plugin.manager.event_parser_manager.base_manager import EventParserManager


class MonitorActivityLogAlertManager(EventParserManager):

    schema_id = "Microsoft.Insights/activityLogs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:

        activity_log = data.get("context", {}).get("activityLog", {})

        response = {
            "event_key": activity_log.get("eventDataId", ""),
            "event_type": self.get_event_type(data.get("status")),
            "title": self.get_title(activity_log),
            "description": self.make_description(data),
            "severity": self.get_severity(activity_log),
            "resource": self.get_resource_info(activity_log),
            "rule": activity_log.get("operationName"),
            "image_url": "",
            "occurred_at": activity_log.get("eventTimestamp"),
            "additional_info": self.get_additional_info(data),
        }
        return [response]

    @staticmethod
    def get_title(activity_log: dict) -> str:
        return activity_log.get("operationName")

    @staticmethod
    def get_event_type(status: str) -> str:
        """

        Args:
            status:
            - Deactivated
            - Activated
        Returns:
            - ALERT
            - RECOVERY
        """
        if status == "Deactivated":
            return "RECOVERY"
        else:
            return "ALERT"


    @staticmethod
    def make_description(activity_log: dict) -> str:
        description = activity_log.get("Description")

        return f"Description: {description}\nActivityLog: {json.dumps(activity_log, indent=2)}"

    @staticmethod
    def get_severity(activity_log: dict) -> str:
        if activity_log.get("level") == "Informational":
            return "INFO"
        elif activity_log.get("level") == "Warning":
            return "WARNING"
        elif activity_log.get("level") == "Error":
            return "ERROR"
        elif activity_log.get("level") == "CRITICAL":
            return "CRITICAL"

        return "NOT_AVAILABLE"

    @staticmethod
    def get_resource_info(activity_log: dict) -> dict:
        return {
            "resource_id": activity_log.get("resourceId"),
            "name": activity_log.get("resourceId"),
            "resource_type": activity_log.get("resourceType")
        }

    @staticmethod
    def get_additional_info(data: dict) -> dict:
        additional_info = {}
        additional_info.update(data.get("context", {}).get("activityLog", {}).get("properties", {}))
        additional_info.update(data.get("properties", {}))

        return additional_info


