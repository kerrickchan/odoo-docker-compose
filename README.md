# Odoo Docker Setup

This repository contains a Docker Compose configuration for running Odoo 18 with PostgreSQL 17 database.

## Services Overview

- **db**: PostgreSQL 17 database server
- **odoo**: Main Odoo application server
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

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Wait for initialization to complete (check logs):
   ```bash
   docker-compose logs -f odoo-init
   ```

5. Access Odoo at: http://localhost:8069

## Directory Structure

```
.
├── docker-compose.yml
├── config/           # Odoo configuration files
├── addons/          # Custom Odoo addons
├── db/
│   └── init/        # Database initialization scripts
└── README.md
```

## Default Credentials

- **Database**: odoo
- **Username**: admin
- **Password**: admin (set during first setup)

## Services Configuration

### PostgreSQL Database
- **Image**: postgres:17
- **Port**: 5432 (exposed)
- **Database**: odoo
- **User**: odoo
- **Password**: odoo
- **Data persistence**: `odoo_db_data` volume

### Odoo Application
- **Image**: odoo:18
- **Port**: 8069 (exposed)
- **Data persistence**: `odoo_web_data` volume
- **Custom addons**: Mount `./addons` directory
- **Configuration**: Mount `./config` directory

### Odoo Initialization
- Runs once to initialize the database with all modules
- Automatically stops after initialization
- Same volumes as main Odoo service

## Common Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f odoo
```

### Restart Odoo
```bash
docker-compose restart odoo
```

### Access database directly
```bash
docker-compose exec db psql -U odoo -d odoo
```

### Reset everything (⚠️ This will delete all data)
```bash
docker-compose down -v
docker-compose up -d
```

## Configuration

### Odoo Configuration
Place your `odoo.conf` file in the `./config` directory. Example:
```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
```

### Custom Addons
Place your custom Odoo addons in the `./addons` directory. They will be automatically available in Odoo.

### Database Initialization
Place any SQL scripts in `./db/init` directory to run them during database initialization.

## Troubleshooting

### Odoo won't start
1. Check if database is healthy:
   ```bash
   docker-compose ps
   ```
2. Check logs for errors:
   ```bash
   docker-compose logs db
   docker-compose logs odoo
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
docker-compose exec db pg_isready -U odoo
```

## Backup and Restore

### Backup database
```bash
docker-compose exec db pg_dump -U odoo odoo > backup.sql
```

### Restore database
```bash
docker-compose exec -T db psql -U odoo odoo < backup.sql
```

### Backup volumes
```bash
docker run --rm -v odoo_odoo_web_data:/data -v $(pwd):/backup alpine tar czf /backup/odoo_data.tar.gz /data
```

## Health Checks

The PostgreSQL service includes a health check that ensures the database is ready before starting Odoo. This prevents connection errors during startup.

## Networks

All services run on the `odoo_network` bridge network, allowing secure internal communication between containers.

## Support

- [Odoo Documentation](https://www.odoo.com/documentation)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
