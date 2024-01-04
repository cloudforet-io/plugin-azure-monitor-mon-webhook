import json
from plugin.manager.event_parser_manager.base_manager import EventParserManager


class MonitorAlertSchemaManager(EventParserManager):
    schema_id = "azureMonitorCommonAlertSchema"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:
        essentials = data.get("essentials")
        alert_context = data.get("alertContext")
        custom_properties = data.get("customProperties")

        response = {
            "event_key": essentials.get("alertId"),
            "event_type": self.get_event_status(essentials.get("monitorCondition")),
            "title": essentials.get("alertRule"),
            "description": self.make_description(essentials.get("description"), alert_context),
            "severity": self.get_severity(essentials.get("severity", "")),
            "resource": self.get_resource_info(essentials),
            "rule": essentials.get("alertRule"),
            "image_url": "",
            "occurred_at": essentials.get("firedDateTime"),
            "additional_info": custom_properties,
        }
        return [response]

    @staticmethod
    def get_resource_info(essentials: dict) -> dict:
        resource_name = essentials.get("configurationItems")[0]
        return {
            "name": resource_name,
        }

    @staticmethod
    def _get_resource_type_from_resource_id(resource_id: str) -> str:
        return resource_id.split("/")[5]

    @staticmethod
    def get_event_status(origin_status: str) -> str:
        if origin_status.lower() == "fired":
            return "ALERT"
        elif origin_status.lower() == "resolved":
            return "RECOVERY"

    @staticmethod
    def get_severity(origin_severity: str) -> str:
        if origin_severity.lower() == "sev0":
            return "CRITICAL"
        elif origin_severity.lower() == "sev1":
            return "ERROR"
        elif origin_severity.lower() == "sev2":
            return "WARNING"
        elif origin_severity.lower() == "sev3":
            return "INFO"
        elif origin_severity.lower() == "sev4":
            return "INFO"
        else:
            return "NOT_AVAILABLE"

    @staticmethod
    def make_description(description: str, alert_context: dict) -> str:
        tmp_description = json.dumps(alert_context, indent=2)

        return f"Description: {description}\nAlertContext: {tmp_description}"
