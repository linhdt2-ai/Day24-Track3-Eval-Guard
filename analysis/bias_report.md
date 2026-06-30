# Phân tích Bias (Phase B)

## Kết quả đo lường
- **Total Judged**: 1 cặp trả lời (Demo)
- **Position Bias Rate**: 0.0
- **Verbosity Bias**: 1.0 (Câu trả lời A thắng và A dài hơn)
- **Cohen's κ (Kappa)**: 0.000 (Placeholder)

## Phân tích
- **Position Bias**: Trong bài test, LLM Judge tỏ ra khá nhất quán, chọn cùng một kết quả cho dù đổi vị trí của câu trả lời. Điều này cho thấy tính ổn định (consistency) tốt, không bị ảnh hưởng quá nhiều bởi vị trí A/B.
- **Verbosity Bias**: LLM có xu hướng chọn câu trả lời dài hơn. Cần quan sát thêm trên tập dữ liệu lớn hơn. Nếu verbosity bias liên tục cao (> 0.6), LLM Judge có thể đang đánh giá sai lệch, ưu tiên độ dài thay vì độ chính xác.

## Đề xuất cải thiện
1. **Tinh chỉnh Prompt cho Judge**: Nhấn mạnh việc ưu tiên sự "ngắn gọn, đúng trọng tâm" (conciseness) trong prompt để giảm verbosity bias.
2. **Luôn sử dụng Swap-and-average**: Mặc dù position bias thấp trong lượt test, nhưng chiến lược swap-and-average vẫn là cần thiết để đảm bảo độ tin cậy.
