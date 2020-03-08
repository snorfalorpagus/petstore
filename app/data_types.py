from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin

JsonDict = Dict[str, Any]


class BaseType(JsonSchemaMixin):
    pass


@dataclass
class Pet(BaseType):
    id: int
    name: str
    tag: str


@dataclass
class ListPetsResponse(BaseType):
    pets: List[Pet]


@dataclass
class ShowPetResponse(BaseType):
    pet: Pet


@dataclass
class Problem(BaseType):
    """Problem details (RFC-7807)"""

    status: int
    title: str
    detail: str
    type: str
    instance: Optional[str]
