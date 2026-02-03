from .start import router as start_router
from .profile import router as profile_router
from .payment import router as payment_router
from .request import router as request_router
from .admin import router as admin_router

routers = [start_router, profile_router, payment_router, request_router, admin_router]
