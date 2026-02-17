# Odoo Docker Setup

This repository contains a Docker Compose configuration for running Odoo 19 with PostgreSQL 18 database.

## Services Overview

- **db**: PostgreSQL 18.2 database server
- **odoo**: Main Odoo 19 application server
- **odoo-init**: Initialization service for setting up Odoo with all modules

## Prerequisites

- Docker
- Docker Compose
- At least 4GB of available RAM
- Ports 8069 and 5432 available on your host machine

## Quick Start

1. Clone or download this configuration
2. Create the required directories:
   ```bash
   mkdir -p config addons db/init
   ```

3. Initialize the database (runs once):
   ```bash
   docker compose up odoo-init
   ```

4. Start the main Odoo service:
   ```bash
   docker compose up -d odoo
   ```

5. Access Odoo at: http://localhost:8069

## Directory Structure

```
.
├── docker-compose.yml
├── config/           # Odoo configuration files
├── addons/           # Custom Odoo addons
│   └── hello_world/  # Example module
├── db/
│   └── init/         # Database initialization scripts (run on first DB creation)
└── README.md
```

## Default Credentials

- **Database**: odoo
- **Username**: admin
- **Password**: admin (set during first setup)

## Services Configuration

### PostgreSQL Database
- **Image**: postgres:18.2
- **Port**: 5432 (exposed)
- **Database**: odoo
- **User**: odoo
- **Password**: odoo
- **Data persistence**: `db_data` volume

### Odoo Application
- **Image**: odoo:19
- **Port**: 8069 (exposed)
- **Custom addons**: Mount `./addons` to `/mnt/addons`
- **Configuration**: Mount `./config` to `/etc/odoo`

### Odoo Initialization
- Runs once to initialize the database with all modules (`-i all --stop-after-init`)
- Does not restart (`restart: no`)
- Same volumes as the main Odoo service

## Enterprise Addons (Optional)

To use Odoo Enterprise source code, uncomment the enterprise volume lines in both the `odoo` and `odoo-init` services in `docker-compose.yml`:

```yaml
- ../enterprise-19.0:/mnt/enterprise:ro
```

## Custom Addons

### Hello World Module

An example `hello_world` module is included in `addons/` demonstrating a basic Odoo module with:

- A model (`hello.world`) with `name`, `message`, and `is_published` fields
- List and form views
- A top-level menu item
- Access control for internal users

### Adding Your Own Modules

Place custom Odoo addons in the `./addons` directory. They are automatically available via the `/mnt/addons` addons path.

## Common Commands

### Start services
```bash
docker compose up -d
```

### Stop services
```bash
docker compose down
```

### View logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f odoo
```

### Restart Odoo
```bash
docker compose restart odoo
```

### Access database directly
```bash
docker compose exec db psql -U odoo -d odoo
```

### Reset everything (⚠️ This will delete all data)
```bash
docker compose down -v
docker compose up -d
```

## Configuration

### Odoo Configuration
Place your `odoo.conf` file in the `./config` directory. Example:
```ini
[options]
addons_path = /mnt/addons,/mnt/enterprise,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
```

### Database Initialization Scripts
Place SQL scripts in `./db/init` — they run automatically on first database creation via PostgreSQL's `docker-entrypoint-initdb.d` mechanism.

## Troubleshooting

### Odoo won't start
1. Check if database is healthy:
   ```bash
   docker compose ps
   ```
2. Check logs for errors:
   ```bash
   docker compose logs db
   docker compose logs odoo
   ```

### Port conflicts
If ports 8069 or 5432 are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8070:8069"  # Change host port
```

### Permission issues
Ensure the volumes have correct permissions:
```bash
sudo chown -R 101:101 config addons
```

### Database connection issues
Verify database service is running and healthy:
```bash
docker compose exec db pg_isready -U odoo
```

## Backup and Restore

### Backup database
```bash
docker compose exec db pg_dump -U odoo odoo > backup.sql
```

### Restore database
```bash
docker compose exec -T db psql -U odoo odoo < backup.sql
```

## Support

- [Odoo Documentation](https://www.odoo.com/documentation)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
