# Hướng dẫn triển khai Legal Law Assistant

## 1. Mục đích

Tài liệu hướng dẫn chuẩn bị môi trường và chạy các thành phần của hệ thống Legal Law Assistant.

Các lệnh thực tế phải được kiểm tra lại với cấu hình và code hiện có của dự án trước khi sử dụng làm quy trình triển khai chính thức.

## 2. Yêu cầu môi trường

Các công cụ dự kiến:
- Git.
- Python tương thích với Backend.
- Node.js và npm nếu Frontend sử dụng React hoặc Next.js.
- Dịch vụ Qdrant nếu hệ thống dùng Qdrant làm cơ sở dữ liệu vector.
- API key của nhà cung cấp mô hình nếu ứng dụng cần dịch vụ mô hình bên ngoài.
- Docker và Docker Compose nếu nhóm triển khai theo hướng container.

Phiên bản cụ thể cần được thống nhất và ghi lại theo môi trường thực tế.

## 3. Lấy mã nguồn

Sao chép repository từ GitHub bằng URL thực tế của nhóm:

```bash
git clone <REPOSITORY_URL>
cd legal-law-assistant
```

Thay `<REPOSITORY_URL>` bằng URL repository thực tế.

## 4. Cấu hình biến môi trường

1. Tạo tệp `.env` tại vị trí được ứng dụng quy định.
2. Tham khảo tên biến trong `.env.example`.
3. Điền giá trị thật ở môi trường chạy cục bộ.
4. Không commit `.env` hoặc thông tin bí mật lên GitHub.

Các biến môi trường phải khớp với code của ứng dụng. Không được coi danh sách biến ví dụ là cấu hình hoàn chỉnh nếu code chưa sử dụng chúng.

## 5. Chuẩn bị Backend

1. Kiểm tra `backend/requirements.txt`.
2. Tạo môi trường Python ảo.
3. Cài các thư viện đã được nhóm khai báo.
4. Cấu hình biến môi trường và các dịch vụ phụ thuộc.
5. Khởi chạy Backend bằng lệnh phù hợp với ứng dụng thực tế.

Ví dụ tạo môi trường Python trên Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Sau đó cài dependencies theo hướng dẫn của Backend. Lệnh khởi chạy ứng dụng chỉ được bổ sung sau khi xác định module và tên biến ứng dụng FastAPI thực tế.

## 6. Chuẩn bị Frontend

Nếu Frontend sử dụng Node.js:
1. Mở thư mục `frontend/`.
2. Kiểm tra `package.json`.
3. Cài dependencies theo package manager mà dự án sử dụng.
4. Cấu hình địa chỉ Backend.
5. Chạy lệnh phát triển hoặc build theo script đã khai báo.

Không giả định rằng mọi dự án đều sử dụng cùng một lệnh hoặc cùng một framework.

## 7. Chuẩn bị RAG và Agent

- Kiểm tra quy trình chuẩn bị dữ liệu.
- Xác nhận đường dẫn tài liệu và cấu hình embedding.
- Khởi động hoặc kết nối kho vector nếu cần.
- Kiểm tra luồng truy xuất và xử lý câu hỏi.
- Xác nhận Agent gọi đúng các thành phần theo kiến trúc.

## 8. Kiểm tra sau triển khai

- Xác nhận Backend khởi động thành công.
- Xác nhận Frontend truy cập được Backend.
- Kiểm tra truy xuất tài liệu với một số câu hỏi mẫu.
- Kiểm tra thông tin trích dẫn.
- Kiểm tra xử lý lỗi khi đầu vào không hợp lệ hoặc không tìm được nguồn phù hợp.
- Lưu lại log và kết quả kiểm thử.

## 9. Khắc phục sự cố

### Không kết nối được Backend
Kiểm tra địa chỉ API, cổng, cấu hình mạng và log của Backend.

### Không truy xuất được tài liệu
Kiểm tra dữ liệu đầu vào, embedding, cấu hình kho vector và tên collection.

### Thiếu API key
Kiểm tra biến môi trường tại môi trường chạy. Không dán khóa thật vào Issue, Pull Request hoặc log công khai.

### Ứng dụng không khởi động
Kiểm tra phiên bản runtime, dependencies, cấu hình và thông báo lỗi đầy đủ.

## 10. Trạng thái tài liệu

Tài liệu này là hướng dẫn khung. Trước khi công bố là hướng dẫn triển khai chính thức, nhóm cần kiểm chứng từng lệnh và cập nhật theo môi trường chạy thực tế.
