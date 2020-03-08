from http import HTTPStatus
from connexion import problem
from connexion.lifecycle import ConnexionResponse

from .data_types import ListPetsResponse, Pet, ShowPetResponse, JsonDict
from . import data_queries as dq


async def listPets(limit: int = 100) -> ConnexionResponse:
    pets = dq.list_pets(limit)
    if pets is None:
        return problem(HTTPStatus.INTERNAL_SERVER_ERROR, "Error", "Failed to list pets")
    response = ListPetsResponse(pets=pets)
    return ConnexionResponse(status_code=HTTPStatus.OK, body=response.to_dict())


async def createPet(body: JsonDict) -> ConnexionResponse:
    pet = Pet.from_dict(body, validate=False)  # validation already performed
    result = dq.create_pet(pet)
    if result is None:
        return problem(HTTPStatus.INTERNAL_SERVER_ERROR, "Error", "Failed to create pet")
    return ConnexionResponse(status_code=HTTPStatus.CREATED)


async def showPetById(petId: int) -> ConnexionResponse:
    pet = dq.get_pet(petId)
    if pet is None:
        return problem(HTTPStatus.NOT_FOUND, "Not Found", f"Pet not found: {petId}")
    response = ShowPetResponse(pet=pet)
    return ConnexionResponse(status_code=HTTPStatus.OK, body=response.to_dict())
