# Production Go-live Checklist

| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Phiên bản tài liệu | Draft 1 |
| Ngày go-live dự kiến |  |
| Production URL |  |
| Release/Tag |  |

## 1. Tách dữ liệu UAT

- [x] Bỏ các file `data/uat/*` khỏi manifest production.
- [ ] Không đưa tài khoản và dữ liệu test/UAT vào production.

## 2. Chuẩn bị database production

- [ ] Tạo database `product_management_prod`.
- [ ] Tạo dữ liệu production sạch hoặc làm sạch dữ liệu UAT trước khi chuyển.
- [ ] Tạo tài khoản người dùng thật và sử dụng mật khẩu mới.

## 3. Cấu hình truy cập production

- [ ] Chuẩn bị domain và trỏ DNS về VPS.
- [ ] Cấu hình Nginx reverse proxy và HTTPS.
- [ ] Không public trực tiếp port Odoo `8069`.
- [ ] Kiểm tra production sử dụng `dbfilter`, `list_db = False` và `proxy_mode = True`.

## 4. Backup và restore

- [ ] Backup PostgreSQL trước khi go-live.
- [ ] Backup Odoo filestore trong volume `odoo-data`.
- [ ] Lưu ít nhất một bản backup ngoài VPS production.
- [ ] Restore thử và xác nhận dữ liệu, ảnh/attachment hoạt động.

## 5. Triển khai release

- [ ] Chốt commit và tạo release tag, ví dụ `v1.0.0`.
- [ ] Deploy bằng `compose.yaml` và `compose.prod.yaml`.
- [ ] Cài đặt hoặc cập nhật module `product_management`.
- [ ] Restart services và kiểm tra các container hoạt động bình thường.

## 6. Kiểm tra và bàn giao

- [ ] Product Management Admin và Viewer đăng nhập thành công.
- [ ] Kiểm tra nhanh Dashboard, Category, Product, Search và Comparison.
- [ ] Xác nhận Viewer không thể tạo, sửa hoặc xóa dữ liệu quản trị.
- [ ] Khách hàng đăng nhập và xác nhận có thể bắt đầu sử dụng.
- [ ] Ghi nhận ngày giờ go-live.
- [ ] Bắt đầu giai đoạn hỗ trợ miễn phí hai tháng sau go-live.

## Xác nhận go-live

| Nội dung | Giá trị |
|---|---|
| Ngày giờ go-live thực tế |  |
| Người triển khai |  |
| Đại diện khách hàng xác nhận |  |
| Ghi chú hoặc issue còn lại |  |
