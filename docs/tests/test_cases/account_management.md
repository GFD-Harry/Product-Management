# Manual Test Cases — Account Management

| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Phiên bản tài liệu | Official |
| Ngày lập | 18-10-2026 |

## 1. Purpose
- Mục tiêu của testing Account Managment là xác nhận Admin có thể quản lý tài khoản chính xác: gồm tạo tài khoản, cập nhật thông tin, gán role, kích hoạt/hủy kích hoạt account, thiết lập mật khẩu tạm thời. Kiểm thử đảm bảo việc quản lý account đảm bảo đúng access control rules, và bảo vệ quyền đặc biệt của admin. 
## 2. Test cases

### ACC-TC-01. Product Admin mở được màn Account Management
Status: Passed

Test Data:
- User `pm_admin`
- User `pm_viewer`
- User không thuộc Product Management, ví dụ `non_pm_user`

Steps:
1. Login bằng `pm_admin`.
2. Vào `Product Management > Accounts`.
3. Kiểm tra danh sách account.
4. Kiểm tra các cột: Name, Login, Email, Access Role, Active.

Expected Result:
- Product Admin thấy menu `Accounts`.
- Danh sách chỉ hiển thị user thuộc Product Management.
- Không hiển thị user ngoài phạm vi Product Management.
- Access Role hiển thị đơn giản là `Viewer` hoặc `Admin`.

### ACC-TC-02. Product Admin tạo Viewer account mới
Status: Passed

Test Data:
- Name: `TEST - Viewer Create`
- Login: `test.viewer.create@example.com`
- Email: để trống hoặc nhập cùng login
- Active: True

Steps:
1. Login bằng `pm_admin`.
2. Vào `Product Management > Accounts`.
3. Bấm `Create Viewer`.
4. Nhập Name, Login, Email, Active.
5. Bấm `Create`.
6. Kiểm tra account vừa tạo.

Expected Result:
- Account được tạo thành công.
- Account có Access Role = `Viewer`.
- Account active đúng theo giá trị đã nhập.
- Email tự lấy theo Login nếu Email để trống.
- Account mở bằng form Account Management, không mở form user hệ thống đầy đủ.

### ACC-TC-03. Không cho tạo account trùng login
Status: Passed

Test Data:
- Login đã tồn tại: dùng login của `pm_viewer` hoặc account vừa tạo ở ACC-TC-02.

Steps:
1. Login bằng `pm_admin`.
2. Vào `Product Management > Accounts`.
3. Bấm `Create Viewer`.
4. Nhập Login đã tồn tại.
5. Bấm `Create`.

Expected Result:
- Hệ thống không cho tạo.
- Hiển thị lỗi login đã tồn tại.
- Không tạo thêm user mới.

### ACC-TC-04. Product Admin cập nhật thông tin cơ bản và trạng thái account
Status: Passed

Test Data:
- Account `TEST - Viewer Create`

Steps:
1. Login bằng `pm_admin`.
2. Mở account `TEST - Viewer Create`.
3. Bấm `Edit Account`.
4. Đổi Name, Email/Login nếu cần.
5. Set Active = False.
6. Save.
7. Mở lại account.
8. Set Active = True.
9. Save.

Expected Result:
- Name/Login/Email được cập nhật đúng.
- Active = False thì account bị khóa/archive theo cơ chế Odoo.
- Active = True thì account được mở lại.
- Form chính vẫn readonly, chỉnh sửa phải đi qua wizard.

### ACC-TC-05. Product Admin đổi role Viewer/Admin trong phạm vi Product Management
Status: Passed

Test Data:
- Account Viewer test: `TEST - Viewer Create`
- Có ít nhất 2 Product Management Admin active.

Steps:
1. Login bằng `pm_admin`.
2. Mở account Viewer.
3. Bấm `Edit Account`.
4. Đổi Role từ `Viewer` sang `Admin`.
5. Save.
6. Mở lại account.
7. Đổi Role từ `Admin` về `Viewer`.
8. Save.

Expected Result:
- Viewer được nâng lên Admin thành công.
- Admin được hạ về Viewer thành công nếu không vi phạm rule last admin/self downgrade.
- Role chỉ thay đổi trong nhóm Product Management.
- Các group ngoài Product Management của user không bị mất.

### ACC-TC-06. Chặn các role change nguy hiểm
Status: Passed

Test Data:
- User đang login là Product Management Admin.
- Case chỉ còn 1 Product Management Admin active.

Steps:
1. Login bằng Product Management Admin.
2. Mở chính account của mình.
3. Thử đổi Role từ Admin về Viewer.
4. Chuẩn bị case chỉ còn 1 Product Management Admin active.
5. Thử hạ admin cuối cùng xuống Viewer.

Expected Result:
- Không cho Product Admin tự hạ quyền chính mình.
- Không cho hạ quyền Product Management Admin cuối cùng.
- Không cho đổi quyền của Odoo System Admin
- Hệ thống hiển thị lỗi rõ ràng.

### ACC-TC-07. Product Admin set temporary password cho Viewer
Status: Passed

Test Data:
- Account Viewer active: `TEST - Viewer Create`
- Temporary password: `Temp@123456`

Steps:
1. Login bằng `pm_admin`.
2. Mở account Viewer active.
3. Bấm `Set Temporary Password`.
4. Bỏ trống New Password và thử save.
5. Nhập New Password khác Confirm Password và thử save.
6. Nhập đúng New Password và Confirm Password.
7. Save.
8. Logout.
9. Login bằng Viewer với temporary password mới.

Expected Result:
- Không cho save khi thiếu New Password.
- Không cho save khi Confirm Password không khớp.
- Set password thành công khi hợp lệ.
- Viewer login được bằng temporary password mới.

### ACC-TC-08. Viewer không truy cập được Account Management
Status: Passed

Test Data:
- User `pm_viewer`

Steps:
1. Login bằng `pm_viewer`.
2. Vào Product Management.
3. Kiểm tra menu top/sub menu.
4. Thử truy cập trực tiếp URL/action Account Management nếu có.

Expected Result:
- Viewer không thấy menu `Accounts`.
- Viewer không mở được Account Management bằng URL/action trực tiếp.
- Viewer vẫn xem được Products/Categories theo quyền readonly.

### ACC-TC-09. Hiển thị lịch sử hoạt động cơ bản của account
Status: Passed

Test Data:
- Account `TEST - Viewer Create`

Steps:
1. Login bằng `pm_admin`.
2. Mở account test.
3. Kiểm tra vùng `Activity`.
4. Cập nhật account bằng `Edit Account`.
5. Mở lại account.
6. Login bằng account Viewer.
7. Logout và login lại bằng Admin.
8. Kiểm tra lại Last Login nếu Odoo cập nhật.

Expected Result:
- Hiển thị Created By, Created On.
- Hiển thị Last Updated By, Last Updated On.
- Last Login hiển thị nếu Odoo có dữ liệu.
- Thời gian hiển thị theo timezone/user setting của Odoo.

### ACC-TC-10. Kiểm tra thông tin bắt buộc khi tạo và cập nhật account
Status: Passed

Test Data:
- Account: TEST - Viewer Create
- Name: để trống
- Login: để trống hoặc giữ nguyên giá trị hợp lệ tùy trường hợp kiểm thử.

Steps:
1. Login bằng pm_admin.
2. Vào Product Management > Accounts.
3. Bấm Create Viewer.
4. Để trống Name và nhập Login hợp lệ.
5. Bấm Create và kiểm tra kết quả.
6. Tiếp tục thử tạo account với Login để trống và Name hợp lệ.
7. Mở account TEST - Viewer Create.
8. Bấm Edit Account.
9. Xóa Name hoặc Login, lần lượt thử Save.
10. Kiểm tra kết quả sau mỗi lần thử.

Expected Result:
- Hệ thống không cho tạo hoặc cập nhật account khi thiếu trường bắt buộc.
- Hiển thị thông báo lỗi phù hợp.
- Không tạo account mới khi dữ liệu không hợp lệ.
- Thông tin account hiện tại không bị thay đổi khi cập nhật thất bại.