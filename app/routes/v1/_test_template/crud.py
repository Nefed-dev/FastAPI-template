from app.db.crud.base import BaseCRUD

from app.db.models import TestModel

from sqlalchemy.orm import sessionmaker


class TestRepository:
    def __init__(self, db_session: sessionmaker):
        self.session = db_session

        self.model = TestModel
        self.base = BaseCRUD(db_session, model=self.model)

    async def get(self):
        async with self.base.transaction():
            return None

    async def post(self):
        async with self.base.transaction():
            return None

    async def patch(self):
        async with self.base.transaction():
            return None

    async def delete(self):
        async with self.base.transaction():
            return None
