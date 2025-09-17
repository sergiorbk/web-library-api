from dependency_injector import containers, providers
from sqlalchemy.orm import Session

import src.db.session
from src.db.repositories.book_repository import BookRepository
from src.db.repositories.user_repository import UserRepository
from src.db.repositories.client_repository import ClientRepository
from src.db.repositories.book_checkout_repository import BookCheckoutRepository
from src.services.auth_serivce import AuthService
from src.services.book_service import BookService
from src.services.user_service import UserService
from src.services.client_service import ClientService
from src.services.book_checkout_service import BookCheckoutService


class Container(containers.DeclarativeContainer):
    # db sessions
    db_session: Session = providers.Factory(src.db.session.SessionLocal)

    # repositories
    user_repository: UserRepository = providers.Factory(UserRepository, db_session=db_session)
    book_repository: BookRepository = providers.Factory(BookRepository, db_session=db_session)
    client_repository: ClientRepository = providers.Factory(ClientRepository, db_session=db_session)
    book_checkout_repository: BookCheckoutRepository = providers.Factory(BookCheckoutRepository, db_session=db_session)

    # services
    auth_service: AuthService = providers.Factory(AuthService, user_repository=user_repository)
    user_service: UserService = providers.Factory(UserService, user_repository=user_repository)
    book_service: BookService = providers.Factory(BookService, book_repository=book_repository)
    client_service: ClientService = providers.Factory(ClientService, client_repository=client_repository)
    book_checkout_service: BookCheckoutService = providers.Factory(
        BookCheckoutService,
        checkout_repository=book_checkout_repository,
        book_repository=book_repository,
        client_repository=client_repository
    )
