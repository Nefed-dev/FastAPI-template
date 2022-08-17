from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.routes.v1.security.auth import authenticate
from app.routes.v1.security.auth import create_access_token
from app.routes.v1.users.crud import UserRepository
from app.routes.v1.users.dependencies import UserDependencyMarker

security_router = APIRouter()


@security_router.post(
    "/login",
    # responses=AuthResponses.login,
    summary="AuthUser"
)
async def login(
    db: UserRepository = Depends(UserDependencyMarker),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # В фнк отдаем юзернейм, чтобы найти в бд,
    # Отдаем пришедший пароль (пароль приходит не хешированный)
    # Далее фнк из библиотеки passlib проверяет совпадение
    # по Хеш паролю из БД и пришедшему не хешированному паролю
    user = await authenticate(
        login=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Далее отдаем для фронта Биарер код.
    # Формируется библиотекой python-jose.
    # !ALARM! просто jose - сломанная библиотека! Необходим python-jose.
    return {
        "access_token": create_access_token(sub=user.uuid),
        "token_type": "bearer",
        "user_uuid": user.uuid,
    }
