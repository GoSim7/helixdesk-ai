from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.runtime import ChatwootMessagePayload, RouteMessageResponse
from app.services.chatwoot_service import ChatwootWebhookError, chatwoot_service
from app.services.health_service import health_service
from app.services.routing_service import routing_service

router = APIRouter()


@router.post("/chatwoot/webhook", response_model=RouteMessageResponse)
async def chatwoot_webhook(request: Request) -> RouteMessageResponse:
    raw_body = await request.body()
    try:
        chatwoot_service.verify_webhook(
            raw_body=raw_body,
            timestamp=request.headers.get("X-Chatwoot-Timestamp"),
            signature=request.headers.get("X-Chatwoot-Signature"),
        )
    except ChatwootWebhookError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    payload = chatwoot_service.parse_webhook(raw_body)
    if payload is None:
        return RouteMessageResponse(action="ignore", reason="unsupported or non-user webhook event")
    return routing_service.route_chatwoot_message(payload, deliver_reply=True)


@router.post("/route-message", response_model=RouteMessageResponse)
async def route_message(payload: ChatwootMessagePayload) -> RouteMessageResponse:
    return routing_service.route_chatwoot_message(payload)


@router.get("/health")
async def get_runtime_health():
    return health_service.get_health()
