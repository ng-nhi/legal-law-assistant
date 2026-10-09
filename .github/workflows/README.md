
# GitHub Actions

Thư mục này dành cho các workflow tự động của repository.

## Mục tiêu
- Tự động kiểm tra thay đổi khi có Pull Request.
- Chạy các kiểm thử phù hợp với mã nguồn.
- Hiển thị trạng thái kiểm tra để hỗ trợ review và tích hợp.

## Quy tắc
- Chỉ thêm workflow sau khi xác nhận lệnh cài dependencies và lệnh chạy kiểm thử thực tế.
- Không lưu API key trực tiếp trong file YAML.
- Sử dụng GitHub Actions Secrets khi workflow cần thông tin bí mật.
- Kiểm tra log và sửa lỗi trước khi yêu cầu merge.

## Trạng thái
Workflow CI sẽ được bổ sung sau khi nhóm xác nhận môi trường và bộ kiểm thử.
