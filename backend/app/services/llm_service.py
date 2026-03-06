"""
LLM Service
============
Multi-backend LLM inference service.
Hỗ trợ: IPEX-LLM (SYCL), Ollama, và llama.cpp.
Chạy trên Intel UHD Graphics 730 (2GB VRAM shared).

Strategy:
  - Reranking logic → CPU (đã có trong reranker.py)
  - LLM inference → GPU (SYCL backend)
  - Quantization: 4-bit (GGUF/GPTQ/AWQ) bắt buộc cho 2GB VRAM
"""
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMService:
    """
    Multi-backend LLM Service.
    Tự động chọn backend khả dụng theo thứ tự ưu tiên:
    1. IPEX-LLM (SYCL) — hiệu năng cao nhất trên Intel GPU
    2. Ollama — dễ cài đặt, hỗ trợ nhiều model
    3. llama.cpp — fallback phổ biến
    """

    def __init__(self):
        self.backend = settings.LLM_BACKEND
        self.model_name = settings.LLM_MODEL
        self._client = None
        self._init_backend()

    def _init_backend(self):
        """Khởi tạo backend dựa trên cấu hình."""
        if self.backend == "ipex-llm":
            self._init_ipex()
        elif self.backend == "ollama":
            self._init_ollama()
        elif self.backend == "llamacpp":
            self._init_llamacpp()
        else:
            logger.warning(f"Unknown LLM backend: {self.backend}. Using placeholder.")

    def _init_ipex(self):
        """
        Khởi tạo IPEX-LLM với SYCL backend.
        Yêu cầu: intel-extension-for-pytorch, oneAPI toolkit.
        """
        try:
            from ipex_llm.transformers import AutoModelForCausalLM
            from transformers import AutoTokenizer

            logger.info(f"[IPEX-LLM] Loading model: {self.model_name} (SYCL/XPU)")
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, trust_remote_code=True
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                load_in_4bit=True,  # 4-bit quantization cho 2GB VRAM
                trust_remote_code=True,
                optimize_model=True,
            )
            # Chuyển model sang Intel GPU (XPU)
            self._model = self._model.to("xpu")
            self._client = "ipex"
            logger.info("[IPEX-LLM] Model loaded successfully on XPU.")

        except ImportError:
            logger.warning("[IPEX-LLM] Not installed. Falling back to Ollama.")
            self.backend = "ollama"
            self._init_ollama()
        except Exception as e:
            logger.error(f"[IPEX-LLM] Failed: {e}. Falling back to Ollama.")
            self.backend = "ollama"
            self._init_ollama()

    def _init_ollama(self):
        """Khởi tạo Ollama client (HTTP API)."""
        try:
            import httpx
            self._client = "ollama"
            self._ollama_url = "http://localhost:11434"
            logger.info(f"[Ollama] Using model: {self.model_name}")
        except Exception as e:
            logger.warning(f"[Ollama] Failed: {e}. Using placeholder.")
            self._client = None

    def _init_llamacpp(self):
        """Khởi tạo llama.cpp (via llama-cpp-python)."""
        try:
            from llama_cpp import Llama
            self._model = Llama(
                model_path=self.model_name,
                n_ctx=2048,
                n_gpu_layers=-1,  # Offload tất cả layers lên GPU
            )
            self._client = "llamacpp"
            logger.info(f"[llama.cpp] Model loaded: {self.model_name}")
        except ImportError:
            logger.warning("[llama.cpp] Not installed. Using placeholder.")
            self._client = None

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """
        Tạo text từ LLM.

        Args:
            prompt: Câu hỏi/yêu cầu từ người dùng.
            system_prompt: System prompt (Memory + Instructions).
            max_tokens: Số token tối đa cho response.
            temperature: Độ sáng tạo (0.0 = chính xác, 1.0 = sáng tạo).

        Returns:
            Generated text response.
        """
        if self._client == "ipex":
            return self._generate_ipex(prompt, system_prompt, max_tokens, temperature)
        elif self._client == "ollama":
            return await self._generate_ollama(prompt, system_prompt, max_tokens, temperature)
        elif self._client == "llamacpp":
            return self._generate_llamacpp(prompt, system_prompt, max_tokens, temperature)
        else:
            # Placeholder khi chưa có backend
            return (
                f"[WIKI-AI Placeholder] Tôi nhận được: \"{prompt}\". "
                f"LLM backend chưa được cấu hình. "
                f"Hãy cài đặt IPEX-LLM, Ollama hoặc llama.cpp."
            )

    def _generate_ipex(self, prompt, system_prompt, max_tokens, temperature):
        """Generate bằng IPEX-LLM trên Intel GPU (XPU)."""
        import torch

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        text = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self._tokenizer(text, return_tensors="pt").to("xpu")

        with torch.inference_mode():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
            )

        response = self._tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
        return response.strip()

    async def _generate_ollama(self, prompt, system_prompt, max_tokens, temperature):
        """Generate bằng Ollama HTTP API."""
        import httpx

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._ollama_url}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception as e:
            logger.error(f"[Ollama] Generate failed: {e}")
            return f"Lỗi kết nối Ollama: {e}"

    def _generate_llamacpp(self, prompt, system_prompt, max_tokens, temperature):
        """Generate bằng llama.cpp."""
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        output = self._model(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return output["choices"][0]["text"].strip()

    def get_status(self) -> dict:
        """Trạng thái hiện tại của LLM service."""
        return {
            "backend": self.backend,
            "model": self.model_name,
            "ready": self._client is not None,
        }
