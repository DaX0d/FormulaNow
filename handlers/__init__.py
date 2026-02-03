from .next_race import next_race_router
from .schedule import schedule_router
from .last_race import last_race_router
from .standings import standings_router
from .buttons import buttons_router
from .guide import guide_router


routers = [
    next_race_router,
    schedule_router,
    last_race_router,
    standings_router,
    guide_router,
    buttons_router  # Этот роутер обязательно последний
]
