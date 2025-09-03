from plugin.manager.event_parser_manager.commom_alert_manager.monitor_alert_schema_manager import (
    MonitorAlertSchemaManager,
)


class PlatformManager(MonitorAlertSchemaManager):
    monitoring_service = "Platform"

    def event_parse(self, options: dict, data: dict) -> list:
        essentials: dict = data.get("essentials")
        alert_context: dict = data.get("alertContext")
        custom_properties = data.get("customProperties")

        response = {
            "event_key": essentials.get("alertId"),
            "event_type": self.get_event_status(essentials.get("monitorCondition")),
            "title": self.make_title(essentials),
            "description": self.make_description(essentials),
            "severity": self.get_severity(essentials.get("severity", "")),
            "resource": self.get_resource_info(essentials),
            "rule": essentials.get("alertRule"),
            "occurred_at": essentials.get("firedDateTime"),
            "additional_info": self.make_common_additional_info(
                alert_context, custom_properties
            ),
        }

        return [response]
