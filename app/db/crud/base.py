from abc import ABC
from contextlib import asynccontextmanager
from typing import AsyncContextManager
from typing import ClassVar

from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from sqlalchemy.orm import sessionmaker

Model = TypeVar("Model")
TransactionContext = AsyncContextManager[AsyncSessionTransaction]


class BaseCRUD(ABC):

    def __init__(
        self,
        db_session: Union[sessionmaker, AsyncSession],
        model: ClassVar[Type[Model]]
    ):
        self.model = model

        if isinstance(db_session, sessionmaker):
            self.session: AsyncSession = cast(AsyncSession, db_session())
        else:
            self.session = db_session

    @asynccontextmanager
    async def transaction(self) -> TransactionContext:
        async with self.session as transaction:
            yield transaction
