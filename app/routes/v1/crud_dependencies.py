from misc import async_session

from app.routes.v1._test_template.crud import TestRepository
from app.routes.v1._test_template.dependencies import TestDependenciesMarker
from app.routes.v1.users.crud import UserRepository
from app.routes.v1.users.dependencies import UserDependencyMarker

# Прокидывание сессий в CRUD-ы

crud_dependencies: dict = {
    TestDependenciesMarker: lambda: TestRepository(
        db_session=async_session
    ),
    UserDependencyMarker: lambda: UserRepository(
        db_session=async_session
    ),
}
