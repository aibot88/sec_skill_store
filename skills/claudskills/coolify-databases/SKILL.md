---
name: coolify-databases
description: >
  This skill should be used when provisioning databases in Coolify, configuring database backups,
  restoring database backups, setting up S3-compatible backup storage, managing database SSL/TLS,
  connecting external clients to Coolify databases, rotating database credentials, running
  migrations against Coolify databases, tuning database resource limits, or choosing between
  standalone databases and service databases. Trigger when: "Coolify database", "create database
  in Coolify", "Coolify PostgreSQL", "Coolify MySQL", "Coolify Redis", "database backup Coolify",
  "restore database Coolify", "S3 backup Coolify", "connect to Coolify database", "database
  migration Coolify", "Coolify MongoDB", "Coolify MariaDB", "Coolify ClickHouse",
  "database credentials", "database SSL Coolify".
---

# Coolify Databases

Covers provisioning, backups, SSL, credential management, and operational patterns for Coolify v4 self-hosted database management.

> **Self-Hosted Only**: All content assumes self-hosted Coolify v4.x. Database management differs on Coolify Cloud.

## Supported Database Engines

Coolify provides one-click provisioning for these databases:

| Engine | Versions Available | Backup Support | Notes |
|--------|-------------------|----------------|-------|
| **PostgreSQL** | 13, 14, 15, 16, 17, **18** | Yes (pg_dump) | Most common choice; full backup/restore. **PG18 + pgvector 18 added in beta.463 (Feb 2026).** |
| **MySQL** | 5.7, 8.0, 8.4 | Yes (mysqldump) | Classic RDBMS |
| **MariaDB** | 10.x, 11.x | Yes (mariadb-dump) | MySQL-compatible alternative |
| **MongoDB** | 5.x, 6.x, 7.x | Yes (mongodump) | Document store |
| **Redis** | 6.x, 7.x | No built-in | In-memory store; use RDB/AOF persistence config |
| **KeyDB** | Latest | No built-in | Redis-compatible, multi-threaded |
| **Dragonfly** | Latest | No built-in | Redis-compatible, high-performance |
| **ClickHouse** | Latest | No built-in | Column-oriented analytics DB |

> **Version note:** Coolify's docs don't always pin exact major versions on the overview page — verify in your running Coolify UI which versions are currently selectable. The overview above reflects what was current as of beta.474 (April 2026). When new major versions ship in upstream images, Coolify typically adds them within a few releases.

## Provisioning Decision Tree

```
START: What database do you need?
│
├─ Relational data with complex queries?
│  ├─ Need MySQL compatibility? → MySQL or MariaDB
│  └─ Default choice / best ecosystem → PostgreSQL
│
├─ Document/JSON data?
│  └─ MongoDB
│
├─ Caching / sessions / queues?
│  ├─ Standard → Redis
│  ├─ Need multi-threading → KeyDB or Dragonfly
│  └─ Need Redis compatibility + lower memory → Dragonfly
│
├─ Analytics / time-series?
│  └─ ClickHouse
│
└─ None of the above?
   └─ Deploy any database as a Docker Compose service or pre-built image
```

## Networking and Access Patterns

### Internal (Private Network) — Default and Recommended

All Coolify resources (apps and databases) on the same server share the `coolify` Docker network. Apps connect to databases using the **internal hostname** (container name):

```
postgresql://user:pass@<DB_CONTAINER_NAME>:5432/mydb
```

- **No port exposure required** — traffic stays on the Docker bridge network
- **SSL not strictly necessary** for same-server internal traffic (traffic does not leave the host)
- **Best for**: All same-server app-to-database connections

### External Access (Expose Port)

To connect external clients (TablePlus, DBeaver, pg_admin):

1. In the database settings, enable **Publicly Accessible** and map the port
2. This exposes the port on the host (e.g., `5432` or a custom port)
3. Connect via `<SERVER_IP>:<PORT>`

**Security warning**: Always use a non-default port, strong credentials, and firewall rules (UFW) to restrict access to trusted IPs only.

### Shared Database Across Multiple Apps

For multiple apps on the **same server** that share one database:

1. Create the database as a standalone resource in the project
2. Each app references it via the internal Docker hostname
3. Set the connection string as an environment variable in each app
4. All containers on the `coolify` network can reach each other by container name

### Dedicated VPS Pattern

Move the database to its own server when:
- Database needs more resources than the app server can spare
- Regulatory requirements mandate data isolation
- Multiple Coolify servers need to share one database
- Database I/O contends with app CPU

## Backups

### S3-Compatible Backup Configuration

1. Navigate to **Settings → S3 Storages → Add**
2. Configure:
   - **Endpoint**: S3-compatible URL (`s3.amazonaws.com`, `nyc3.digitaloceanspaces.com`, Minio URL)
   - **Bucket**: Target bucket name
   - **Region**: Bucket region
   - **Access Key**: IAM access key ID
   - **Secret Key**: IAM secret access key
3. Navigate to the database → **Backups** tab
4. Enable scheduled backups and select the S3 storage
5. Set the cron schedule (e.g., `0 2 * * *` for daily at 2 AM)

### Backup Formats

| Engine | Tool Used | Output Format |
|--------|-----------|---------------|
| PostgreSQL | `pg_dump --format=custom` | `.dmp` (custom binary format) |
| MySQL | `mysqldump` | SQL dump |
| MariaDB | `mariadb-dump` | SQL dump |
| MongoDB | `mongodump --gzip --archive` | Gzipped BSON archive |

### Backup Schedule Options

Coolify uses cron expressions for scheduling:

| Schedule | Cron Expression |
|----------|----------------|
| Every hour | `0 * * * *` |
| Daily at 2 AM | `0 2 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Weekly (Sunday 3 AM) | `0 3 * * 0` |
| Custom | Any valid cron expression |

### Backup Retention

Configure retention by number of backups kept. Older backups are automatically deleted when the limit is reached. Set this in the database backup settings.

### Restore Procedure

**From Coolify UI** (when available):
1. Database → Backups → select the backup → Restore

**Manual restore from S3 backup**:

```bash
# PostgreSQL
# 1. Download the backup from S3
aws s3 cp s3://<BUCKET>/backups/<DB_NAME>/<TIMESTAMP>.sql.gz ./backup.sql.gz

# 2. Decompress
gunzip backup.sql.gz

# 3. Exec into the database container or connect remotely
docker exec -i <POSTGRES_CONTAINER> psql -U <USER> -d <DATABASE> < backup.sql

# MySQL/MariaDB
docker exec -i <MYSQL_CONTAINER> mysql -u <USER> -p<PASSWORD> <DATABASE> < backup.sql

# MongoDB
docker exec -i <MONGO_CONTAINER> mongorestore --archive < backup.archive
```

## SSL/TLS Configuration

### When SSL Is Needed

| Scenario | SSL Required? |
|----------|---------------|
| App → DB on same Coolify server (private network) | No — traffic stays on Docker bridge |
| App → DB on different server | **Yes** — traffic traverses network |
| External client → DB over internet | **Yes** — always encrypt in transit |
| Compliance requirements (PCI, HIPAA) | **Yes** — regardless of network topology |

### PostgreSQL SSL Modes

| Mode | Behavior |
|------|----------|
| `disable` | No SSL |
| `require` | SSL required, no certificate verification |
| `verify-ca` | SSL required, verify server CA |
| `verify-full` | SSL required, verify CA + hostname |

Set via connection string: `postgresql://user:pass@host:5432/db?sslmode=require`

## Operational Patterns

### Running Migrations

Option 1 — **Pre-deployment script** (recommended):
Configure a pre-deployment script in the app settings that runs migrations before the new container receives traffic.

Option 2 — **Exec into app container**:
```bash
docker exec -it <APP_CONTAINER> npx prisma migrate deploy
# or
docker exec -it <APP_CONTAINER> python manage.py migrate
```

Option 3 — **One-off container**:
```bash
docker run --rm --network coolify \
  -e DATABASE_URL="postgresql://user:pass@db-container:5432/mydb" \
  <APP_IMAGE> npx prisma migrate deploy
```

### Connecting External Clients

1. Enable **Publicly Accessible** on the database and set a port mapping
2. Restrict access via UFW: `ufw allow from <YOUR_IP> to any port <DB_PORT>`
3. Connect with your client using `<SERVER_IP>:<PORT>`, database user, and password
4. **Disable public access when done** — do not leave database ports open permanently

### Credential Rotation

1. Create a new database user with the same permissions
2. Update all app environment variables to use the new credentials
3. Redeploy affected applications
4. Verify all apps connect successfully
5. Drop the old user

**Warning**: There is no built-in zero-downtime credential rotation. Plan a brief maintenance window or use connection poolers that support hot credential swaps.

### Resource Limits

Set CPU and memory limits in the database resource settings:
- **Memory limit**: Prevents OOM from affecting other containers. Set to ~80% of available memory for dedicated DB servers.
- **CPU limit**: Set fractional CPUs (e.g., `2.0` for 2 cores)

When a database container hits its memory limit, Docker's OOM killer terminates it. Coolify's restart policy brings it back, but in-flight transactions are lost.

### Auto-Restart on Reboot

Coolify configures database containers with Docker restart policy `unless-stopped`. After a server reboot, Docker automatically restarts all database containers. Coolify's Sentinel agent verifies container health after boot.

## Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Exposing database port to 0.0.0.0 without firewall rules | Database accessible to the entire internet |
| No backup schedule configured | Data loss on disk failure or corruption |
| Storing backups on the same server as the database | Single point of failure; backup lost with the server |
| Using default credentials (postgres/postgres) | Trivially compromised |
| Not setting memory limits on database containers | OOM kills the database AND other containers on the server |
| Running migrations in Dockerfile build phase | Migrations run against wrong database or fail in CI |
| Sharing a small Redis between cache and queue workloads | Cache evictions delete queued jobs |
| Not testing backup restoration | Discover corrupt backups only during an emergency |
| Exposing ports and forgetting to close them | Permanent attack surface |
| Using `sslmode=disable` for cross-server connections | Credentials sent in plaintext |

## Related Skills

- **coolify-deploy** — Pre-deployment scripts for running migrations
- **coolify-security** — Database credential management, network isolation
- **coolify-troubleshoot** — Database OOM diagnosis, connection issues
- **coolify-observability** — Database monitoring and alerting

## Additional Resources

### Reference Files

- **`references/backup-restore.md`** — Detailed backup configuration, restore procedures per engine, point-in-time recovery
- **`references/connection-patterns.md`** — Connection string formats, pooling, SSL configuration per database engine
