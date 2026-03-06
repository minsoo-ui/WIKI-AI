# Phase 05: Hardware Optimization (IPEX-LLM / SYCL)

## Objective
Tích hợp IPEX-LLM với SYCL backend để tận dụng Intel iGPU UHD 730 cho LLM inference.
CPU xử lý Reranking logic, GPU xử lý LLM inference và embedding.

## Tasks
- [x] Tạo LLM Service (multi-backend: IPEX-LLM, Ollama, llama.cpp).
- [x] Tạo Embedding Service (nomic-embed-text-v1.5).
- [x] Kết nối Graph API endpoint `/chat/send` với Graph builder.
- [x] Inject embed_fn thực tế vào RAG Pipeline.

## Test Criteria
- [ ] LLM inference hoạt động qua ít nhất 1 backend.
- [ ] Embedding tạo được vector 768 dimensions.
- [ ] API `/chat/send` trả về response từ Graph.
