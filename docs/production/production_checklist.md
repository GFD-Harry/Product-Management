# Production Checklist
## 0. Information
## 1. Pre-Flight Checklist
| Category | Item | Value | Status |
|---|---|---|---|
| Server Sizing | CPU | 2 vCPU | Pass |
| Server Sizing | RAM | 4GB | Pass |
| Server Sizing | Disk | 50GB SSD | Pass |
| Workload | Users / Concurrent | ~10 / ~3–4 | Pass |
| Resource Allocation | Workers / RAM | 3 / ~1.5GB | Pass |
| Odoo Configuration | `workers` | 3 | Pass |
| Odoo Configuration | `max_cron_threads` | 1 | Pass |
| Odoo Configuration | `limit_memory_soft` | 536870912 | Pass |
| Odoo Configuration | `limit_memory_hard` | 805306368 | Pass |
| Cloud Provider | Type | VPS — Eztech | Pass |
| Odoo Version | Version | 19.0.0 | Pass |
| Module Inventory | Name | Product Management | Pass |
| Module Inventory | Version / Author | 19.0.1.0.0 / Product Management PV | Pass |
| Module Inventory | Depends | `base` | Pass |
| Module Inventory | Purpose | Manage internal product information; support customer consultation | Pass |

Cấu hình được lựa chọn dựa trên quy mô sử dụng (team 10 người), nhu cầu vận hành thực tế (2-3 người dùng cùng lúc), ngân sách phát triển (<500k/tháng), đảm bảo hệ thống ổn định, đáp ứng nhu cầu và tối ưu tài nguyên máy chủ

## 2. Server Setup Checklist

| Category | Item | Configuration | Status |
|---|---|---|---|
| OS | Host OS | Ubuntu 22.04.1 LTS | Pass |
| OS | Docker Engine | 29.1.3 | Pass |
| OS | Docker Compose | v2.40.3 | Pass |
| Deployment | Runtime | Docker Compose | Pass |
| PostgreSQL | Version | 15 | Pass |
| Python | Management | Managed by Odoo Docker image | Pass |
| wkhtmltopdf | Management | Managed by Odoo Docker image | Pass |
| Odoo System User | Configuration | Not required; deployment uses Docker Compose | Pass |
| Firewall | Software | UFW | Pass |
| Firewall | Status | Active | Pass |
| Firewall | Default incoming | Deny | Pass |
| Firewall | Allowed ports | 22/tcp (SSH), 80/tcp (HTTP), 443/tcp (HTTPS) | Pass |
| Firewall | Odoo ports | 8069/8070 — Not publicly exposed | Pass |
| Firewall | PostgreSQL port | 5432 — Not publicly exposed | Pass |
| Fail2ban | Status | Installed and enabled | Pass |
| Fail2ban | SSH jail | Configured | Pass |
| Fail2ban | Protection | SSH brute-force protection active | Pass |

- OS: `Ubuntu 22.04 LTS` được chọn nhờ tính ổn định, hỗ trợ dài hạn và tương thích Docker
- Firewall và Fail2ban: `UFM` giới hạn các công truy cập công khai, `Fail2ban` phát hiện và chặn các IP có hành vi đăng nhập bất thường (Brute-force) 

### 3. Odoo Configuration Checklist

| Category | Item | Configuration | Status |
|---|---|---|---|
| Master Password | `admin_passwd` | Changed from default | Pass |
| Database Manager | `list_db` | `False` | Pass |
| Workers | CPU | 2 vCPU | Pass |
| Workers | `workers` | 3 | Pass |
| Workers | `max_cron_threads` | 1 | Pass |
| Memory Limits | `limit_memory_soft` | 536870912 (512 MB) | Pass |
| Memory Limits | `limit_memory_hard` | 805306368 (768 MB) | Pass |
| Reverse Proxy | `proxy_mode` | `True` | Pass |
| Reverse Proxy | Nginx | Configured as reverse proxy | Pass |
| Reverse Proxy | `X-Forwarded-For` | Configured | Pass |
| Reverse Proxy | `X-Forwarded-Proto` | Configured | Pass |
| Reverse Proxy | HTTP → HTTPS | Redirect configured | Pass |
| Longpolling / WebSocket | Usage | Not required | Pass |
| Longpolling / WebSocket | Port exposure | No additional port exposed | Pass |

- Các cấu hình quan trọng được lựa chọn nhằm tăng cường bảo mật và đảm bảo hiệu năng vận hành của Odoo production. admin_passwd và list_db = False hạn chế rủi ro quản trị database; workers và memory limits kiểm soát việc sử dụng tài nguyên; proxy_mode kết hợp Nginx và HTTPS đảm bảo xử lý request an toàn, chính xác.
## 4. Security Checklist
### 4.1. HTTPS/SSL

| Item | Configuration / Actual | Status |
|---|---|---|
| SSL Certificate | Let's Encrypt — `pv.harryon.io.vn` | Pass |
| Certificate Validity | Expires 30/12/2026, còn 73 ngày tại thời điểm kiểm tra | Pass |
| HTTPS | Website phản hồi `HTTP 303 SEE OTHER` | Pass |
| HTTP → HTTPS | `HTTP 301 Moved Permanently` | Pass |
| Auto-renewal | `certbot.timer` enabled và active | Pass |
| Renewal Schedule | Chạy 2 lần/ngày | Pass |
| Renewal Test | `certbot renew --dry-run` thành công cho cả 2 certificates | Pass |

- HTTPS/SSL mã hóa dữ liệu trao đổi giữa người dùng và máy chủ, bảo vệ thông tin đăng nhập và dữ liệu nghiệp vụ. Cấu hình chuyển hướng HTTP sang HTTPS đảm bảo các kết nối sử dụng giao thức an toàn. Tự động gia hạn chứng chỉ giúp tránh gián đoạn dịch vụ do chứng chỉ hết hạn.

### 4.2. Nginx Security Header

| Item | Configuration thực tế | Status |
|---|---|---|
| X-Content-Type-Options | `nosniff` | Pass |
| X-Frame-Options | `SAMEORIGIN` | Pass |
| Strict-Transport-Security (HSTS) | `max-age=31536000` (1 năm) | Pass |
| Content-Security-Policy (CSP) | Chưa cấu hình | Deferred |

- Security Headers giúp tăng cường bảo mật cho ứng dụng web, hạn chế các rủi ro như MIME-type sniffing, clickjacking và một số hình thức tấn công dựa trên trình duyệt. CSP được hoãn triển khai để tránh ảnh hưởng đến khả năng tương thích của Odoo.

### 4.3. PostgreSQL Access/SSH Auth/Automatic Security Update/Odoo Admin account

| Category | Item | Configuration thực tế | Status |
|---|---|---|---|
| PostgreSQL Access | Port 5432 | Không publish port ra host | Pass |
| PostgreSQL Access | Docker Network | Odoo kết nối PostgreSQL qua Docker network | Pass |
| SSH Authentication | SSH Key | Chưa triển khai | Pending |
| Automatic Security Update | `unattended-upgrades` | Đã cài đặt, service active | Pass |
| Automatic Security Update | Security Patches | Cấu hình tự động cập nhật bảo mật | Pass* |
| Odoo Admin Account | Default Username | Đã thay đổi | Pass* |
| Odoo Admin Account | Default Password | Đã thay đổi | Pass* |

- Các cấu hình bảo mật giúp hạn chế nguy cơ truy cập trái phép vào database, máy chủ và tài khoản quản trị Odoo. PostgreSQL chỉ giao tiếp qua mạng nội bộ Docker nhằm giảm bề mặt tấn công; unattended-upgrades giúp tự động cập nhật các bản vá bảo mật cho Ubuntu; thay đổi thông tin đăng nhập mặc định giúp bảo vệ tài khoản quản trị. SSH Key chưa được triển khai và cần được xem xét trong giai đoạn tiếp theo.
## 5. Backup Checklist

| Category | Item | Configuration thực tế | Status |
|---|---|---|---|
| Database Backup | Backup Format | `pg_dump -Fc`, filename có timestamp | Pass |
| Database Backup | Schedule | Cron chạy hằng ngày lúc 02:00 | Pass |
| Database Backup | Retention | Tự động xóa backup cũ hơn 14 ngày trên VPS | Pass |
| Filestore Backup | Backup Method | `tar.gz`, filename có timestamp | Pass |
| Filestore Backup | Schedule | Backup hằng ngày lúc 02:00 | Pass |
| Filestore Backup | Retention | Tự động xóa backup cũ hơn 14 ngày trên VPS | Pass |
| Offsite Backup | Cloudflare R2 | Database và filestore được upload lên R2 | Pass |
| Offsite Backup | Automatic Upload | Upload tự động trong script backup hằng ngày | Pass |
| Test Restore | Restore Environment | Có script và cấu hình tạo môi trường restore riêng | Pass* |
| Retention Policy | VPS | Xóa file backup cũ hơn 14 ngày | Pass |
| Retention Policy | Cloudflare R2 | Xóa backup cũ hơn 14 ngày bằng `rclone delete --min-age 14d` | Pass |

- Quy trình backup và recovery giúp đảm bảo khả năng khôi phục dữ liệu khi xảy ra sự cố như lỗi hệ thống, mất dữ liệu hoặc thao tác nhầm. Backup database kết hợp với filestore đảm bảo tính toàn vẹn dữ liệu Odoo; lưu bản sao trên Cloudflare R2 giúp giảm rủi ro mất dữ liệu khi VPS gặp sự cố. Chính sách retention 14 ngày cân bằng giữa khả năng khôi phục dữ liệu và chi phí lưu trữ. Kiểm thử restore trước go-live giúp xác nhận backup thực sự sử dụng được và đánh giá thời gian khôi phục khi có sự cố.

## 6. Monitoring Checklist
| Mục | Hạng mục | Trạng thái |
|---|---|---|
| 6.1 | **Server Metrics** — CPU >80%, RAM >90%, Disk >85%; `monitor-server.sh`, email alert qua SMTP | **Pass** |
| 6.2 | **Odoo Workers** — Chưa implement | **Pending** |
| 6.3 | **PostgreSQL** — Cảnh báo khi connection >80%, kiểm tra mỗi 5 phút | **Pass** |
| 6.4 | **Response Time** — Theo dõi response time và p95; cảnh báo khi p95 >3 giây; cron mỗi 5 phút | **Pass** |
| 6.5 | **Errors Log** — Theo dõi lỗi Odoo, PostgreSQL và Nginx; cron mỗi 5 phút | **Pass** |
| 6.6 | **Uptime** — UptimeRobot báo trạng thái Up | **Pass** |

- Các hệ thống monitoring giúp phát hiện sớm tình trạng quá tải tài nguyên, lỗi database, phản hồi chậm và gián đoạn dịch vụ. Qua đó, quản trị viên có thể chủ động xử lý sự cố, giảm downtime và duy trì tính ổn định của hệ thống production.