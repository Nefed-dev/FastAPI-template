from fastapi import APIRouter
from fastapi import Depends
from starlette.responses import JSONResponse

from app.routes.v1.security.context import get_password_hash
from app.routes.v1.users.crud import UserRepository
from app.routes.v1.users.dependencies import UserDependencyMarker
from app.routes.v1.users.schemas import RegisterUserModel
from app.routes.v1.users.schemas import UserCreated

users_router = APIRouter()


@users_router.post(
    "/users",
    response_model=UserCreated
)
async def create(
    data: RegisterUserModel,
    user_db: UserRepository = Depends(UserDependencyMarker)
):
    password_hashed = get_password_hash(data.password)
    user = await user_db.create(
        login=data.login, password=password_hashed
    )
    answer = {"detail": "User created", "uuid": str(user.uuid)}

    return JSONResponse(status_code=201, content=answer)

@users_router.get("/users")
async def get():
    pass


@users_router.patch("/users")
async def patch():
    pass


@users_router.delete("/users")
async def delete():
    pass
