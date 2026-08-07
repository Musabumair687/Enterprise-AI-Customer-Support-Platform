"""Conversation-history REST endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import ConversationRead
from app.schemas.response import APIResponse
from app.services import conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("", response_model=APIResponse[list[ConversationRead]])
def list_conversations(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[ConversationRead]]:
    conversations = conversation_service.list_conversations(db, skip, limit)
    return APIResponse(success=True, message="Conversations retrieved successfully.", data=[ConversationRead.model_validate(conversation) for conversation in conversations])
