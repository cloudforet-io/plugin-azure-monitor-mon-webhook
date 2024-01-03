from plugin.manager.event_parser_manager.base_manager import EventParserManager
from abc import ABCMeta


class MonitorMetricAlertManager(EventParserManager):
    schema_id = "AzureMonitorMetricAlert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:
        context = data.get("context")
        response = {
            "event_key": f"{context.get('id')}:{context.get('timestamp')}",
            "event_type": "ALERT",
            "title": context.get("name"),
            "description": data.get("description"),
            "severity": self.get_severity(context.get("severity", "")),
            "resource": self.get_resource_info(context),
            "rule": context.get("name"),
            "image_url": context.get("portalLink", ""),
            "occurred_at": context.get("timestamp"),
            "additional_info": self.get_additional_info(context.get("condition", {})),
        }
        return [response]

    @staticmethod
    def get_additional_info(condition: dict) -> dict:
        additional_info = {}
        if all_of := condition.get("allOf"):
            additional_info["all_of"] = all_of
        if condition_type := condition.get("conditionType"):
            additional_info["condition_type"] = condition_type
        return additional_info

    @staticmethod
    def get_resource_info(context: dict) -> dict:
        resource_info = {}

        if resource_id := context.get("resourceId"):
            resource_info["resource_id"] = resource_id

        if resource_name := context.get("resourceName"):
            resource_info["name"] = resource_name

        if resource_type := context.get("resourceType"):
            resource_info["resource_type"] = resource_type

        return resource_info

    @staticmethod
    def _get_resource_type_from_resource_id(resource_id: str) -> str:
        return resource_id.split("/")[5]

    @staticmethod
    def get_severity(origin_severity: str) -> str:
        if origin_severity.lower() == "0":
            return "CRITICAL"
        elif origin_severity.lower() == "1":
            return "ERROR"
        elif origin_severity.lower() == "2":
            return "WARNING"
        elif origin_severity.lower() == "3":
            return "INFO"
        elif origin_severity.lower() == "4":
            return "NONE"
        else:
            return "UNKNOWN"
