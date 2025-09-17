from src.db.models.orm_client import Client
from src.schemas.client import ClientSchema, CreateClientRequest


def map_client_orm_to_schema(client: Client) -> ClientSchema:
    """Map Client ORM model to ClientSchema"""
    return ClientSchema(
        client_id=client.client_id,
        user_id=client.user_id,
        email=client.email,
        name=client.name,
        surname=client.surname,
        patronymic=client.patronymic,
        birthdate=client.birthdate
    )


def map_create_request_to_orm(request: CreateClientRequest) -> Client:
    """Map CreateClientRequest to Client ORM model"""
    return Client(
        user_id=request.user_id,
        email=request.email,
        name=request.name,
        surname=request.surname,
        patronymic=request.patronymic,
        birthdate=request.birthdate
    )