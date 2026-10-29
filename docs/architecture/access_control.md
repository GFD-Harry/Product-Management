# Access Control

| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Ứng dụng | Quản lý sản phẩm nội bộ |
| Nguồn đầu vào | None |
| Phiên bản tài liệu | Official 1 |
| Ngày lập | 17-10-2026 |

Mục tiêu của tài liệu là quy định các thao tác của người dùng trong ứng dụng phù hợp với phân quyền

## 1. Access Right
Access Rights được cấu hình theo model bằng `ir.model.access.csv`


| Model | Admin | Viewer |
|---|---|---|
| Category | Read, Write, Create, Unlink | Read |
| Category Field | Read, Write, Create, Unlink | Read |
| Category Field Option | Read, Write, Create, Unlink | Read |
| Product | Read, Write, Create, Unlink | Read |
| Brand | Read, Write, Create, Unlink | Read |
| Product Field Value | Read, Write, Create, Unlink | Read |
| Product Compare Wizard | Kế thừa quyền Viewer | Read, Write, Create, Unlink |
| Product Compare Result Line | Kế thừa quyền Viewer | Read, Write, Create, Unlink |
| Account Create Wizard | Read, Write, Create, Unlink | Không có ACL được khai báo |
| Account Edit Wizard | Read, Write, Create, Unlink | Không có ACL được khai báo |
| Account Password Wizard | Read, Write, Create, Unlink | Không có ACL được khai báo |
| Dashboard | Kế thừa quyền Viewer | Read |

## 2. Menu and UI Access

| Menu / Action | Admin | Viewer |
|---|---|---|
| Dashboard | Có | Có |
| Xem danh sách sản phẩm | Có | Có |
| Xem chi tiết sản phẩm | Có | Có |
| Tạo / chỉnh sửa sản phẩm | Có | Không |
| Tìm kiếm, lọc, sắp xếp sản phẩm | Có | Có |
| So sánh sản phẩm | Có | Có |
| Xem danh mục và các field | Có | Có |
| Tạo / chỉnh sửa danh mục và field | Có | Không |
| Xem thương hiệu | Có | Có |
| Xem danh sách tài khoản | Có | Không |
| Tạo tài khoản | Có | Không |
| Chỉnh sửa tài khoản | Có | Không |
| Đổi / đặt lại mật khẩu tài khoản | Có | Không |

## 3. Notes
