from http import HTTPStatus
import pytest
from unittest import mock

from app.data_types import ListPetsResponse, ShowPetResponse


@pytest.fixture(autouse=True)
def example_pets():
    data = {
        "1": {"id": 1, "name": "Scooby", "tag": "doge"},
        "2": {"id": 2, "name": "Garfield", "tag": "kitteh"},
    }
    with mock.patch.dict("app.data_queries.DATABASE", data):
        yield


async def test_list_pets(test_client):
    response = await test_client.get("/pets")
    assert response.status == HTTPStatus.OK
    data = await response.json()
    pets = [pet for pet in ListPetsResponse.from_dict(data).pets]
    assert len(pets) == 2
    assert {p.name for p in pets} == {"Scooby", "Garfield"}


async def test_create_pet(test_client):
    # Create a new pet
    pet = {"id": 42, "name": "John Bon Pony", "tag": "horsey"}
    response = await test_client.post("/pets", json=pet)
    assert response.status == HTTPStatus.CREATED

    # Retrieve the pet
    response = await test_client.get("/pets/42")
    assert response.status == HTTPStatus.OK
    data = await response.json()
    pet = ShowPetResponse.from_dict(data).pet
    assert pet.id == 42
    assert pet.name == "John Bon Pony"
    assert pet.tag == "horsey"


@pytest.mark.parametrize(
    "invalid_pet", [{"id": 123, "name": -999, "tag": "doge"}, {"id": 123, "tag": "doge"}],
)
async def test_create_invalid_pet(test_client, invalid_pet):
    """Submitting an invalid Pet should return a 400 BAD REQUEST"""
    response = await test_client.post("/pets", json=invalid_pet)
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_get_missing_pet(test_client):
    response = await test_client.get("/pets/999")
    assert response.status == HTTPStatus.NOT_FOUND
