import logging

from plugin.manager.event_parser_manager.base_manager import EventParserManager

_LOGGER = logging.getLogger("spaceone")


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
            "title": self.make_title(essentials),
            "description": self.make_description(essentials),
            "severity": self.get_severity(essentials.get("severity", "")),
            "resource": self.get_resource_info(essentials),
            "rule": essentials.get("alertRule"),
            "image_url": "",
            "occurred_at": essentials.get("firedDateTime"),
            "additional_info": custom_properties,
        }
        return [response]

    @staticmethod
    def make_title(essentials: dict) -> str:
        return f"{essentials.get('alertRule')}"

    @staticmethod
    def get_affected_resource(essentials: dict) -> str:
        resource = essentials.get("configurationItems")[0] if len(essentials.get("configurationItems")) > 0 else ""

        return resource

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
    def get_alert_target(alert_target_id: str) -> dict:
        """

        Args:
            alert_target_id:
             /subscriptions/xxxx/resourcegroups/xxxx/providers/microsoft.compute/virtualmachines/xxxx

        Returns:
            subscriptions : "xxx"
            resourcegroups: "xxx"
            providers: "xxx"
            {service}: "xxxx"
            {name}: "xxxxx"

        """
        target: list = alert_target_id.split("/")[1:]
        k: list = []
        v: list = []
        for i, t in enumerate(target):
            k.append(t) if i % 2 == 0 else v.append(t)

        return dict(zip(k, v))

    def make_description(self, essentials: dict) -> str:
        alert_target = self.get_resource(essentials.get("alertTargetIDs")[0])

        return (f"- Alert name: {essentials.get('alertRule')}\n"
                f"- Severity: {essentials.get('severity')}\n"
                f"- Monitor condition: {essentials.get('monitorCondition')}\n"
                f"- Affected resource: {self.get_affected_resource(essentials)}\n"
                f"- Resource group: {alert_target.get('resourcegroups')}\n"
                f"- Description: {essentials.get('description')}\n"
                f"- Monitoring service: {essentials.get('monitoringService')}\n"
                f"- Signal type: {essentials.get('signalType')}\n"
                f"- Fired time: {essentials.get('firedDateTime')}\n"
                f"- Alert ID: {essentials.get('alertId')}\n")
