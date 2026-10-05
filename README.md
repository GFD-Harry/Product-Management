# Product Management PV

Ứng dụng quản lý sản phẩm nội bộ được xây dựng trên Odoo Community. Hệ thống
cung cấp một nơi tập trung để lưu trữ, cập nhật và tìm kiếm thông tin sản phẩm,
hỗ trợ tư vấn khách hàng và theo dõi cơ bản giá bán, số lượng tồn kho.

## Trạng thái

Dự án đã có addon nghiệp vụ, dữ liệu Test/UAT, tài liệu kiểm thử
và cấu hình Docker Compose. Công việc hiện tại tập trung vào việc tách
biệt Development, UAT và Production trước khi go-live.

## Công nghệ

- Odoo Community 19.0.
- PostgreSQL 15.
- Docker Engine hoặc Docker Desktop.
- Docker Compose v2.

Development dùng version tag `odoo:19.0` và `postgres:15`. Khi nghiệm thu
hoặc triển khai production, image sẽ được khóa thêm bằng digest.

## Yêu cầu máy phát triển

- Git.
- Docker Engine hoặc Docker Desktop đang hoạt động.
- Docker Compose v2, kiểm tra bằng `docker compose version`.
- Port mặc định `8069` chưa được ứng dụng khác sử dụng.

Không cần cài trực tiếp Odoo, Python hoặc PostgreSQL trên máy phát triển.

Các phiên bản đã kiểm tra trong SET-02:

```text
Docker Engine:  29.1.3
Docker Compose: 2.40.3
Odoo:           19.0-20260723
PostgreSQL:     15.18
```

Image development hiện tại:

```text
Tag:    odoo:19.0
Digest: sha256:e415f9924395e7521245813135112f264b9222bcde3b1d3c2ee9ff073081540a
```

## Odoo development

Tải image chính thức và xác nhận phiên bản:

```bash
docker pull odoo:19.0
docker run --rm odoo:19.0 odoo --version
```

Cấu hình development nằm tại `config/odoo.conf`. Khi container được tích hợp
ở SET-04:

- `config/` được mount vào `/etc/odoo`.
- `addons/` được mount vào `/mnt/extra-addons`.
- Dữ liệu Odoo nằm tại `/var/lib/odoo` và được giữ bằng named volume.

`odoo.conf` không chứa database password hoặc master password. Development
và UAT hiện dùng `.env`; Production dùng `.env.prod` riêng.

## Chuẩn bị file môi trường

```bash
git clone <repository-url>
cd product-management-pv
cp .env.example .env
cp .env.prod.example .env.prod
```

Mở hai file và thay các giá trị có tiền tố `replace_with_`.
Không commit `.env` hoặc `.env.prod`.

Giữ `POSTGRES_USER=odoo` để khớp với cấu hình Odoo hiện tại.
Database Dev/UAT được chọn tường minh bằng `-d` trong lệnh cài
addon, không phụ thuộc vào `ODOO_DATABASE` trong `.env`.

Do Development và UAT dùng chung `.env` và `ODOO_PORT`, không chạy đồng
thời hai project trên cùng một máy. Nếu cần chạy đồng thời, khi đó
mới tách thêm file env hoặc ghi đè port cho một project.

## Triển khai Development

Development dùng Compose project `product-management-dev`, database
`product_management_dev` và addon `product_management_test_data`. Addon dữ
liệu test phụ thuộc vào `product_management`, vì vậy Odoo sẽ tự cài addon
nghiệp vụ nếu database chưa có.

```bash
docker compose -p product-management-dev --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d db

docker compose -p product-management-dev --env-file .env \
  -f compose.yaml -f compose.dev.yaml run --rm odoo \
  -d product_management_dev \
  -i product_management_test_data \
  --stop-after-init --no-http

docker compose -p product-management-dev --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d odoo
```

Truy cập Development tại:

```text
http://localhost:<ODOO_PORT>
```

## Triển khai UAT

UAT dùng Compose project `product-management-uat`, database
`product_management_uat` và addon `product_management_uat_data`. Dữ liệu UAT
chỉ được nạp vào database này.

```bash
docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d db

docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml run --rm odoo \
  -d product_management_uat \
  -i product_management_uat_data \
  --stop-after-init --no-http

docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d odoo
```

Truy cập UAT tại `http://<server-ip>:<ODOO_PORT>` hoặc qua domain UAT
nếu đã cấu hình reverse proxy.

## Triển khai Production

Production dùng Compose project `product-management-prod`, database
`product_management_prod` và chỉ cài addon nghiệp vụ `product_management`.
Không cài `product_management_test_data` hoặc
`product_management_uat_data` trên Production.

```bash
docker compose -p product-management-prod --env-file .env.prod \
  -f compose.yaml -f compose.prod.yaml up -d db

docker compose -p product-management-prod --env-file .env.prod \
  -f compose.yaml -f compose.prod.yaml run --rm odoo \
  -d product_management_prod \
  -i product_management \
  --stop-after-init --no-http

docker compose -p product-management-prod --env-file .env.prod \
  -f compose.yaml -f compose.prod.yaml up -d odoo
```

`compose.prod.yaml` chỉ bind Odoo vào `127.0.0.1`. Production cần được đặt
sau Nginx và HTTPS trước khi cho phép người dùng truy cập.

## Cập nhật addon đã cài

Trước khi update, dừng service Odoo của đúng môi trường. Thay `-i`
bằng `-u`, sau đó khởi động lại Odoo. Ví dụ cho UAT:

```bash
docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml stop odoo

docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml run --rm odoo \
  -d product_management_uat \
  -u product_management,product_management_uat_data \
  --stop-after-init --no-http

docker compose -p product-management-uat --env-file .env \
  -f compose.yaml -f compose.dev.yaml up -d odoo
```

Luôn dùng cùng `-p`, `--env-file` và cặp file Compose cho mọi lệnh
vận hành của một môi trường. Không dùng
`docker compose down -v`; tùy chọn `-v` xóa database và Odoo filestore.

## Docker Compose

- `compose.yaml`: hai service `odoo` và `db`, network, healthcheck và named
  volumes dùng chung.
- `compose.dev.yaml`: publish port ra máy phát triển và mount addon ở chế độ
  ghi để phát triển.
- `compose.prod.yaml`: restart tự động, chỉ bind Odoo vào loopback để đặt sau
  Nginx và dùng cấu hình production.

PostgreSQL phải healthy trước khi Odoo khởi động. Port PostgreSQL `5432` chỉ
hoạt động trong Docker network và không được publish ra host.

Mỗi Compose project tạo network và named volume riêng. Ví dụ:

```text
product-management-dev_db-data
product-management-dev_odoo-data
product-management-uat_db-data
product-management-uat_odoo-data
product-management-prod_db-data
product-management-prod_odoo-data
```

Master password được đọc từ file môi trường, ghi vào file cấu
hình tạm bên trong container bởi `scripts/odoo-entrypoint.sh` và không
được lưu trong repository.
`compose.prod.yaml` mới là cấu hình nền; việc đóng gói addon vào image, khóa
digest, Nginx và HTTPS thuộc Epic 9.

## URL truy cập

```text
Development: http://localhost:<ODOO_PORT trong .env>
UAT:         http://<server-ip>:<ODOO_PORT trong .env>
Production:  https://<production-domain>
```

Production chỉ được mở cho người dùng sau khi tên miền, reverse proxy
và HTTPS đã được cấu hình.

## Cấu trúc repository

```text
product-management-pv/
├── .github/workflows/       GitHub Actions
├── addons/                  Custom Odoo addons
│   ├── product_management/           Addon nghiệp vụ chính
│   ├── product_management_test_data/ Dữ liệu Development/Test
│   └── product_management_uat_data/  Dữ liệu UAT
├── config/                  Cấu hình Odoo
├── docs/                    Tài liệu dự án
├── scripts/                 Quy trình kỹ thuật chạy lặp lại
├── .env.example             Mẫu biến Development/UAT
├── .env.prod.example        Mẫu biến Production
├── .gitignore
├── compose.yaml             Cấu hình container dùng chung
├── compose.dev.yaml         Cấu hình development
└── compose.prod.yaml        Nền cấu hình production
```

`scripts/` chỉ chứa thao tác có nhiều bước hoặc cần thực hiện nhất quán, ví dụ
CI, cập nhật module, backup và restore. Không tạo script chỉ để thay thế một
lệnh Compose đơn giản.

## Database

| Môi trường | Database |
|---|---|
| Development | `product_management_dev` |
| Automated test | `product_management_test` |
| Demo/UAT | `product_management_uat` |
| Production | `product_management_prod` |

Image development:

```text
Tag:    postgres:15
Digest: sha256:74e110c41804365e3915fcc09d5e7a1eff50161aaa94d5da0e58e0cd75ae509c
```

PostgreSQL sử dụng role `odoo`, không sử dụng role `postgres` làm tài khoản
kết nối của Odoo. Trong cấu hình Compose ở SET-04:

- Host database là tên service `db`.
- Port `5432` chỉ mở trong Docker network, không publish ra host.
- Database khởi tạo và password lấy từ file biến môi trường đã chọn.
- Dữ liệu PostgreSQL được giữ trong named volume.

SET-03 đã kiểm tra Odoo 19 tạo database qua Docker network và xác nhận dữ liệu
vẫn tồn tại sau khi container PostgreSQL được tạo lại với cùng volume.

## Addon Odoo

Tên kỹ thuật của module là `product_management`, version hiện tại
`19.0.1.0.0`.

Hai addon dữ liệu `product_management_test_data` và
`product_management_uat_data` đều khai báo `auto_install = False`. Chúng chỉ
được cài khi lệnh triển khai của đúng môi trường chỉ định rõ addon.
Production chỉ cài `product_management`.

## Quy trình Git

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

## Restore Backup từ Cloudclare R2
### 1. Chuẩn bị
Backup gồm 2 file:

- PostgreSQL database: `product_management_prod_YYYY-MM-DD_HH-MM-SS.dump`
- Odoo filestore: `filestore_product_management_prod_YYYY-MM-DD_HH-MM-SS.tar.gz`

Restore trên environment riêng `product-management-restore`.

### 2. Xem các backup trên R2
```bash
rclone ls r2:pv-product-management-backup
```
Chọn cùng timestamp cho db và filestore

### 3. Download Backup
```bash
mkdir -p ~/restore-backup
```

- Download db
```bash
rclone copy \
  r2:pv-product-management-backup/filestore_product_management_prod_YYYY-MM-DD_HH-MM-SS.tar.gz \
  ~/restore-backup/ \
  --s3-no-check-bucket
```

- Download filestores
```bash
rclone copy \
  r2:pv-product-management-backup/filestore_product_management_prod_YYYY-MM-DD_HH-MM-SS.tar.gz \
  ~/restore-backup/ \
  --s3-no-check-bucket
```

- Kiểm tra:
```
ls -lh ~/restore-backup/
```

### 4. Restore DB
- Tạo DB Restore:
```
docker exec product-management-restore-db-1 \
  psql -U odoo -d postgres \
  -c "CREATE DATABASE product_management_restore OWNER odoo;"
```

- Restore
```bash
time docker exec -i product-management-restore-db-1 \
  pg_restore \
  -U odoo \
  -d product_management_restore \
  --no-owner \
  < ~/restore-backup/product_management_prod_YYYY-MM-DD_HH-MM-SS.dump
```

- Kiểm tra
```bash
docker exec product-management-restore-db-1 \
  psql -U odoo -d postgres \
  -c "\l"
```

### 5. Restore Filestore
- Dừng Odoo:
```bash
docker compose -p product-management-restore stop odoo
```

- Tạo thư mục filestore:
```bash
sudo mkdir -p \
/var/lib/docker/volumes/product-management-restore_odoo-data/_data/filestore
```

- Extract backup:
```bash
sudo tar -xzf \
~/restore-backup/filestore_product_management_prod_YYYY-MM-DD_HH-MM-SS.tar.gz \
-C /var/lib/docker/volumes/product-management-restore_odoo-data/_data/filestore
```

Lười

## Xử lý lỗi thiết lập

### Container không chạy

Luôn thêm đúng project name, file biến môi trường và cặp file
Compose. Ví dụ kiểm tra Development:

```bash
docker compose -p product-management-dev --env-file .env \
  -f compose.yaml -f compose.dev.yaml ps

docker compose -p product-management-dev --env-file .env \
  -f compose.yaml -f compose.dev.yaml logs odoo db
```

### Port 8069 đã được sử dụng

Đổi `ODOO_PORT` trong file môi trường tương ứng, sau đó chạy lại
lệnh `up -d odoo` của môi trường đó.

### Odoo không kết nối PostgreSQL

- Kiểm tra service `db` đang chạy.
- Kiểm tra user và password giữa Odoo và PostgreSQL khớp nhau.
- Database host phải là tên service `db`, không phải `localhost`.
- Kiểm tra PostgreSQL đã hoàn tất khởi tạo.

### Không thấy module

- Kiểm tra module nằm tại `addons/product_management`.
- Kiểm tra `addons/` được mount tới `/mnt/extra-addons`.
- Kiểm tra `addons_path`, manifest và các file `__init__.py`.
- Cập nhật Apps List và xem log Odoo.

### Thay mật khẩu PostgreSQL nhưng không có tác dụng

Biến khởi tạo của image PostgreSQL chỉ có tác dụng khi data directory còn
trống. Không xóa volume tùy tiện; hãy đổi mật khẩu trong PostgreSQL hoặc tạo
lại môi trường development có kiểm soát.

### Dữ liệu mất sau khi tạo lại container

Kiểm tra persistent volume cho cả PostgreSQL database và Odoo filestore.

## Kế hoạch

Xem [mục lục kế hoạch](docs/plans/README.md),
[kế hoạch triển khai](docs/plans/implementation_plan.md) và
[kế hoạch tách môi trường](docs/plans/enviroment_separation_plan.md).
