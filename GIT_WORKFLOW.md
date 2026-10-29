# Quy trình Git

Branch `main` phải luôn ở trạng thái có thể triển khai. Các loại branch:

```text
feature/<task-id>-<short-name>
fix/<task-id>-<short-name>
docs/<short-name>
```

Ví dụ:

```text
feature/SET-02-odoo-environment
fix/SEA-01-product-search
docs/setup-guide
```

Commit gắn với backlog phải bắt đầu bằng mã task:

```text
SET-01: initialize repository structure
PRO-01: add product model
```

Quy trình pull request:

1. Tạo branch từ phiên bản mới nhất của `main`.
2. Mỗi branch xử lý một task hoặc thay đổi có phạm vi rõ ràng.
3. Push branch và mở pull request vào `main`.
4. Mô tả mục đích, thay đổi chính và cách kiểm tra.
5. Ít nhất một thành viên khác review.
6. Chỉ merge khi tiêu chí hoàn thành và CI đều đạt.
7. Ưu tiên squash merge.

Git tag phát hành sử dụng Semantic Versioning, ví dụ `v0.1.0`, `v1.0.0-rc.1`
và `v1.0.0`. Không dùng tag `dev` hoặc `prod` có thể bị di chuyển làm định danh
duy nhất.
