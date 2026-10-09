# Quy trình làm việc nhóm trên GitHub

## 1. Mục tiêu

Tài liệu này quy định quy trình tạo nhánh, phát triển chức năng, tạo Pull Request, kiểm thử và hợp nhất code trong dự án Legal Law Assistant.

## 2. Quy ước nhánh

### `main`

Chứa phiên bản ổn định được nhóm chấp nhận.

Không tự ý commit trực tiếp lên `main`.

### `develop`

Chứa các thay đổi đã được xem xét và hợp nhất để tích hợp giữa các thành viên.

Không tự ý commit trực tiếp lên `develop` nếu repository đã bật quy tắc bảo vệ nhánh.

### Nhánh tính năng

Ví dụ:
- `feature/backend-api`
- `feature/rag-retrieval`
- `feature/agent`
- `feature/citation-validator`
- `feature/frontend`
- `feature/devops`

Tên nhánh cần thể hiện rõ mục đích thay đổi.

## 3. Quy trình thực hiện công việc

### Bước 1. Nhận nhiệm vụ

- Xác định nội dung công việc.
- Tạo hoặc cập nhật GitHub Issue nếu nhóm đang sử dụng Issues.
- Xác định người phụ trách và tiêu chí hoàn thành.

### Bước 2. Cập nhật nhánh gốc

Trước khi làm việc, cập nhật nhánh cơ sở theo quy trình của nhóm để hạn chế xung đột.

Nếu làm việc bằng Git CLI, có thể sử dụng:

```bash
git switch develop
git pull origin develop
git switch -c feature/ten-cong-viec
```

Nếu nhánh tính năng đã tồn tại, chuyển sang nhánh đó thay vì tạo lại.

### Bước 3. Thực hiện thay đổi

- Chỉ sửa các tệp thuộc phạm vi nhiệm vụ.
- Không đưa khóa API hoặc tệp `.env` chứa thông tin bí mật vào commit.
- Kiểm tra các thay đổi trước khi gửi lên GitHub.

### Bước 4. Commit

Dùng thông điệp commit ngắn gọn, mô tả đúng nội dung thay đổi.

Ví dụ:
- `docs: add architecture documentation`
- `feat: add document retrieval`
- `fix: handle empty query`
- `test: add citation validator tests`
- `chore: update repository structure`

### Bước 5. Push nhánh

Đẩy nhánh tính năng lên GitHub bằng công cụ nhóm sử dụng.

Ví dụ với Git CLI:

```bash
git push -u origin feature/ten-cong-viec
```

### Bước 6. Tạo Pull Request

- Chọn nhánh nguồn là nhánh tính năng.
- Chọn nhánh đích theo quy trình nhóm, thông thường là `develop`.
- Mô tả mục tiêu, các tệp đã thay đổi và cách kiểm thử.
- Liên kết Issue nếu có.
- Chỉ định người review phù hợp.

### Bước 7. Review và kiểm thử

Người review cần kiểm tra:
- Thay đổi có đúng yêu cầu không.
- Có làm hỏng chức năng hiện tại không.
- Có đưa dữ liệu bí mật vào repository không.
- Các bài kiểm thử có phù hợp không.
- Các kiểm tra tự động có thành công không, nếu đã cấu hình.

### Bước 8. Merge

Chỉ merge khi đáp ứng các quy tắc bảo vệ nhánh và yêu cầu review của repository.

Nếu kiểm tra thất bại, sửa lỗi trên nhánh tính năng, cập nhật Pull Request và chờ kiểm tra lại.

### Bước 9. Đồng bộ sau merge

Sau khi merge:
- Kiểm tra thay đổi trên nhánh đích.
- Cập nhật nhánh làm việc trước nhiệm vụ tiếp theo.
- Xóa nhánh tính năng đã hoàn tất nếu không còn cần sử dụng.

## 4. Quy tắc bảo mật

- Không commit `.env`.
- Không công khai API key, mật khẩu, token hoặc private key.
- Sử dụng `.env.example` để mô tả tên biến cần thiết nhưng không chứa giá trị bí mật.
- Nếu bí mật đã bị commit, cần thu hồi hoặc xoay vòng thông tin đó; xóa tệp trong commit mới không đảm bảo bí mật đã biến mất khỏi lịch sử Git.

## 5. Xử lý xung đột

Khi GitHub thông báo có conflict:
1. Không cố merge một cách mù quáng.
2. Xác định các tệp bị xung đột.
3. Trao đổi với thành viên sở hữu phần code liên quan.
4. Hợp nhất các thay đổi có chủ đích.
5. Chạy lại các bài kiểm thử cần thiết.
6. Cập nhật nhánh và kiểm tra Pull Request.

## 6. Tiêu chí hoàn thành nhiệm vụ

- Thay đổi đúng phạm vi.
- Code hoặc tài liệu được cập nhật.
- Không có thông tin bí mật bị đưa vào Git.
- Có mô tả thay đổi trong Pull Request.
- Đã review và kiểm tra theo quy định nhóm.
- Đã merge đúng nhánh đích sau khi đủ điều kiện.
