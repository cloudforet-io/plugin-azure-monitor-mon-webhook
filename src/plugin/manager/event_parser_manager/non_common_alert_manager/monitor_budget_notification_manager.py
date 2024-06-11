import logging
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
            "title": self.make_title(data),
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
    def make_title(data: dict) -> str:
        return f"Budget Alarm {data.get('BudgetName')}"

    @staticmethod
    def make_description(data: dict) -> str:
        return (
            f"- Budget name: {data.get('BudgetName')}\n"
            f"- Budget type: {data.get('BudgetType')}\n"
            f"- Account name: {data.get('AccountName')}\n"
            f"- Department name: {data.get('DepartmentName')}\n"
            f"- Enrollment number: {data.get('EnrollmentNumber')}\n"
            f"- Notification threshold: {data.get('NotificationThresholdAmount')}\n"
            f"- Budget: {data.get('Budget')}\n"
            f"- Unit: {data.get('Unit')}\n"
            f"- Cost: {data.get('SpendingAmount')}"
            f"- Resource group: {data.get('ResourceGroup')}\n"
            f"- Fired time: {datetime.utcnow()}\n"
        )

    @staticmethod
    def get_resource_info(data: dict) -> dict:
        return {"name": data.get("BudgetName"), "resource_type": data.get("BudgetType")}
