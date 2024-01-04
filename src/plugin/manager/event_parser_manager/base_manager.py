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
