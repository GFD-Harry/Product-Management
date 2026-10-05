# UAT Guide
| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Ứng dụng | Quản lý sản phẩm nội bộ |
| Nguồn đầu vào |  |
| Phiên bản tài liệu | Draft 2 |
| Ngày lập | 2026-08-22 |

## 1. Objective

Xác nhận Product Management MVP đáp ứng đủ các luồng nghiệp vụ chính của customer trong giai đoạn nghiệm thu (UAT)

## 2. Scope

### In Scope

- Dashboard
- Category Management
- Product Management
- Product Detail / Specifications
- Product Discovery / Search / Filter / Group By
- Product Comparison
- Basic Inventory status
- Account Management
- Access Control cơ bản

### Out of Scope

- Sales / payment / accounting
- Advanced inventory
- AI product suggestion
- Customer portal / external users
- Mobile app riêng
- Production deployment hardening
- CI/CD
- Performance/load testing sâu

## 3. UAT Environment

- URL truy cập: http://160.250.187.247:8069
- Database: product_management_uat
- Branch/build: uat/
- Module version: 1.0.0
- Deploy date: 22-08-2026

Note:

- Đây là môi trường UAT/staging tạm thời.
- Dữ liệu có thể được reset nếu cần.
- Không dùng dữ liệu production.

## 4. UAT Accounts

| Role | Login | Password | Purpose |
|---|---|---|---|
| System Admin | admin | *** | Setup, support kỹ thuật, xử lý lỗi cấu hình (chỉ dành cho dev) |
| Product Admin | vy | 1 | Test luồng quản trị category, product, account. |
| Product Viewer | johnson | 1 | Test luồng xem, tìm kiếm, so sánh sản phẩm. |

## 5. UAT Data

Chuẩn bị dữ liệu đủ cho:

- Categories: Laptop, Smartphone, Accessory
- Brands: Dell, Apple, Samsung, Logitech
- Category fields/options: CPU, RAM, Storage, Screen Size, Warranty, Color...
- Products:
  - Available product
  - Draft product
  - Discontinued product
  - Low stock product
  - Out of stock product
  - Product thiếu required specification
  - 2-4 products cùng category để compare

## 6. Feature Checklist

Quy ước trạng thái: `Not Run`, `Pass`, `Fail`, `Blocked`, `Skipped`.
Đây là checklist gợi ý, user có thể thay đổi tùy theo mong đợi (đối chiếu với scope từ  file customer.pdf). Không care tới cột test case nhé.

| Status | ID | Area | Nội dung cần kiểm tra | Kết quả mong đợi | Test case tham chiếu |
|---|---|---|---|---|---|
| Not Run | UAT-DAS-01 | Dashboard | Mở Dashboard bằng tài khoản Admin và Viewer. | Hiển thị đúng số liệu tổng quan và danh sách sản phẩm cần chú ý; user không gặp lỗi quyền truy cập. | Chưa có test case chi tiết |
| Not Run | UAT-CAT-01 | Category Management | Admin tạo category có Name, Description và Parent Category, sau đó cập nhật thông tin. | Category được tạo/cập nhật thành công; bắt buộc nhập Name; quan hệ cha-con được lưu đúng. | CAT-TC-01, CAT-TC-02, CAT-TC-04 |
| Not Run | UAT-CAT-02 | Category Management | Admin archive và restore category. | Category biến mất khỏi danh sách active, xuất hiện khi lọc Archived và trở lại danh sách sau khi restore. | CAT-TC-03 |
| Not Run | UAT-CAT-03 | Category Management | Admin tạo/cập nhật/archive dynamic field kiểu Text, Char, Boolean và cấu hình Required. | Field lưu đúng type, required, help và thứ tự; field inactive không còn dùng để nhập liệu chính. | CAT-TC-05, CAT-TC-06 |
| Not Run | UAT-CAT-04 | Category Management | Admin tạo Selection field, thêm/sửa/archive các option. | Options thuộc đúng field và thay đổi được lưu chính xác. | CAT-TC-07, BR-FIELD-TC-06 |
| Not Run | UAT-CAT-05 | Category Management | Thêm hoặc archive field của category đang có product. | Specifications của product được đồng bộ; dữ liệu specification khác không bị mất. | CAT-TC-08 |
| Not Run | UAT-CAT-06 | Category Management | Mở tab Audit Information của category. | Hiển thị readonly Created By/On và Last Updated By/On. | CAT-TC-09 |
| Not Run | UAT-PRO-01 | Product Management | Admin tạo product Draft với category, brand, giá và số lượng; sau đó cập nhật lại. | Product được tạo/cập nhật; dữ liệu lưu đúng; stock status tự tính theo quantity. | PRO-TC-01 |
| Not Run | UAT-PRO-02 | Product Management | Lưu product thiếu Name hoặc Category. | Hệ thống chặn lưu và chỉ rõ trường bắt buộc còn thiếu. | PRO-TC-02 |
| Not Run | UAT-PRO-03 | Product Detail / Specifications | Mở product và nhập đủ các kiểu specification của category. | Chỉ hiển thị field thuộc đúng category; giá trị được lưu và hiển thị đúng khi mở lại. | PRO-TC-03 |
| Not Run | UAT-PRO-04 | Product Management | Chuyển product thiếu required specification sang Available, sau đó bổ sung đủ dữ liệu và thử lại. | Lần đầu bị chặn và nêu field còn thiếu; khi đủ dữ liệu thì chuyển Available thành công. | PRO-TC-04, BR-FIELD-TC-01 đến BR-FIELD-TC-05 |
| Not Run | UAT-PRO-05 | Product Management | Đổi category của product. | Specifications đồng bộ theo category mới; field của category cũ không còn là active specification. | PRO-TC-05 |
| Not Run | UAT-PRO-06 | Product Management | Thử archive product Available; chuyển sang Discontinued rồi archive và restore. | Không archive được product Available; product Discontinued archive được và có thể tìm bằng filter Archived. | PRO-TC-06, BR-STATUS-TC-01, BR-STATUS-TC-02 |
| Not Run | UAT-PRO-07 | Product Management | Nhập giá bán âm, bằng 0 và dương. | Giá âm bị chặn; giá bằng 0 và giá dương hợp lệ được lưu đúng. | BR-PRICE-TC-01 đến BR-PRICE-TC-04 |
| Not Run | UAT-DIS-01 | Product Discovery | Mở ứng dụng Product Management. | Mặc định mở Product List với các cột chính; danh sách ưu tiên product active và Available. | DIS-TC-01, DIS-TC-02 |
| Not Run | UAT-DIS-02 | Product Discovery | Search theo tên, mã nội bộ, category, brand và purpose. | Chỉ trả về các product phù hợp với từ khóa/tiêu chí tìm kiếm. | DIS-TC-03 |
| Not Run | UAT-DIS-03 | Product Discovery | Filter theo Product Status và Stock Status. | Danh sách chỉ hiển thị product đúng trạng thái; có thể bỏ filter để quay về danh sách mong muốn. | DIS-TC-04 |
| Not Run | UAT-DIS-04 | Product Discovery | Group By theo Category, Brand, Product Status và Stock Status. | Product được gom đúng nhóm và user có thể mở/thu từng nhóm. | DIS-TC-05 |
| Not Run | UAT-CMP-01 | Product Comparison | Chọn 2-4 product cùng category và mở Compare Products. | Wizard mở thành công, hiển thị product theo cột và tiêu chí chung/specification theo dòng. | CMP-TC-01, CMP-TC-04 |
| Not Run | UAT-CMP-02 | Product Comparison | Thử compare 1 product, 5 product và các product khác category. | Hệ thống chặn từng trường hợp và hiển thị cảnh báo rõ ràng. | CMP-TC-02, CMP-TC-03 |
| Not Run | UAT-CMP-03 | Product Comparison | Chọn/bỏ tiêu chí trong bảng compare và thử chỉnh dữ liệu. | Bảng cập nhật theo tiêu chí đã chọn và luôn ở chế độ readonly. | CMP-TC-04, CMP-TC-05 |
| Not Run | UAT-INV-01 | Basic Inventory | Nhập quantity âm, bằng 0, từ 1-5 và lớn hơn 5. | Số âm bị chặn; 0 = Out of Stock; 1-5 = Low Stock; trên 5 = In Stock. | BR-STOCK-TC-01 đến BR-STOCK-TC-05 |
| Not Run | UAT-INV-02 | Basic Inventory | Thử nhập Stock Status thủ công và đặt product hết hàng ở trạng thái Available. | Stock Status là readonly/tự tính; product quantity 0 vẫn có thể Available nếu đủ dữ liệu bắt buộc. | BR-STOCK-TC-06, BR-STOCK-TC-07 |
| Not Run | UAT-ACC-01 | Account Management | Admin mở danh sách Accounts và tạo Viewer mới. | Chỉ thấy account thuộc Product Management; account mới có role Viewer; Email lấy từ Login nếu để trống. | ACC-TC-01, ACC-TC-02 |
| Not Run | UAT-ACC-02 | Account Management | Tạo account trùng Login và cập nhật Name/Login/Email của account có sẵn. | Login trùng bị chặn; thông tin hợp lệ được cập nhật đúng qua Edit Account. | ACC-TC-03, ACC-TC-04 |
| Not Run | UAT-ACC-03 | Account Management | Khóa và mở khóa account. | Account inactive không đăng nhập được và có thể được mở lại bởi Admin. | ACC-TC-04 |
| Not Run | UAT-ACC-04 | Account Management | Đổi role Viewer/Admin; thử tự hạ quyền và hạ quyền Admin cuối cùng. | Đổi role hợp lệ thành công; thao tác nguy hiểm bị chặn; group ngoài Product Management không bị thay đổi. | ACC-TC-05, ACC-TC-06 |
| Not Run | UAT-ACC-05 | Account Management | Set temporary password với dữ liệu trống, confirm không khớp và dữ liệu hợp lệ. | Dữ liệu không hợp lệ bị chặn; password hợp lệ được đặt và Viewer đăng nhập được. | ACC-TC-07 |
| Not Run | UAT-ACC-06 | Account Management | Kiểm tra Activity/Audit của account sau khi tạo, cập nhật và đăng nhập. | Hiển thị Created, Last Updated và Last Login khi Odoo có dữ liệu. | ACC-TC-09 |
| Not Run | UAT-ACL-01 | Access Control | Viewer mở Products/Categories và thử tạo, sửa, xóa hoặc archive dữ liệu. | Viewer chỉ xem được product/category/specification và không thực hiện được thao tác quản trị. | PRO-TC-07, CAT-TC-10 |
| Not Run | UAT-ACL-02 | Access Control | Viewer kiểm tra menu Accounts và thử truy cập trực tiếp URL/action quản lý account. | Không thấy menu Accounts và không truy cập trực tiếp được chức năng quản trị account. | ACC-TC-08 |

Lưu ý: tài liệu `access_control.md` hiện đánh dấu `Skipped`; các tiêu chí quyền trong checklist này được tham chiếu từ test case Product, Category và Account Management đã có.

## 7. Issue Reporting

Khi gặp lỗi, ghi theo format:

```text
Feature:
Account used:
Steps:
Expected:
Actual:
Screenshot(recommended):
Severity (High/Medium/Low):
Notes:
```