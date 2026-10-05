# Odoo Project Instructions

- Dự án sử dụng Odoo 19, Python và PostgreSQL.
- Ưu tiên sử dụng Odoo ORM; chỉ dùng raw SQL khi thực sự cần thiết.
- Không chỉnh sửa Odoo core; mọi tùy chỉnh phải nằm trong custom modules.
- Tuân theo cấu trúc và convention hiện tại của project.
- Đặt business logic trong model thay vì view hoặc controller khi phù hợp.
- Khi thêm model, field hoặc chức năng mới, kiểm tra ACL, record rules và quyền truy cập liên quan.
- Khi sửa XML view, đảm bảo field, action, menu và external ID tồn tại và đúng dependency.
- Không tự ý thay đổi database schema, manifest dependency hoặc cấu hình production ngoài phạm vi yêu cầu.