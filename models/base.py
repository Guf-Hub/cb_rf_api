from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel
from sqlalchemy import (
    Date,
)


class Model(BaseModel):
    @classmethod
    def fields(cls):
        """
        Return a list of all the fields in the schema.
        :return: A list of field names.
        :rtype: list
        """
        return list(cls.model_json_schema(by_alias=False).get("properties").keys())

    def to_dict(self) -> Dict[Any, Any]:
        """
        Convert the object to a dictionary representation.
        :return: A dictionary representation of the object, or None if the object is empty.
        :rtype: dict or None
        """
        return self.model_dump() if self else None

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    class Config:
        from_attributes = True  # Позволяет использовать ORM, если требуется
