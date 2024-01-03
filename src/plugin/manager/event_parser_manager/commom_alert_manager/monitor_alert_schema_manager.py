from plugin.manager.event_parser_manager.base_manager import EventParserManager
from abc import ABCMeta


class MonitorAlertSchemaManager(EventParserManager):
    schema_id = "azureMonitorCommonAlertSchema"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_parse(self, options, data) -> list:
        essentials = data.get("essentials")
        response = {
            "event_key": essentials.get("alertId"),
            "event_type": self.get_event_status(essentials.get("monitorCondition")),
            "title": essentials.get("alertRule"),
            "description": essentials.get("description"),
            "severity": self.get_severity(essentials.get("severity", "")),
            "resource": self.get_resource_info(essentials),
            "rule": essentials.get("alertRule"),
            "occurred_at": essentials.get("firedDateTime"),
            "additional_info": self.get_additional_info(data),
        }
        return [response]

    @staticmethod
    def get_additional_info(data: dict) -> dict:
        additional_info = {}
        if affected_resource := data.get("essentials").get("alertTargetIDs"):
            additional_info["affected_resource"] = affected_resource
        if alert_context := data.get("alertContext"):
            additional_info["alert_context"] = alert_context
        return additional_info

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
            return "NONE"
        else:
            return "UNKNOWN"
