# Mô hình dữ liệu (Data Model)

## 1. Tổng quan

Module Product Management sử dụng PostgreSQL để lưu trữ thông tin sản phẩm, danh mục, thương hiệu và các trường dữ liệu động.

Cấu trúc cơ sở dữ liệu, bao gồm bảng, cột, ràng buộc và quan hệ giữa các bảng, được phân tích và tự động tạo tài liệu bằng **SchemaSpy 7.0.2**.

## 2. Tài liệu cấu trúc cơ sở dữ liệu

- **Công cụ:** SchemaSpy 7.0.2
- **Hệ quản trị cơ sở dữ liệu:** PostgreSQL 15
- **Schema:** `public`
- **Số bảng được phân tích:** 12

Tham khảo báo cáo SchemaSpy để xem chi tiết cấu trúc bảng và sơ đồ quan hệ giữa các thực thể (ERD).

## 3. Cập nhật tài liệu

Khi cấu trúc cơ sở dữ liệu thay đổi, cần chạy lại SchemaSpy để tạo báo cáo mới, bảo đảm tài liệu phản ánh cấu trúc cơ sở dữ liệu hiện tại.