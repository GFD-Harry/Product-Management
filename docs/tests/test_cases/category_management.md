# Category Management Test Case

| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Phiên bản tài liệu | Officiel |
| Ngày lập | 18-10-2026 |

## 1. Scope
Kiểm tra các luồng chính của Category Management:
- Category CRUD cơ bản
- Parent category
- Dynamic fields
- Selection Options
- Archieve / restore
- Audit Information
- Access Controll Admin/Viewer

## 2. Test Cases
### CAT-TC-01. Admin tạo và cập nhật category
Status: Pass

Steps:
1. Login bằng Product Management Admin.
2. Vào `Product Management > Categories`.
3. Tạo category `TEST - Category Create`.
4. Nhập description, sequence, active.
5. Save.
6. Mở lại category vừa tạo.
7. Cập nhật description và sequence.
8. Save.

Expected Result:
- Category được tạo thành công.
- Category hiển thị trong danh sách.
- Thông tin cập nhật được lưu đúng.

### CAT-TC-02. Không cho lưu category thiếu tên
Status: Pass

Steps:
1. Login bằng Product Management Admin.
2. Vào `Product Management > Categories`.
3. Bấm New.
4. Để trống `Name`.
5. Save.

Expected Result:
- Hệ thống không cho lưu.
- Field `Name` được báo là bắt buộc.

### CAT-TC-03. Archive và restore category
Status: Pass

Preconditions:
- Có category active dùng riêng cho test archive.
   
Steps:
1. Login bằng Product Management Admin.
2. Mở category test.
3. Đặt `Active = False`.
4. Save.
5. Kiểm tra category không còn trong danh sách active mặc định.
6. Dùng filter Archived.
7. Mở lại category.
8. Đặt `Active = True`.
9. Save.

Expected Result:
- Category archive thành công.
- Category hiển thị khi filter Archived.
- Category restore thành công và quay lại danh sách active.

### CAT-TC-04. Gán parent category và chặn xóa parent đang được tham chiếu
Status: Pass

Preconditions:
- Có `TEST - Electronics`.
- Có `TEST - Laptop`.

Steps:
1. Login bằng Product Management Admin.
2. Mở `TEST - Laptop`.
3. Set `Parent Category = TEST - Electronics`.
4. Save.
5. Mở `TEST - Electronics`.
6. Thử delete `TEST - Electronics`.

Expected Result:
- `TEST - Laptop` lưu đúng parent category.
- Hệ thống không cho xóa parent category đang được category khác tham chiếu.
- Category con không bị mất dữ liệu.

### CAT-TC-05. Admin tạo dynamic fields nhiều kiểu dữ liệu
Status: Pass

Preconditions:
- Có category `TEST - Laptop`.

Steps:
1. Login bằng Product Management Admin.
2. Mở category `TEST - Laptop`.
3. Trong tab Field, thêm các field:
   - `TEST - CPU Extra`, Field Type = Char, Required = True.
   - `TEST - Detail Note`, Field Type = Text, Required = False.
   - `TEST - Has Touch Screen Extra`, Field Type = Boolean, Required = False.
4. Save.

Expected Result:
- Các dynamic fields được tạo thành công.
- Field type, required và active được lưu đúng.
- Fields thuộc đúng category.

### CAT-TC-06. Admin cập nhật và archive dynamic field
Status: Pass

Preconditions:
- Có category với field `TEST - CPU Extra`.

Steps:
1. Login bằng Product Management Admin.
2. Mở category chứa field.
3. Đổi tên field `TEST - CPU Extra` thành `TEST - Processor Extra`.
4. Cập nhật help và sequence.
5. Save.
6. Đặt field này `Active = False`.
7. Save.

Expected Result:
- Field được cập nhật thành công.
- Help và sequence được lưu đúng.
- Field archive thành công và không còn là active field của category.

### CAT-TC-07. Admin tạo và cập nhật selection field/options
Status: Pass

Preconditions:
- Có category `TEST - Laptop`.

Steps:
1. Login bằng Product Management Admin.
2. Mở category `TEST - Laptop`.
3. Thêm field `TEST - Warranty Extra`, Field Type = Selection.
4. Thêm options `12 months` và `24 months`.
5. Save.
6. Đổi option `12 months` thành `1 year`.
7. Archive option `24 months`.
8. Save.

Expected Result:
- Selection field được tạo thành công.
- Options được lưu đúng theo field.
- Option update thành công.

### CAT-TC-08. Dynamic fields đồng bộ sang product thuộc category
Status: Pass

Preconditions:
- Có category `TEST - Laptop`.
- Có product thuộc category `TEST - Laptop`.

Steps:
1. Login bằng Product Management Admin.
2. Mở category `TEST - Laptop`.
3. Thêm một active field mới.
4. Save.
5. Mở product thuộc `TEST - Laptop`.
6. Kiểm tra tab Specifications.
7. Quay lại category và archive field vừa thêm.
8. Mở lại product.

Expected Result:
- Field mới xuất hiện trong specifications của product thuộc category.
- Field inactive không còn là active specification sau khi archive.
- Product không mất các specification khác không liên quan.

### CAT-TC-09. Hiển thị audit information của category
Status: Pass

Preconditions:
- Có category đã được tạo hoặc cập nhật.

Steps:
1. Login bằng Product Management Admin.
2. Mở category.
3. Vào tab Audit Information.

Expected Result:
- Hiển thị Created by.
- Hiển thị Created on.
- Hiển thị Last Updated by.
- Hiển thị Last Updated on.
- Các field audit là readonly.

### CAT-TC-10. Viewer chỉ được xem category và dynamic fields/options
Status: Pass

Steps:
1. Login bằng Product Management Viewer.
2. Vào `Product Management > Categories`.
3. Mở một category có dynamic fields/options.
4. Thử tạo category mới.
5. Thử sửa category.
6. Thử sửa dynamic field hoặc option.
7. Thử xóa category.

Expected Result:
- Viewer xem được Categories.
- Viewer xem được dynamic fields/options.
- Viewer không tạo/sửa/xóa được category.
- Viewer không sửa được dynamic fields/options.

## 3. Open Questions
| ID | Observation | Impact | Decision |
|---|---|---|---|
| CAT-OQ-01 | Category inactive hiện không tự archieve hoặc đổi trạng thái product thuộc category đó | Có thể hơi confuse vè category inactive mà product available | Tạm thời chưa fix | 
| CAT-OQ-02 | Sequence là field kỹ thuật, không nhất thiết cần người dùng chỉnh trong MVP | UI có thể hơi technical | Xóa field sequence |
| CAT-OQ-03 | Khi xóa parent category đang được category con tham chiếu, hệ thống chặn đúng nhưng thông báo còn technical | User có thể khó hiểu | Custom validation message |

## 4. Fixxed Issues During Testing
| ID | Issue | Fix | Verified By |
|---|---|---|---|
| BUG-ACL-01 | Viewer login thành công nhưng không vào được Odoo backend do thiếu `Internal User`. | Added `base.group_user` as implied group of Product Management Viewer. | CAT-TC-10 |