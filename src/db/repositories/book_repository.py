from sqlalchemy.orm import Session


class BookRepository:
    def __init__(self, db_session: Session):
        self.__db = db_session