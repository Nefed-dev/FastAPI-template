from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.db.crud.base import BaseCRUD
from app.db.models import UserModel


class UserRepository:
    def __init__(self, db_session: sessionmaker | Session):
        self.db_session = db_session
        self.model = UserModel
        self.base = BaseCRUD(db_session=db_session, model=self.model)

    async def create(self, login: str, password: str):
        async with self.base.transaction():
            data = self.model(
                login=login,
                password=password
            )
            self.base.session.add(data)
            await self.db_session.flush()
            return data

    async def get_by_login(self, login) -> UserModel:
        async with self.base.transaction():
            sql = select(self.model).where(self.model.login == login)
            result = await self.base.session.execute(sql)
            return result.scalar_one()

    async def get_by_uuid(self, uuid: UUID | str) -> UserModel:
        async with self.base.transaction():
            sql = select(self.model).where(self.model.uuid == uuid)
            result = await self.base.session.execute(sql)
            return result.scalar_one()
