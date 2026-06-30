# Phân tích Failure Clusters (Phase A)

## Hiện trạng
Theo dự đoán đối với các bộ câu hỏi RAG:
- **Dominant failure distribution**: Thường là `multi_hop` hoặc `adversarial`. Các câu hỏi này yêu cầu LLM phải tổng hợp từ nhiều nguồn tài liệu khác nhau hoặc phải tránh các bẫy về phiên bản chính sách cũ/mới.
- **Dominant failure metric**: Thường là `context_recall` (thiếu context) hoặc `faithfulness` (bịa ra câu trả lời dựa trên kiến thức sẵn có do thiếu context).

## Phân tích Bottom-10
Phần lớn các câu hỏi rơi vào top 10 tệ nhất có thể có chung đặc điểm:
- **Nguyên nhân cốt lõi**: Khâu chunking cắt đứt ngữ cảnh hoặc Vector Search không truy xuất đủ các chunk cần thiết (context_recall thấp).
- **Hệ quả**: Do không đủ context, LLM tự động hallucinate dẫn tới faithfulness thấp.

## Đề xuất cải thiện
1. **Cải tiến chiến lược Chunking**: Tăng `HIERARCHICAL_PARENT_SIZE` để bao trọn ngữ cảnh, hoặc sử dụng semantic chunking thông minh hơn.
2. **Nâng cấp Search**: Sử dụng Hybrid Search (kết hợp Sparse/BM25 và Dense Search) một cách hiệu quả hơn.
3. **Prompt Engineering**: Điều chỉnh system prompt để ép LLM trả lời "Tôi không biết" thay vì tự suy diễn khi không tìm thấy đủ dữ liệu trong chunk, nhằm tăng độ Faithfulness (giảm Hallucination).
