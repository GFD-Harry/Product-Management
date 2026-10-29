# Quản lý sản phẩm (Product Management)

Custom module trên Odoo 19, phiên bản chính thức đầu tiên, phục vụ nhu cầu quản lý/tư vấn thông tin sản phẩm nội bộ.
**Tên kỹ thuật:** `product_management`
**Phiên bản:** `19.0.1.0.0`
## 1. Chức năng chính

| Chức năng | Mô tả |
|---|---|
| **Quản lý sản phẩm** | Quản lý danh mục, thương hiệu, giá, hình ảnh, mục đích sử dụng, số lượng tồn kho, trạng thái sản phẩm và thông số kỹ thuật theo từng danh mục. |
| **Quản lý danh mục** | Tạo và quản lý danh mục sản phẩm; cấu hình các trường thông tin động và các tùy chọn lựa chọn tương ứng. |
| **Tra cứu sản phẩm** | Hỗ trợ tìm kiếm, lọc và nhóm sản phẩm trong danh sách. |
| **Bảng điều khiển** | Tổng hợp số lượng sản phẩm, các sản phẩm được cập nhật gần đây và danh sách sản phẩm cần chú ý về tồn kho. |
| **So sánh sản phẩm** | So sánh thông tin giữa các sản phẩm thuộc cùng một danh mục. |
| **Quản lý tồn kho cơ bản** | Theo dõi số lượng tồn kho và trạng thái tồn kho được tính toán tự động. |
| **Quản lý tài khoản và phân quyền** | Hỗ trợ hai nhóm quyền: Product Management Viewer và Product Management Admin. |

## 2. Ngoài phạm vi

Module tập trung vào quản lý thông tin sản phẩm nội bộ, không triển khai đầy đủ các quy trình nghiệp vụ thuộc những phân hệ khác của Odoo, bao gồm:

- **Mua hàng (Purchase):** Quy trình yêu cầu mua hàng, đơn mua hàng và các nghiệp vụ liên quan.
- **Bán hàng (Sales):** Quy trình báo giá, đơn bán hàng và các nghiệp vụ liên quan.
- **Kho (Inventory):** Quy trình nhập, xuất, điều chuyển và các nghiệp vụ quản lý kho nâng cao.
- **Kế toán (Accounting):** Các nghiệp vụ kế toán và tài chính liên quan.
- **Sản xuất (Manufacturing):** Quy trình hoạch định và thực hiện sản xuất.

Các nghiệp vụ trên không thuộc phạm vi chức năng của module trong phiên bản hiện tại.

## 3. Addon Status

| Nhóm hạng mục | Trạng thái | Mô tả |
|---|---|---|
| Development | `Completed` | Các chức năng chính đã hoàn thành, xem tại .... |
| Testing | `In Progress` | Đang trong quá trình clean codebase (dọn dẹp các tài liệu, rút gọn thành những tài liệu thực sự cần thiết). |
| Go-live | `Not Started` | Chưa bắt đầu | 
| Production | `Not Started` | Chưa bắt đầu |
| Other | `Confirmed` | Đồng bộ giữa dữ liệu uat/test bị break | 
