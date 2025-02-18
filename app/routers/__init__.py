from .auth import router as auth_router
from .devices import router as devices_router
from .orders import router as orders_router

__all__ = ["auth_router", "devices_router", "orders_router"]
