# Báo cáo kiểm thử hệ thống

## 1. Thông tin chung

- Tên dự án: Legal Law Assistant
- Mục đích kiểm thử: Đánh giá hoạt động của các thành phần và khả năng tích hợp giữa chúng.
- Người thực hiện: Cập nhật tên thành viên thực tế.
- Ngày kiểm thử: Cập nhật khi tiến hành kiểm thử.
- Phiên bản/commit được kiểm thử: Cập nhật mã commit hoặc nhánh tương ứng.

## 2. Phạm vi kiểm thử

Các thành phần dự kiến được kiểm thử:

1. Backend API.
2. RAG và truy xuất tài liệu.
3. Agent.
4. Citation Validator.
5. Frontend.
6. Tích hợp toàn hệ thống.
7. Quy trình CI/CD, nếu đã cấu hình.

## 3. Danh sách kiểm thử

| Mã | Thành phần | Nội dung kiểm thử | Kết quả | Bằng chứng/Ghi chú |
|---|---|---|---|---|
| TC-01 | Backend | API tiếp nhận yêu cầu hợp lệ | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-02 | Backend | Xử lý đầu vào rỗng hoặc không hợp lệ | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-03 | RAG | Truy xuất tài liệu liên quan đến câu hỏi | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-04 | RAG | Xử lý trường hợp không tìm thấy tài liệu | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-05 | Agent | Điều phối các bước xử lý theo thiết kế | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-06 | Citation Validator | Kiểm tra trích dẫn có nguồn đối chiếu | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-07 | Citation Validator | Phát hiện trích dẫn không xác minh được | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-08 | Frontend | Gửi câu hỏi và hiển thị kết quả | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-09 | Tích hợp | Frontend kết nối Backend | Chưa thực hiện | Cập nhật sau khi chạy |
| TC-10 | CI | Workflow chạy thành công trên Pull Request | Chưa thực hiện | Cập nhật sau khi cấu hình |

## 4. Quy ước kết quả

- PASS: Đã thực hiện và đáp ứng tiêu chí kiểm thử.
- FAIL: Đã thực hiện nhưng không đáp ứng tiêu chí.
- BLOCKED: Chưa thể kiểm thử do thiếu thành phần, cấu hình hoặc điều kiện cần thiết.
- NOT RUN: Chưa thực hiện kiểm thử.

Mỗi kết quả PASS hoặc FAIL cần có bằng chứng phù hợp, chẳng hạn log, ảnh chụp màn hình, kết quả test hoặc liên kết workflow.

## 5. Ghi nhận lỗi

Khi phát hiện lỗi, ghi nhận:
- Mã lỗi hoặc Issue liên quan.
- Bước tái hiện lỗi.
- Kết quả mong đợi.
- Kết quả thực tế.
- Mức độ ảnh hưởng.
- Người phụ trách xử lý.
- Trạng thái khắc phục.

## 6. Kết luận

Chỉ đưa ra kết luận về mức độ sẵn sàng của hệ thống sau khi đã thực hiện các kiểm thử cần thiết.

Không sử dụng báo cáo này để khẳng định hệ thống hoạt động đầy đủ khi các thành phần chưa được triển khai hoặc chưa có kết quả kiểm thử thực tế.
