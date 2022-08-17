from typing import Any
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from starlette import status

from app.routes.v1.security.context import verify_password
from app.routes.v1.users.crud import UserRepository
from app.routes.v1.users.dependencies import UserDependencyMarker
from config import settings_app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Wrong data.",
    headers={"WWW-Authenticate": "Bearer"},
)


async def authenticate(
    *,
    login: str,
    password: str,
    db: UserRepository = Depends(UserDependencyMarker),
) -> Optional[Any]:
    # Получаем юзера по любому доступному логину
    # (телефон, почта и т.п. в зависимости от настроек модели
    user = await db.get_by_login(login)
    if not user:
        raise credentials_exception

    # Проверяем пароль. ФНК расшифровывает хеш хуй знает как и сравнивает
    if not verify_password(password, user.password):
        raise credentials_exception

    # Возвращает юзера
    return user


def create_access_token(*, sub: str) -> str:
    # sub - в нашем случае это зашиваемый userUUID,
    # который в get_current_user->decode_jwt достается для доступа к юзеру из БД
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings_app.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    # !ALARM! Здесь используется библиотека python-jose
    # Библиотека "jose" без python сломана!
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings_app.JWT_SECRET, algorithm=settings_app.JWT_ALGORITHM)


def remove_token_type_in_token(token: str):
    # Убираем из ЖВТ токена лишний момент в виде "Кода" Bearer
    if token.lower().startswith('bearer'):
        token = token.replace('Bearer ', '')
    return token


def decode_jwt(token: str = Depends(oauth2_scheme)):
    # Функция, которая достает данные, зашитые в JWT-токене.
    # На наших проектах используется ТОЛЬКО юзер ЮЮИД
    reformat_token = remove_token_type_in_token(token)

    try:
        payload = jwt.decode(
            reformat_token,
            settings_app.JWT_SECRET,
            algorithms=[settings_app.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user_uuid


async def get_current_user(
    db: UserRepository = Depends(UserDependencyMarker),
    token: str = Depends(oauth2_scheme)
):
    # Получение текущего юзера.
    # В JWT токене зашит ЮЮИД юзера, который зашивается при ручке /login
    # (первая строчка словаря "access_token": create_access_token(sub=user.uuid))
    jwt_user_uuid = decode_jwt(token=token)

    # Дальше всё просто. Ищем по расшифрованному ЮЮИД юзера в БД
    user_db = await db.get_by_uuid(jwt_user_uuid)

    if user_db is None:
        raise credentials_exception

    return user_db

# SOME MOMENTS:
# Авторизацию к ручкам можно прикрутить 3 способами:
# 1. В параметрах непосредственно ручки
#    current_user: UserModel = Depends(get_current_user)
# 2. Можно задать авторизацию при объявлении Роута в handlers
# some_router = APIRouter(
#     dependencies=[Depends(get_current_user)],
# )
# 3. При биндинге. В рамках этого репозитория в файле route_bindings можно прописывать следующее:
# router_vX.include_router(some_router, tags=['1. Some'], dependencies=[Depends(get_current_user)],)
# 4. Насколько я понял, можно также на весь МАМА - роутер закинуть.
# router_vX = APIRouter(dependencies=[Depends(get_current_user)],)


