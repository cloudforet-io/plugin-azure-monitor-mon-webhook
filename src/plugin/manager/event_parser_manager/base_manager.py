import logging
from abc import abstractmethod, ABC

from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger("spaceone")

class EventParserManager(BaseManager, ABC):
    schema_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def event_parse(self, **kwargs) -> dict:
        pass

    @classmethod
    def get_manager_by_schema_id(cls, schema_id: str):
        for sub_class in cls.__subclasses__():
            if sub_class.schema_id == schema_id:
                return sub_class()

    @staticmethod
    def get_resource(resource_id: str) -> dict:
        """

        Args:
            resource_id:
             /subscriptions/xxxx/resourcegroups/xxxx/providers/microsoft.compute/virtualmachines/xxxx

        Returns:
            subscriptions : "xxx"
            resourcegroups: "xxx"
            providers: "xxx"
            {service}: "xxxx"
            {name}: "xxxxx"

        """
        target: list = resource_id.split("/")[1:]
        k: list = []
        v: list = []
        for i, t in enumerate(target):
            k.append(t) if i/2 == 0 else v.append(t)

        return dict(zip(k, v))
