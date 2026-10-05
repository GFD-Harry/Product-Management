# Production Checklist
## 0. Information
## 1. Pre-Flight Checklist
### 1.1. Server Sizing
- VPS:
  - CPU: 2 vCPU
  - RAM: 4GB
  - Disk: 30GB SSD

- Workload:
  - Users: ~10
  - Concurrent users: ~3-4

- Resource allocation:
  - Odoo workers: 3
  - RAM allocation for Odoo: ~1.5GB

- Odoo configuration:
  - workers = 3
  - max_cron_threads = 1
  - limit_memory_soft = 536870912
  - limit_memory_hard = 805306368

### 1.2. Cloud Provider
- VPS

### 1.3. Odoo Version
- 19.0.0
### 1.4. Module Inventory
- Custom Modules:
    - Product Management
    - Version: 19.0.1.0.0
    - Author: Product Management PV
    - Depends:
        - base
    - Purpose:
        - Manage internal product information
        - Customer consultation support

## 2. Server Setup Checklist
### 2.1. OS
**Host**
- OS: Ubuntu 24.04 LTS
- Docker Engine: 29.1.3
- Docker Compose: v2.40.3
**Deployment**
- Runtime: Docker Compose

### 2.2. PostgreSQL
- postgresql 15

### 2.3. Python
- Managed by odoo docker image

### 2.4. wkhtmltoppdf
- Managed by Odoo Docker image

### 2.5. Odoo System User
- Skip because of using Docker Compose to Deploy

### 2.6. Firewall
- Firewall: UFW
- Status: Active
- Default incoming: Deny
- Allowed: 
  - 22/tcp --> SSH
  - 80/tcp --> HTTP
  - 443/tcp --> HTTPS
- Odoo 8069/8070: Not publicly exposed
- PostgreSQL 5432: Not publicly exposed

### 2.7. Fail2ban
- Installed & enabled
- SSH jail configured
- SSH brute-force protection active

### 3. Odoo Configuration Checklist

## 3.1. Master Password
- admin_passwd changed from default
- Strong and unique password
- Master password for Odoo Database Manager
- Not the same as Odoo user password

### 3.2. Database Manager
- list_db = False
- Database Manager not exposed on production
- Prevent database listing/creation/deletion through the web UI
### 3.3. Workers
- CPU: 2 vCPU
- workers = 3
- max_cron_threads = 1
- Reference formula: (CPU_cores × 2) + 1
### 3.4. Memory Limits
- limit_memory_soft = 536870912 (512 MB)
- limit_memory_hard = 805306368 (768 MB)
- Soft limit: Worker is recycled after completing the current request
- Hard limit: Worker is terminated when the limit is exceeded
### 3.5. Reverse Proxy
- proxy_mode = True
- Nginx configured as reverse proxy
- X-Forwarded-For configured
- X-Forwarded-Proto configured
- HTTP → HTTPS redirect configured
### 3.6. Longpolling / WebSocket
- Not required
- Live Chat / Discuss / real-time notification: Not used
- No additional longpolling port exposed

## 4. Security Checklist
### 4.1. HTTPS/SSL
- Let's Encrypt + Certbot - SSL certificate cho pv.harryon.io.vn đã được cấp và hoạt động
- HTTPS bắt buộc - Nginx cấu hình HTTPS và HTTP (HTTPS redirect)
- Auto-renewal - certbot.timer active, tự động chạy 2 lần/ngày
- Reviewal test - certbot renew --dry-run thành công cho toàn bộ certificate.
### 4.2. Nginx Security Header
- [x] X-Content-Type-Options
- [x] X-Frame-Options
- [x] Strict-Transport-Security (HSTS)
- [ ] Content-Security-Policy (CSP) — deferred due to Odoo compatibility
### 4.3. PostgreSQL Access
- Không expose port 5432 ra Internet
- Odoo --> PostgreSQL qua Docker Internal Network
### 4.4. SSH Authentication
- Tạm thời chưa implement
### 4.5. Automatic Security Update
- `unattended-upgrades` được cài đặt và hoạt động
- Ubuntu host tự động nhận security patches
### 4.6. Odoo Admin Account
- Thay đổi default usern và pw của admin odoo

## 5. Backup Checklist
### 5.1. Database Backup
- pg_dump -Fc + filename timestamp
- Backup hằng ngày + retention 14 ngày
### 5.2. Filestore Backup
- Backup filestore + filename timestamp
- Backup hằng ngày + retention 14 ngày
### 5.3. Offsite Backup
- DB Backup Cloudflare R2
- Filestore Backup Cloudclare R2
- Tự động upload mỗi ngày

### 5.4. Test Restore
- Test restore trước go-live
- Restore trên môi trường riêng
- Đo thừoi gian restore
### 5.5. Retention Policy
- Tự động xóa các backup dài hơn 14 ngày ở VPS và Cloudclare R2

## 6. Monitoring Checklist
### 6.1. Server Metrics
- CPU alert threshold: >80%
- RAM alert threshold: >90%
- Disk alert threshold: >85%
- Monitoring script: `monitor-server.sh`
- Email alert via SMTP

### 6.2. Odoo workers
- chưa implement
### 6.3. PostgreSQL
- Alert khi connection >80%, quét mỗi 5p
### 6.4. Response Time
### Response Time
- Theo dõi response time
- Theo dõi p95
- Alert khi p95 > 3s
- Cron chạy mỗi 5 phút
### 6.5. Errors Log
### 6.6. Uptime