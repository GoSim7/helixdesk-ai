from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ChatwootMessagePayload(BaseModel):
    conversation_id: int
    content: str
    sender_type: str = "user"
    contact_name: str | None = None
    event: str = "message_created"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatwootWebhookConversation(BaseModel):
    id: int | None = None


class ChatwootWebhookSender(BaseModel):
    name: str | None = None
    type: str | None = None


class ChatwootWebhookPayload(BaseModel):
    event: str
    content: str | None = None
    message_type: str | int | None = None
    private: bool | None = None
    conversation: ChatwootWebhookConversation | None = None
    conversation_id: int | None = None
    sender: ChatwootWebhookSender | None = None
    sender_type: str | None = None
    content_attributes: dict[str, Any] = Field(default_factory=dict)
    additional_attributes: dict[str, Any] = Field(default_factory=dict)


class AstrBotReplyRequest(BaseModel):
    conversation_id: str
    user_message: str
    contact_name: str | None = None
    preset: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class RuntimeHealthResponse(BaseModel):
    status: str
    services: dict[str, str]
    checked_at: datetime


class RouteMessageResponse(BaseModel):
    action: str
    reason: str
    reply: str | None = None
