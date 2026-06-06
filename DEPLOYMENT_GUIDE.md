# AutoStream AI Agent - Deployment Guide

## 📋 Prerequisites

- Docker & Docker Compose installed
- GitHub account with repository access
- Gemini API key
- Twilio account (for WhatsApp)
- Server/VPS for deployment

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone repository
git clone https://github.com/Sngithub12/autostream-ai-agent.git
cd autostream-ai-agent

# Create .env file
cp .env.example .env

# Edit .env with your credentials
vim .env

# Start with Docker Compose
docker-compose up

# Access API at http://localhost:8000
```

### 2. GitHub Actions Setup (CI/CD)

**Step 1: Add GitHub Secrets**

Go to: `Settings → Secrets and variables → Actions`

Add these secrets:
```
DOCKER_USERNAME=your_docker_hub_username
DOCKER_PASSWORD=your_docker_hub_password
DEPLOY_HOST=your_server_ip_or_domain
DEPLOY_USER=deploy_user
DEPLOY_KEY=your_ssh_private_key
```

**Step 2: Push to main branch**

```bash
git add .
git commit -m "Deploy real-time features"
git push origin main
```

Workflow triggers automatically!

### 3. Production Server Setup

**On your server:**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone https://github.com/Sngithub12/autostream-ai-agent.git
cd autostream-ai-agent

# Create .env
cp .env.example .env
vim .env  # Add production credentials

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat Message
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "Hi", "channel": "web"}'
```

### Capture Lead
```bash
curl -X POST http://localhost:8000/lead/capture \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com", "platform": "YouTube", "phone": "1234567890"}'
```

### Get Analytics
```bash
curl http://localhost:8000/analytics/summary
```

### Get Conversation History
```bash
curl http://localhost:8000/user/user123/history
```

## 🔧 Troubleshooting

### Docker container won't start
```bash
# Check logs
docker-compose logs app

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Database connection issues
```bash
# Check PostgreSQL
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up
```

### Port already in use
```bash
# Change port in docker-compose.yml
# Or kill existing process:
lsof -i :8000
kill -9 <PID>
```

## 📊 Monitoring

### View real-time logs
```bash
docker-compose logs -f app
```

### Check container status
```bash
docker-compose ps
```

### Access database
```bash
docker-compose exec db psql -U postgres -d autostream
```

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit `.env` file
2. **SSH Keys**: Keep deploy keys secure
3. **Database**: Use strong passwords
4. **SSL/TLS**: Set up reverse proxy with Nginx
5. **API Keys**: Rotate Gemini/Twilio keys regularly

## 🚀 Advanced Deployment

### Using Nginx reverse proxy

Create `nginx.conf`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL with Let's Encrypt
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com
```

## 📞 Support

For issues:
1. Check logs: `docker-compose logs app`
2. Open GitHub issue
3. Contact support@autostream.com
