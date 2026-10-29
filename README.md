# Product Management PV

Ứng dụng quản lý sản phẩm nội bộ được xây dựng trên Odoo Community. Hệ thống
cung cấp một nơi tập trung để lưu trữ, cập nhật và tìm kiếm thông tin sản phẩm,
hỗ trợ tư vấn khách hàng và theo dõi cơ bản giá bán, số lượng tồn kho.

## Trạng thái

- Đang trong quá trình Go-live nhằm phát hiện các bug phát sinh trong quá trình khách hàng sử dụng thực tế
- Đang review và viết lại manual test case 

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

