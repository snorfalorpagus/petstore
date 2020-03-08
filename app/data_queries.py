from typing import List, Optional, Dict
import copy

from .data_types import Pet, JsonDict

DATABASE: Dict[int, JsonDict] = {}


def list_pets(limit: int) -> Optional[List[Pet]]:
    pets: List[Pet] = []
    for n, (pet_data) in enumerate(DATABASE.values()):
        if n == limit:
            break
        pet = Pet(**pet_data)
        pets.append(pet)
    return pets


def create_pet(pet: Pet) -> Optional[int]:
    DATABASE[pet.id] = pet.to_dict()
    return pet.id


def get_pet(pet_id: int) -> Optional[Pet]:
    try:
        pet_data = copy.copy(DATABASE[pet_id])
    except KeyError:
        return None
    pet = Pet(**pet_data)
    return pet
