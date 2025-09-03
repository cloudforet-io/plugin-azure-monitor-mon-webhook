import logging

from plugin.manager.event_parser_manager.base_manager import EventParserManager

_LOGGER = logging.getLogger("spaceone")


class MonitorMetricAlertManager(EventParserManager):
    schema_id = "AzureMonitorMetricAlert"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:
        context = data.get("context")

        condition = context.get("condition")
        properties = data.get("properties", {})

        response = {
            "event_key": context.get("id"),
            "event_type": self.get_event_status(data.get("status")),
            "title": self.make_title(context),
            "description": self.make_description(data),
            "severity": self.get_severity(context.get("severity", "")),
            "resource": self.get_resource_info(context),
            "rule": context.get("name"),
            "image_url": context.get("portalLink", ""),
            "occurred_at": context.get("timestamp"),
            "additional_info": self.make_additional_info_from_condition(
                condition, properties
            ),
        }
        return [response]

    @staticmethod
    def make_title(context: dict) -> str:
        return f"{context.get('name')}"

    @staticmethod
    def make_description(data: dict) -> str:
        context = data.get("context", {})

        return (
            f"- Alert name: {context.get('name')}\n"
            f"- Severity: {context.get('severity')}\n"
            f"- Status: {data.get('status')}\n"
            f"- Resource name: {context.get('resourceName')}\n"
            f"- Resource type: {context.get('resourceType')}\n"
            f"- Resource group: {context.get('resourceGroupName')}\n"
            f"- Description: {context.get('description')}\n"
            f"- Condition type: {context.get('conditionType')}\n"
            f"- Fired time: {context.get('timestamp')}\n"
            f"- Alert ID: {context.get('id')}\n"
        )

    @staticmethod
    def get_event_status(status: str) -> str:
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

    @staticmethod
    def make_additional_info_from_condition(condition: dict, properties: dict) -> dict:
        additional_info = {}

        if condition:
            additional_info["condition"] = condition

        if properties:
            additional_info.update(properties)

        return additional_info
