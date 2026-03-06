"""
Layer 1: Query Expansion
=========================
Mở rộng từ khóa bằng Synonym Dictionary (~70 entries) và pattern matching.
Giúp tìm đúng "Sữa hạt Macca" dù user gõ "sữa hạt" hoặc "macca".
"""

# Synonym Dictionary - Bảng từ đồng nghĩa (~70 entries)
SYNONYM_DICT: dict[str, list[str]] = {
    # === Thực phẩm ===
    "sữa hạt": ["sữa hạt macca", "sữa hạt điều", "sữa hạt óc chó", "plant milk", "nut milk"],
    "sữa": ["sữa tươi", "sữa bột", "sữa chua", "sữa đặc", "dairy"],
    "trà": ["trà xanh", "trà đen", "trà oolong", "trà hoa", "tea", "matcha"],
    "cà phê": ["cafe", "coffee", "espresso", "latte", "cappuccino", "đen", "nâu"],
    "nước ép": ["nước trái cây", "juice", "sinh tố", "smoothie"],
    "bánh": ["bánh ngọt", "bánh mì", "cake", "bread", "pastry"],
    "trái cây": ["hoa quả", "fruit", "táo", "cam", "nho", "chuối"],

    # === Công nghệ ===
    "ai": ["artificial intelligence", "trí tuệ nhân tạo", "machine learning", "ml", "deep learning"],
    "llm": ["large language model", "mô hình ngôn ngữ", "gpt", "qwen", "llama", "chatgpt"],
    "rag": ["retrieval augmented generation", "tìm kiếm tăng cường", "vector search"],
    "vector db": ["qdrant", "chromadb", "pinecone", "vector database", "milvus", "weaviate"],
    "embedding": ["nhúng", "vector hóa", "text embedding", "word2vec"],
    "gpu": ["card đồ họa", "graphics card", "vram", "sycl", "cuda", "rocm"],
    "cpu": ["vi xử lý", "processor", "chip"],
    "ram": ["bộ nhớ trong", "memory", "ddr4", "ddr5"],

    # === Hành động ===
    "tìm": ["tìm kiếm", "tra cứu", "search", "lookup", "explore"],
    "mua": ["đặt hàng", "order", "purchase", "thêm vào giỏ", "buy"],
    "bán": ["sell", "kinh doanh", "cung cấp"],
    "hủy": ["cancel", "xóa", "delete", "remove"],
    "sửa": ["edit", "update", "cập nhật", "modify"],
    "tạo": ["create", "làm mới", "new", "generate"],
    "giá": ["giá tiền", "price", "chi phí", "cost", "bao nhiêu tiền", "giá bán"],
    "hướng dẫn": ["cách làm", "tutorial", "guide", "how to"],
    "lỗi": ["bug", "error", "fail", "không chạy", "hỏng"],

    # === Tính từ phổ biến ===
    "tốt": ["chất lượng", "premium", "best", "xịn", "ok"],
    "rẻ": ["giá rẻ", "tiết kiệm", "affordable", "cheap", "mềm"],
    "mới": ["mới nhất", "latest", "new", "vừa ra", "brand new"],
    "cũ": ["đã qua sử dụng", "second hand", "used", "old"],
    "ngon": ["hấp dẫn", "tuyệt vời", "delicious", "tasty"],
    "đẹp": ["thẩm mỹ", "beautiful", "gorgeous", "xinh"],

    # === Tiện ích ===
    "tóm tắt": ["summary", "rút gọn", "ngắn gọn", "tổng hợp", "TL;DR"],
    "dịch": ["translate", "phiên dịch", "ngôn ngữ"],
    "chuyển đổi": ["convert", "đổi", "biến đổi", "transform"],
    "so sánh": ["compare", "đối chiếu", "so tài", "versus", "vs"],
    "đăng nhập": ["login", "sign in", "vào", "truy cập"],
    "đăng xuất": ["logout", "sign out", "thoát"],
    "tài khoản": ["account", "profile", "nick", "user"],
    "mật khẩu": ["password", "mật mã", "passcode"],
}


def expand_query(query: str) -> tuple[str, list[str]]:
    """
    Mở rộng câu truy vấn bằng synonym dictionary.

    Args:
        query: Câu truy vấn gốc.

    Returns:
        (expanded_query, expanded_keywords)
        - expanded_query: Query đã thêm từ đồng nghĩa.
        - expanded_keywords: Danh sách từ khóa mở rộng đã thêm.
    """
    query_lower = query.lower()
    all_keywords = []

    for key, synonyms in SYNONYM_DICT.items():
        if key in query_lower:
            # Thêm 2 synonyms đầu tiên (tránh quá dài)
            relevant = synonyms[:2]
            all_keywords.extend(relevant)

    if not all_keywords:
        return query, []

    # Kết hợp query gốc + synonyms vào chuỗi mới
    expanded = f"{query} {' '.join(all_keywords)}"
    return expanded, all_keywords
