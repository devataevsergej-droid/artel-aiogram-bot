from .start import router as start_router
from .menu import router as menu_router
from .profile import router as profile_router   # <--- ДОБАВИТЬ

def register_all_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(profile_router)   # <--- ДОБАВИТЬ
