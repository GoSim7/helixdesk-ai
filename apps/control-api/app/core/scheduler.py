from apscheduler.schedulers.background import BackgroundScheduler

from app.services.settings_service import settings_service


class SchedulerService:
    def __init__(self) -> None:
        self._scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self._scheduler.add_job(
            settings_service.refresh_runtime_flags,
            "interval",
            minutes=1,
            id="refresh-runtime-flags",
            replace_existing=True,
        )
        self._scheduler.start()
        self._started = True

    def shutdown(self) -> None:
        if not self._started:
            return
        self._scheduler.shutdown(wait=False)
        self._started = False


scheduler_service = SchedulerService()
