"""
Memory Manager
==============
Bộ nhớ 3 Tầng: Hot Context, Progressive Summary, Profile
"""
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

HOT_CONTEXT_SIZE = 8
PROFILE_DIR = Path("./data/profiles")

class MemoryManager:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    def get_hot_context(self, chat_history: list[dict]) -> list[dict]:
        return chat_history[-HOT_CONTEXT_SIZE:]

    def build_progressive_summary(self, chat_history: list[dict], existing_summary: str = "") -> str:
        if len(chat_history) <= HOT_CONTEXT_SIZE:
            return existing_summary
        old_messages = chat_history[:-HOT_CONTEXT_SIZE]
        summary_parts = [existing_summary] if existing_summary else []
        for msg in old_messages[-5:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")[:100]
            if role == "user":
                summary_parts.append(f"- User: {content}")
            elif role == "assistant":
                summary_parts.append(f"- AI: {content}")
        return "\n".join(summary_parts[-10:])

    def get_user_profile(self, user_id: str) -> dict:
        if self.redis:
            try:
                data = self.redis.get(f"user_profile:{user_id}")
                return json.loads(data) if data else {}
            except Exception:
                pass
        profile_path = PROFILE_DIR / f"{user_id}.json"
        if profile_path.exists():
            with open(profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
