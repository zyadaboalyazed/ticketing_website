# Deployment Guide

## Table of Contents
- [Quick Start with Docker](#quick-start-with-docker)
- [Manual Deployment](#manual-deployment)
- [Production Configuration](#production-configuration)
- [Troubleshooting](#troubleshooting)

## Quick Start with Docker

The easiest way to deploy the ticketing system is using Docker Compose.

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zyadaboalyazed/ticketing_website.git
   cd ticketing_website
   ```

2. **Configure environment variables**:
   ```bash
   # Backend configuration
   cp backend/.env.example backend/.env
   # Edit backend/.env with your settings
   
   # Frontend configuration
   cp frontend/.env.example frontend/.env
   # Edit if needed (default should work for local development)
   ```

3. **Generate a secure secret key** for the backend:
   ```bash
   # On Linux/Mac:
   export SECRET_KEY=$(openssl rand -hex 32)
   echo "SECRET_KEY=$SECRET_KEY" >> backend/.env
   
   # Or manually add to backend/.env:
   # SECRET_KEY=your-very-secure-random-secret-key-here
   ```

4. **Start all services**:
   ```bash
   docker-compose up -d
   ```

5. **Wait for services to be healthy** (about 30 seconds):
   ```bash
   docker-compose ps
   ```

6. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

7. **Create your first admin user**:
   You can register through the UI at http://localhost/register and select "Admin" role.

### Managing the Deployment

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose stop

# Start services
docker-compose start

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

## Manual Deployment

For production environments, you may want to deploy services separately.

### Backend Deployment

1. **Install dependencies**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

3. **Set up PostgreSQL database**:
   ```sql
   CREATE DATABASE ticketing_db;
   CREATE USER ticketing_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ticketing_db TO ticketing_user;
   ```

4. **Update DATABASE_URL in .env**:
   ```
   DATABASE_URL=postgresql://ticketing_user:your_password@localhost:5432/ticketing_db
   ```

5. **Run the backend**:
   ```bash
   # Development
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # Production (with Gunicorn)
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
   ```

### Frontend Deployment

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit VITE_API_URL to point to your backend
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Serve the built files**:
   - **Using Nginx** (recommended):
     ```nginx
     server {
         listen 80;
         server_name your-domain.com;
         root /path/to/frontend/dist;
         index index.html;

         location / {
             try_files $uri $uri/ /index.html;
         }

         location /api {
             proxy_pass http://localhost:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```
   
   - **Using serve**:
     ```bash
     npm install -g serve
     serve -s dist -l 3000
     ```

## Production Configuration

### Backend Production Settings

Edit `backend/.env`:

```env
# Database - Use strong password
DATABASE_URL=postgresql://user:strong_password@db_host:5432/ticketing_db

# Security - Generate with: openssl rand -hex 32
SECRET_KEY=your-very-long-random-secret-key-minimum-32-characters

# JWT Token expiration (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email configuration - Use real SMTP server
SMTP_HOST=smtp.your-domain.com
SMTP_PORT=587
SMTP_USER=noreply@your-domain.com
SMTP_PASSWORD=your-email-password
EMAIL_FROM=noreply@your-domain.com

# Redis - For caching and background tasks
REDIS_URL=redis://redis-host:6379/0

# CORS - Add your frontend domains
BACKEND_CORS_ORIGINS=["https://your-domain.com","https://www.your-domain.com"]

# Application
PROJECT_NAME=Your Ticketing System
```

### Frontend Production Settings

Edit `frontend/.env`:

```env
VITE_API_URL=https://api.your-domain.com
```

### Security Considerations

1. **Use HTTPS**: Always use HTTPS in production
2. **Strong Passwords**: Use strong, unique passwords for database and admin accounts
3. **Secret Key**: Generate a strong, random SECRET_KEY
4. **CORS**: Limit CORS origins to your actual domains
5. **Database Backups**: Set up regular database backups
6. **Rate Limiting**: Consider adding rate limiting (e.g., with Nginx)
7. **Firewall**: Configure firewall to only allow necessary ports

### Database Migrations

For production, you should use database migrations:

```bash
cd backend

# Initialize Alembic (if not already done)
alembic init migrations

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Setting up Systemd Services (Linux)

Create `/etc/systemd/system/ticketing-backend.service`:

```ini
[Unit]
Description=Ticketing System Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/ticketing_website/backend
Environment="PATH=/path/to/ticketing_website/backend/venv/bin"
ExecStart=/path/to/ticketing_website/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ticketing-backend
sudo systemctl start ticketing-backend
sudo systemctl status ticketing-backend
```

## Monitoring and Logging

### Backend Logs

Logs are printed to stdout. In production, redirect to a file:

```bash
gunicorn ... >> /var/log/ticketing/backend.log 2>&1
```

### Database Monitoring

Monitor PostgreSQL performance:
```bash
# Check connections
psql -U ticketing_user -d ticketing_db -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
psql -U ticketing_user -d ticketing_db -c "SELECT pg_size_pretty(pg_database_size('ticketing_db'));"
```

### Health Checks

The backend provides health check endpoints:
- `/health` - Basic health check
- `/` - API information

Set up monitoring tools (e.g., Prometheus, Grafana) to track these endpoints.

## Troubleshooting

### Backend won't start

1. **Check database connection**:
   ```bash
   psql -U ticketing_user -d ticketing_db -h localhost
   ```

2. **Verify environment variables**:
   ```bash
   cd backend
   cat .env
   ```

3. **Check logs**:
   ```bash
   docker-compose logs backend  # If using Docker
   # Or check systemd logs if using systemd
   sudo journalctl -u ticketing-backend -f
   ```

### Frontend can't connect to backend

1. **Check CORS settings** in backend `.env`
2. **Verify API URL** in frontend `.env`
3. **Check network/firewall rules**

### Database connection errors

1. **Verify PostgreSQL is running**:
   ```bash
   sudo systemctl status postgresql
   ```

2. **Check database exists**:
   ```bash
   psql -U postgres -c "\l"
   ```

3. **Test connection**:
   ```bash
   psql -U ticketing_user -d ticketing_db -h localhost
   ```

### Email notifications not working

1. **Verify SMTP settings** in backend `.env`
2. **Test SMTP connection**:
   ```bash
   telnet your-smtp-host 587
   ```
3. **Check firewall rules** for outbound SMTP (port 587)
4. **Enable "less secure apps"** if using Gmail (or use App Passwords)

### Performance issues

1. **Check database indexes**
2. **Monitor database query performance**
3. **Increase backend workers** (gunicorn -w parameter)
4. **Add caching** with Redis
5. **Use a CDN** for frontend static assets

## Backup and Restore

### Database Backup

```bash
# Backup
pg_dump -U ticketing_user ticketing_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U ticketing_user ticketing_db < backup_20240101.sql
```

### Automated Backups

Set up a cron job:
```bash
# Add to crontab
0 2 * * * pg_dump -U ticketing_user ticketing_db > /backups/ticketing_$(date +\%Y\%m\%d).sql
```

## Scaling

### Horizontal Scaling

1. **Backend**: Run multiple backend instances behind a load balancer
2. **Database**: Use PostgreSQL replication for read replicas
3. **Redis**: Use Redis Cluster for distributed caching
4. **Frontend**: Serve from CDN

### Vertical Scaling

1. **Increase server resources** (CPU, RAM)
2. **Optimize database** (indexes, query optimization)
3. **Use connection pooling** for database connections

## Support

For production deployment issues:
- Check the [main README](README.md)
- Review [GitHub Issues](https://github.com/zyadaboalyazed/ticketing_website/issues)
- Contact: support@your-domain.com
