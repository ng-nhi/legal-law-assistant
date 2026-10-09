
# Tests

## 1. Mục đích

Thư mục này dành cho các bài kiểm thử của Legal Law Assistant.

## 2. Phạm vi kiểm thử

- Backend API.
- Làm sạch và chia đoạn tài liệu.
- Truy xuất RAG.
- Logic Agent.
- Citation Validator.
- Tích hợp Frontend và Backend.
- Trường hợp lỗi và đầu vào không hợp lệ.

## 3. Nguyên tắc

- Mỗi bài kiểm thử cần có mục tiêu rõ ràng.
- Xác định đầu vào và kết quả mong đợi.
- Không sử dụng API key thật trong mã kiểm thử.
- Hạn chế phụ thuộc dịch vụ ngoài trong unit test.
- Ghi rõ điều kiện cần thiết khi chạy integration test.

## 4. Cách chạy

Cập nhật lệnh chạy test chính thức sau khi nhóm xác nhận framework, cấu trúc test và cấu hình môi trường.

## 5. Báo cáo

Ghi số bài kiểm thử đã chạy, kết quả thành công/thất bại và lỗi còn tồn tại trong `docs/testing-report.md`.
