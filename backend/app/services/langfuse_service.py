"""
LangFuse Service
================
Dịch vụ tích hợp LangFuse để giám sát, truy vết (tracing) và phân tích luồng AI.
Hỗ trợ tạo Callback Handler cho LangChain/LangGraph.
"""
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LangfuseService:
    def __init__(self):
        self.enabled = False
        self._init_langfuse()

    def _init_langfuse(self):
        """Khởi tạo Langfuse Callback Handler."""
        if not settings.LANGFUSE_PUBLIC_KEY:
            logger.info("[LangFuse] Not configured (missing PUBLIC_KEY). Observability disabled.")
            return

        try:
            from langfuse.callback import CallbackHandler
            # Chỉ khởi tạo handler để nhúng vào Graph/Chain config
            self.handler = CallbackHandler(
                secret_key=settings.LANGFUSE_SECRET_KEY,
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                host=settings.LANGFUSE_HOST,
            )
            self.enabled = True
            logger.info("[LangFuse] CallbackHandler initialized successfully.")
        except ImportError:
            logger.warning("[LangFuse] SDK not installed (`pip install langfuse`). Observability disabled.")
        except Exception as e:
            logger.error(f"[LangFuse] Initialization failed: {e}")

    def get_callback(self):
        """Lấy callback handler để chèn vào `config={"callbacks": [...]}`."""
        return [self.handler] if self.enabled else []

    def get_status(self) -> dict:
        """Kiểm tra trạng thái LangFuse."""
        return {
            "enabled": self.enabled,
            "host": settings.LANGFUSE_HOST if self.enabled else None,
        }
