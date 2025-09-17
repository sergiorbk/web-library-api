import uuid
from typing import List, Optional
from datetime import date

from src.db.repositories.client_repository import ClientRepository
from src.exceptions.client_exceptions import ClientNotFoundException, ClientAlreadyExistsException, InvalidClientDataException
from src.mappers.client_mappers import map_client_orm_to_schema, map_create_request_to_orm
from src.schemas.client import ClientSchema, CreateClientRequest, UpdateClientRequest, ClientSearchRequest


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.__client_repository = client_repository

    def create_client(self, request: CreateClientRequest) -> ClientSchema:
        """Create a new client"""
        # Check if client with same email already exists
        if self.__client_repository.exists_by_email(request.email):
            raise ClientAlreadyExistsException(f"Client with email {request.email} already exists")

        # Validate birthdate (not in future)
        if request.birthdate > date.today():
            raise InvalidClientDataException("Birthdate cannot be in the future")

        # Check if user already has a client profile
        existing_client = self.__client_repository.get_by_user_id(request.user_id)
        if existing_client:
            raise ClientAlreadyExistsException(f"Client profile for user {request.user_id} already exists")

        client_orm = map_create_request_to_orm(request)
        created_client = self.__client_repository.create(client_orm)
        return map_client_orm_to_schema(created_client)

    def get_all_clients(self) -> List[ClientSchema]:
        """Get all clients"""
        clients = self.__client_repository.get_all()
        return [map_client_orm_to_schema(client) for client in clients]

    def get_client_by_id(self, client_id: uuid.UUID) -> Optional[ClientSchema]:
        """Get client by ID"""
        client = self.__client_repository.get_by_id(client_id)
        if not client:
            return None
        return map_client_orm_to_schema(client)

    def get_client_by_user_id(self, user_id: uuid.UUID) -> Optional[ClientSchema]:
        """Get client by user ID"""
        client = self.__client_repository.get_by_user_id(user_id)
        if not client:
            return None
        return map_client_orm_to_schema(client)

    def get_client_by_email(self, email: str) -> Optional[ClientSchema]:
        """Get client by email"""
        client = self.__client_repository.get_by_email(email)
        if not client:
            return None
        return map_client_orm_to_schema(client)

    def update_client(self, client_id: uuid.UUID, request: UpdateClientRequest) -> Optional[ClientSchema]:
        """Update client"""
        if not self.__client_repository.get_by_id(client_id):
            raise ClientNotFoundException(f"Client with ID {client_id} not found")

        # Check if email is being changed and if it already exists
        if request.email:
            existing_client = self.__client_repository.get_by_email(request.email)
            if existing_client and existing_client.client_id != client_id:
                raise ClientAlreadyExistsException(f"Client with email {request.email} already exists")

        # Validate birthdate if being updated
        if request.birthdate and request.birthdate > date.today():
            raise InvalidClientDataException("Birthdate cannot be in the future")

        update_data = {}
        if request.email is not None:
            update_data['email'] = request.email
        if request.name is not None:
            update_data['name'] = request.name
        if request.surname is not None:
            update_data['surname'] = request.surname
        if request.patronymic is not None:
            update_data['patronymic'] = request.patronymic
        if request.birthdate is not None:
            update_data['birthdate'] = request.birthdate

        updated_client = self.__client_repository.update(client_id, **update_data)
        if not updated_client:
            return None
        return map_client_orm_to_schema(updated_client)

    def delete_client(self, client_id: uuid.UUID) -> bool:
        """Delete client"""
        if not self.__client_repository.get_by_id(client_id):
            raise ClientNotFoundException(f"Client with ID {client_id} not found")

        return self.__client_repository.delete_by_id(client_id)

    def search_clients(self, request: ClientSearchRequest) -> List[ClientSchema]:
        """Search clients based on criteria"""
        clients = []

        if request.name:
            clients = self.__client_repository.search_by_name(request.name)
        elif request.start_birthdate and request.end_birthdate:
            clients = self.__client_repository.get_by_birthdate_range(
                request.start_birthdate,
                request.end_birthdate
            )
        else:
            clients = self.__client_repository.get_all()

        return [map_client_orm_to_schema(client) for client in clients]