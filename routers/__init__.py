__all__ = ('router',)

from aiogram import Router

from .admin_handlers import router as admin_router
from .book_hanlers import router as book_router
from .user_handlers import router as user_router
from routers.sender.sender import router as sender_router

router = Router(name=__name__)

router.include_routers(
    book_router,
    admin_router,
    sender_router
)

router.include_router(user_router)
