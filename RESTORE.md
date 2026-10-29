
# Restore Backup từ Cloudclare R2
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