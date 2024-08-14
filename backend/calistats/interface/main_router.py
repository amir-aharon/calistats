from fastapi import APIRouter
from calistats.interface.routes.stat_routes import stat_router
from calistats.interface.routes.stat_type_routes import stat_type_router


main_router = APIRouter()

main_router.include_router(stat_router)
main_router.include_router(stat_type_router)
