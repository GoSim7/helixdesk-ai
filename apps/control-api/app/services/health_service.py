from app.core.time import utc_now
from app.schemas.runtime import RuntimeHealthResponse
from app.services.astrbot_service import astrbot_service
from app.services.chatwoot_service import chatwoot_service


class HealthService:
    def get_health(self) -> RuntimeHealthResponse:
        services = {
            "postgres": "ok",
            "redis": "not_configured",
            "chatwoot": chatwoot_service.health_status(),
            "astrbot": astrbot_service.health_status(),
        }
        return RuntimeHealthResponse(
            status="ok" if "error" not in services.values() else "degraded",
            services=services,
            checked_at=utc_now(),
        )


health_service = HealthService()
