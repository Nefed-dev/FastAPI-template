from fastapi import APIRouter

from app.routes.v1._test_template.handlers import test_router
from app.routes.v1.docs.handlers import docs_router
from app.routes.v1.security.handlers import security_router
from app.routes.v1.users.handlers import users_router

router_v1 = APIRouter()

router_v1.include_router(docs_router, tags=['Docs'])
router_v1.include_router(test_router, tags=['_. Test router'])
router_v1.include_router(security_router, tags=['0. Security'])
router_v1.include_router(users_router, tags=['1. User'])

