from sqlalchemy.orm import DeclarativeBase, declared_attr


class Model(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()
