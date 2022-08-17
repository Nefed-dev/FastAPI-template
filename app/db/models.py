from uuid import uuid4


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


from misc import Base


class TestModel(Base):
    __tablename__ = '0test'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class UserModel(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, unique=True, index=True)
    password = Column(String)
