
# Data — Dữ liệu pháp luật

## 1. Mục đích

Thư mục `data/` dùng để quản lý tài liệu và thông tin liên quan đến dữ liệu đầu vào của dự án Legal Law Assistant.

Dữ liệu được sử dụng trong quá trình chuẩn bị tài liệu, xây dựng hệ thống RAG và kiểm thử chức năng tra cứu pháp luật.

## 2. Nội dung dự kiến

Thư mục có thể được tổ chức thành các phần sau khi nhóm triển khai:

- `raw/`: tài liệu nguồn ban đầu.
- `processed/`: tài liệu đã được làm sạch và chuẩn hóa.
- `metadata/`: thông tin mô tả tài liệu và nguồn tham khảo.
- `samples/`: dữ liệu mẫu phục vụ kiểm thử, nếu cần.

Đây là cấu trúc dự kiến. Chỉ tạo các thư mục con khi nhóm thực sự cần sử dụng.

## 3. Quy trình xử lý dữ liệu

1. Thu thập tài liệu từ nguồn phù hợp.
2. Kiểm tra nguồn, tính đầy đủ và định dạng tài liệu.
3. Làm sạch và chuẩn hóa nội dung.
4. Chuẩn bị dữ liệu cho quá trình chia đoạn (chunking) và tạo embedding.
5. Kiểm tra kết quả truy xuất và nguồn trích dẫn.

## 4. Quy tắc quản lý dữ liệu

- Ghi rõ nguồn gốc tài liệu khi có thể.
- Không đưa API key, mật khẩu hoặc thông tin bí mật vào repository.
- Kiểm tra quyền sử dụng và điều kiện phân phối tài liệu trước khi đưa lên GitHub.
- Không tải lên dữ liệu lớn hoặc dữ liệu nhạy cảm khi chưa được nhóm thống nhất.
- Không coi tài liệu chưa được xác minh là nguồn pháp luật chính thức.

## 5. Trách nhiệm

Thành viên phụ trách dữ liệu phối hợp với các thành viên RAG để chuẩn bị, làm sạch, chia đoạn và kiểm tra dữ liệu phục vụ hệ thống.

## 6. Trạng thái

Thư mục hiện được thiết lập để mô tả quy trình và quy tắc quản lý dữ liệu. Dữ liệu thực tế sẽ được bổ sung theo tiến độ của nhóm.
