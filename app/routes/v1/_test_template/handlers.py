from fastapi import APIRouter
from fastapi import Depends

from app.db.models import UserModel
from app.routes.v1.security.auth import get_current_user

test_router = APIRouter()


@test_router.get(
    "/test"
)
async def test_get():
    return "Test get"


@test_router.post(
    "/test"
)
async def test_create():
    return "Test post"


@test_router.patch(
    "/test"
)
async def test_patch():
    return "Test patch"


@test_router.delete(
    "/test"
)
async def test_delete():
    return "Test delete"


@test_router.get("/with_auth")
async def get_with_auth(
    current_user: UserModel = Depends(get_current_user),
):
    return current_user
