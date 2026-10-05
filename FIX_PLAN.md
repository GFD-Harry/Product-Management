# Kế hoạch cô lập và làm sạch sau sự cố UAT

## 1. Mục tiêu và phạm vi

Mục tiêu của kế hoạch này là cô lập sự cố, loại bỏ môi trường UAT đã bị xâm
phạm, kiểm tra phạm vi ảnh hưởng và harden cấu hình. Điểm kết thúc là máy chủ và
repository ở trạng thái sạch, sẵn sàng cho một kế hoạch triển khai riêng trong
tương lai.

Kế hoạch này **không triển khai lại UAT và không triển khai production**.

Các nguyên tắc bắt buộc:

- Không khởi động lại UAT cũ để thử nghiệm.
- Không phục hồi dữ liệu người dùng đã test trên UAT.
- Không xóa hoặc sửa bằng chứng gốc.
- Không dùng `docker compose down -v` trên phạm vi không được xác định rõ.
- Không xóa volume có tên thuộc `product-management-prod`.
- Không mở trực tiếp port Odoo ra Internet.
- Mọi kết luận về danh tính người tấn công phải dựa trên bằng chứng; IP và
  `create_uid` không đủ để quy kết một cá nhân.

## 2. Tóm tắt sự cố đã xác nhận

Ngày 06/09/2026, một client từ `77.239.124.107` đăng nhập thành công tài khoản
Odoo `admin` qua XML-RPC. Client tạo Server Action ID `5679`, sau đó sử dụng
`env.cr.execute()` và PostgreSQL `COPY FROM PROGRAM` để chạy shell trong DB
container.

Payload được tải từ `196.251.121.188:8887`, lưu thành
`/var/lib/postgresql/data/z` và chạy dưới user hệ điều hành `postgres`. Payload
đã tạo tiến trình dùng nhiều CPU/RAM. Request độc hại kéo dài 174 giây khiến
Odoo thực hiện reload nhưng không mở lại socket HTTP trên port 8069.

Chuỗi khai thác thực hiện được vì ứng dụng dùng role PostgreSQL `odoo` có quyền
superuser và `pg_execute_server_program`. Odoo service không có healthcheck nên
Docker vẫn báo container `Up` dù HTTP server đã ngừng phục vụ.

Các IOC chính:

| Loại | Giá trị |
|---|---|
| Source IP | `77.239.124.107` |
| Payload host | `196.251.121.188:8887` |
| Server Action | `ir.actions.server` ID `5679` |
| Action name | `_f77b34a3003a128c_` |
| Payload file | `/var/lib/postgresql/data/z` |
| Process | `./z -d --fetch-only --single` |

Hồ sơ chi tiết được lưu tại:

```text
/root/workspace/uat-incident-2026-09-07/
/root/workspace/uat-incident-2026-09-07.tar.gz
```

## 3. Giai đoạn 1 — Thu thập và bảo toàn bằng chứng

### Mục tiêu

Giữ lại đủ thông tin để điều tra và chứng minh tính toàn vẹn của hiện trường
trước khi dừng hoặc xóa tài nguyên bị nhiễm.

### Công việc

- [x] Thu thập log Odoo và PostgreSQL.
- [x] Ghi nhận trạng thái container, process, socket và firewall.
- [x] Xuất Server Action độc hại `5679` ở dạng văn bản.
- [x] Ghi nhận metadata và SHA-256 của payload `z` mà không sao chép/chạy nó.
- [x] Lập timeline và danh sách IOC.
- [x] Phân loại bằng chứng theo thư mục.
- [x] Tạo checksum cho các tệp bằng chứng.
- [x] Đóng gói hồ sơ thành `uat-incident-2026-09-07.tar.gz`.
- [ ] Sao chép archive bằng chứng sang nơi lưu trữ an toàn ngoài máy chủ.
- [ ] Xác minh checksum của bản sao bên ngoài.

### Điều kiện hoàn thành

- Có ít nhất hai bản sao bằng chứng.
- Một bản nằm ngoài máy chủ đang điều tra.
- Tất cả checksum trả về `OK`.
- File payload không được mở hoặc thực thi.

## 4. Giai đoạn 2 — Cô lập toàn bộ hệ thống

### Mục tiêu

Chấm dứt hoạt động của payload và bảo đảm môi trường hiện tại không tiếp tục
phục vụ hoặc giao tiếp với Internet.

### Công việc

- [ ] Kiểm tra lại trạng thái container vì lần dừng trước đã bị hủy giữa chừng.
- [ ] Dừng Odoo UAT để đóng port public 8069.
- [ ] Dừng PostgreSQL UAT để kết thúc payload và phiên `COPY`.
- [ ] Dừng production hiện tại trong thời gian kiểm tra.
- [ ] Giữ nguyên volume production.
- [ ] Xác minh port 8069 và 8070 không còn lắng nghe.
- [ ] Xác minh không còn process `z` đang chạy.
- [ ] Ghi lại trạng thái sau cô lập vào hồ sơ sự cố.

### Điều kiện hoàn thành

```text
UAT Odoo:       stopped
UAT PostgreSQL: stopped
Production:     stopped
Port 8069:      closed
Port 8070:      closed
Payload z:      không còn chạy
```

## 5. Giai đoạn 3 — Loại bỏ UAT nhiễm và kiểm tra phạm vi

### 5.1. Loại bỏ UAT nhiễm

Do không có nhu cầu giữ dữ liệu người dùng đã test:

- [ ] Xác minh lại archive và checksum trước thao tác phá hủy.
- [ ] Xóa container UAT.
- [ ] Xóa network UAT.
- [ ] Xóa chính xác volume `product-management-uat_db-data`.
- [ ] Xóa chính xác volume `product-management-uat_odoo-data`.
- [ ] Không restore database hoặc filestore UAT cũ.
- [ ] Giữ snapshot/bằng chứng ở trạng thái ngoại tuyến.
- [ ] Xác minh không còn tài nguyên Docker mang tên `product-management-uat`.

### 5.2. Kiểm tra host

- [ ] Kiểm tra process bất thường.
- [ ] Kiểm tra file mới/file thực thi trong `/tmp`, `/var/tmp` và `/dev/shm`.
- [ ] Kiểm tra cron job và systemd service.
- [ ] Kiểm tra SSH `authorized_keys` và lịch sử đăng nhập.
- [ ] Kiểm tra kết nối mạng và DNS bất thường.
- [ ] Kiểm tra container, image và volume lạ được tạo gần thời gian sự cố.
- [ ] Xác minh không container nào mount Docker socket.
- [ ] Theo dõi CPU, RAM và network sau khi UAT dừng.

### 5.3. Kiểm tra production ngoại tuyến

- [ ] Không khởi động Odoo production trong quá trình kiểm tra.
- [ ] Bảo toàn volume production cho tới khi có kết luận.
- [ ] Kiểm tra log và metadata container production.
- [ ] Tìm IOC, payload `z`, Server Action và tài khoản/API key bất thường.
- [ ] Kiểm tra production có dùng lại credential của UAT hay không.
- [ ] Nếu dữ liệu production chưa có giá trị, chuẩn bị loại bỏ và dựng mới sau.
- [ ] Nếu cần giữ dữ liệu, tạo snapshot rồi chỉ phân tích trên bản sao cách ly.

### Cổng quyết định

- Không có dấu vết ngoài UAT: tiếp tục giai đoạn hardening.
- Có dấu vết trong production: đánh dấu production là compromised.
- Có persistence hoặc payload trên host: dừng kế hoạch và rebuild host sạch
  trước khi chuẩn bị triển khai.

## 6. Giai đoạn 4 — Thu hồi credential và harden cấu hình offline

### 6.1. Credential

- [ ] Đổi Odoo master password.
- [ ] Đổi mật khẩu tài khoản Odoo admin.
- [ ] Đổi mật khẩu PostgreSQL UAT và production.
- [ ] Thu hồi API key/token liên quan.
- [ ] Đổi credential ở các hệ thống khác nếu từng dùng lại cùng giá trị.
- [ ] Rà soát và thay SSH key nếu có khả năng bị lộ.
- [ ] Tạo `.env.uat` và `.env.prod` riêng.
- [ ] Xác minh secret không được commit vào Git hoặc ghi vào tài liệu/log.

### 6.2. PostgreSQL

Không dùng role ứng dụng làm tài khoản khởi tạo PostgreSQL. Mô hình mục tiêu:

```text
postgres/admin role -> chỉ dùng để khởi tạo và quản trị
odoo app role       -> chỉ dùng bởi ứng dụng Odoo
```

Role ứng dụng `odoo` phải có:

```text
NOSUPERUSER
NOCREATEROLE
NOREPLICATION
không có pg_execute_server_program
```

Checklist:

- [ ] Tách biến môi trường quản trị DB khỏi credential của ứng dụng.
- [ ] Thêm init script tạo role ứng dụng với quyền tối thiểu.
- [ ] Không cấp lại `pg_execute_server_program` cho role ứng dụng.
- [ ] Thêm kiểm tra tự động xác nhận `rolsuper = false`.

### 6.3. Odoo và Docker

- [ ] Bind Odoo vào `127.0.0.1`, không dùng `0.0.0.0`.
- [ ] Không publish trực tiếp port 8069 ra Internet.
- [ ] Thêm healthcheck HTTP thực tế cho Odoo.
- [ ] Tách project, network, volume và env theo môi trường.
- [ ] Xác minh không mount Docker socket.
- [ ] Dùng read-only mount/filesystem khi phù hợp.
- [ ] Đặt giới hạn CPU và RAM cho container.
- [ ] Pin image bằng version/digest đã kiểm tra.
- [ ] Rà soát source code, addon và image trước khi sử dụng.
- [ ] Hạn chế XML-RPC nếu không có nhu cầu tích hợp.

### 6.4. Thiết kế truy cập tương lai

Chỉ chuẩn bị cấu hình, chưa triển khai:

- [ ] VPN hoặc SSH tunnel cho quản trị.
- [ ] Nginx reverse proxy.
- [ ] IP whitelist hoặc lớp xác thực bổ sung cho UAT.
- [ ] HTTPS cho production.
- [ ] Rate limit và cảnh báo đăng nhập thất bại.

### Điều kiện hoàn thành

- Cấu hình mới qua kiểm tra cú pháp.
- Không có secret trong Git.
- Role ứng dụng không thể chạy `COPY FROM PROGRAM`.
- Không có container UAT/production nào được khởi động.

## 7. Giai đoạn 5 — Xác minh sạch và chốt trạng thái sẵn sàng

### Checklist cuối

- [ ] UAT nhiễm đã bị loại bỏ.
- [ ] Không còn container, network hoặc volume UAT cũ.
- [ ] Production cũ đang dừng và đã được kiểm tra.
- [ ] Không có port 8069/8070 public.
- [ ] Không còn process/payload `z` ngoài bản bằng chứng.
- [ ] Không còn kết nối tới các IOC đã biết.
- [ ] Không có cron, service, user hoặc SSH key bất thường.
- [ ] Credential cũ đã được thu hồi.
- [ ] Source/config đã được rà soát và harden.
- [ ] Mô hình quyền PostgreSQL mới đã được định nghĩa và kiểm thử offline.
- [ ] Healthcheck và giới hạn tài nguyên đã được khai báo.
- [ ] Checksum bằng chứng vẫn trả về `OK`.
- [ ] Báo cáo ghi rõ nội dung đã xác nhận và nội dung chưa thể xác nhận.
- [ ] Có checklist triển khai mới nhưng chưa chạy `docker compose up`.

### Trạng thái kết thúc mong muốn

```text
Bằng chứng:       đã bảo toàn
UAT bị nhiễm:     đã loại bỏ
Production cũ:    đã dừng và kiểm tra
Host:             không còn dấu hiệu hoạt động độc hại
Credential cũ:    đã thu hồi
Source/config:    đã harden
UAT mới:          chưa triển khai
Production mới:   chưa triển khai
```

## 8. Thứ tự thực hiện tóm tắt

1. Bảo toàn và sao chép bằng chứng ra ngoài máy chủ.
2. Dừng/cô lập UAT và production hiện tại.
3. Xóa UAT nhiễm, kiểm tra host và production ngoại tuyến.
4. Thu hồi credential và harden repository/config.
5. Xác minh sạch và dừng tại trạng thái sẵn sàng triển khai.

