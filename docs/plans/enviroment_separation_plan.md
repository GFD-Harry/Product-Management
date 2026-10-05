# Kế hoạch tách Development, UAT và Production

| Thuộc tính | Giá trị |
|---|---|
| Dự án | Product Management PV |
| Phiên bản tài liệu | Draft 2 |
| Ngày cập nhật | 2026-08-26 |

## 1. Mục tiêu

- Dùng một Git repository và một codebase nghiệp vụ.
- Chạy Development, UAT và Production bằng các Docker Compose project
  độc lập.
- Không dùng chung database, filestore, network hoặc secrets giữa các
  môi trường.
- Chỉ nạp dữ liệu mẫu vào Development/UAT.
- Chỉ deploy lên Production phiên bản đã được nghiệm thu.

## 2. Cấu hình mục tiêu

| Môi trường | Compose project | Database | Addon cài đặt | Source |
|---|---|---|---|---|
| Development | `product-management-dev` | `product_management_dev` | `product_management_test_data` | Branch đang phát triển |
| UAT | `product-management-uat` | `product_management_uat` | `product_management_uat_data` | `main` hoặc release candidate |
| Production | `product-management-prod` | `product_management_prod` | Chỉ `product_management` | Stable Git tag |

Hai addon dữ liệu phụ thuộc vào `product_management`, nên khi cài addon
Test/UAT, Odoo sẽ tự cài addon nghiệp vụ nếu cần. Cả hai addon dữ
liệu phải giữ `auto_install = False`.

Trên VPS có thể dùng hai checkout từ cùng repository:

```text
/opt/product-management/
├── uat/          # main hoặc release candidate
└── production/   # stable Git tag
```

## 3. Quy ước trạng thái

- `Not Started`: chưa thực hiện.
- `In Progress`: đang thực hiện.
- `Blocked`: không thể tiếp tục cho đến khi có quyết định hoặc điều
  kiện bên ngoài.
- `Done`: đã thực hiện và có thể kiểm tra.
- `Deferred`: chủ động để lại sau.

## 4. Danh sách công việc

### 4.1. Tách code và dữ liệu mẫu

| Status | ID | Task |
|---|---|---|
| Done | ENV-01 | Tách dữ liệu Test và UAT khỏi addon `product_management` thành hai addon riêng. |
| Done | ENV-02 | Đặt hai addon dữ liệu thành `auto_install = False`; Production chỉ cài `product_management`. |
| Not Started | ENV-03 | Cài `product_management` trên database sạch và xác nhận không có dữ liệu Test/UAT. |

### 4.2. Cấu hình và cách ly môi trường

| Status | ID | Task |
|---|---|---|
| Done | ENV-04 | Tạo cấu hình Production nền: `compose.prod.yaml`, `odoo.prod.conf` và `.env.prod.example`. |
| Done | ENV-05 | Ghi lệnh triển khai Dev/UAT/Production với project name, file `.env`, database và addon tương ứng trong README. |
| Not Started | ENV-06 | Tạo ba môi trường thực tế với secrets, port, database và volume riêng. |
| Not Started | ENV-07 | Xác minh ba môi trường không dùng chung container, network, volume hoặc database. |
| Not Started | ENV-08 | Xác minh PostgreSQL không publish port ra host và Odoo Production chỉ bind vào loopback. |

### 4.3. Quản lý phiên bản và release

| Status | ID | Task |
|---|---|---|
| Not Started | ENV-09 | Chốt UAT deploy từ `main` hay từ release-candidate tag/branch. |
| Not Started | ENV-10 | Chốt cách phân phối Production: khuyến nghị checkout stable Git tag và mount `addons/` read-only. |
| Not Started | ENV-11 | Viết quy trình `feature branch → main → UAT → stable tag → Production`. |
| Not Started | ENV-12 | Tạo checklist release có commit/tag, người phê duyệt, thời gian deploy và kết quả smoke test. |
| Not Started | ENV-13 | Viết quy trình rollback về stable tag trước và khôi phục database/filestore khi cần. |

### 4.4. Go-live và vận hành Production

| Status | ID | Task |
|---|---|---|
| Not Started | ENV-14 | Backup database và filestore trước mỗi lần deploy; lưu ít nhất một bản ngoài VPS. |
| Not Started | ENV-15 | Restore thử backup trong môi trường riêng và ghi nhận kết quả. |
| Not Started | ENV-16 | Cấu hình domain, Nginx, HTTPS và firewall; không public trực tiếp PostgreSQL/Odoo. |
| Not Started | ENV-17 | Viết và chạy smoke test Admin/Viewer sau mỗi lần deploy. |
| Not Started | ENV-18 | Theo dõi log, dung lượng volume, backup và tình trạng container. |

### 4.5. Kiểm thử và tài liệu

| Status | ID | Task |
|---|---|---|
| Not Started | ENV-19 | Thêm CI kiểm tra Python, XML, manifest và cài addon trên database sạch. |
| Not Started | ENV-20 | Thêm Odoo automated tests cho phân quyền và business rules quan trọng. |
| Not Started | ENV-21 | Cập nhật tài liệu deploy UAT và checklist go-live theo quy trình đã chốt. |

## 5. Thứ tự thực hiện

1. Hoàn thành kiểm tra database sạch (`ENV-03`).
2. Dựng và xác minh ba môi trường độc lập (`ENV-06` đến `ENV-08`).
3. Chốt cách quản lý version, release và rollback (`ENV-09` đến
   `ENV-13`).
4. Hoàn thành bảo mật, backup và smoke test Production (`ENV-14` đến
   `ENV-18`).
5. Bổ sung CI, automated tests và cập nhật tài liệu (`ENV-19` đến
   `ENV-21`).

## 6. Điều kiện hoàn thành

- Development, UAT và Production có container, network, volume, database và
  secrets riêng.
- Database Production sạch không có dữ liệu Test/UAT.
- Production chạy đúng stable Git tag đã được UAT phê duyệt.
- Production chỉ truy cập qua HTTPS; PostgreSQL và cổng Odoo không public
  trực tiếp.
- Backup database và filestore đã restore thử thành công.
- Smoke test Admin/Viewer đạt sau deploy.
- README, tài liệu UAT và checklist Production phản ánh đúng quy trình
  thực tế.

## 7. Quyết định cần chốt

| ID | Quyết định | Đề xuất hiện tại |
|---|---|---|
| DEC-01 | Source dùng cho UAT | `main` cho UAT liên tục; release-candidate tag cho đợt nghiệm thu chính thức. |
| DEC-02 | Cách phân phối addon Production | Checkout stable Git tag và mount `addons/` read-only. |
| DEC-03 | URL UAT | Domain UAT và HTTPS nếu UAT chạy dài hạn. |
| DEC-04 | Chính sách backup | Chốt lịch, thời gian lưu và nơi lưu ngoài VPS. |
| DEC-05 | Quyền release | Chốt người phê duyệt UAT và người được deploy Production. |
