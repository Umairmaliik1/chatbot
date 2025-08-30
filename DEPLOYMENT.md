# 🚀 Deployment Guide

## Overview
This guide covers deploying the chatbot application using Docker containers with nginx reverse proxy on a VPS.

## Architecture
```
Internet → Nginx (Port 80/443) → Docker Container (Port 8000) → FastAPI + Vue.js
```

## Prerequisites

### Local Machine
- Docker installed
- Node.js and npm installed
- Docker Hub account

### Fresh VPS Server
- Ubuntu 20.04 LTS or newer (recommended)
- At least 1GB RAM, 1 vCPU, 20GB storage
- SSH access (root or sudo user)
- Public IP address
- Optional: Domain name pointed to VPS IP

## 📦 Local Build & Push

### 1. Update Configuration
Edit the following files with your actual values:
- `deploy.sh`: Update `DOCKER_USERNAME`
- `docker-compose.prod.yml`: Update image name
- `nginx.conf`: Update `server_name` with your domain

### 2. Build and Push
```bash
# Make deploy script executable
chmod +x deploy.sh

# Build and push (replace with your tag)
./deploy.sh v1.0.0

# Or with default 'latest' tag
./deploy.sh
```

## 🖥️ Fresh VPS Setup (First Time)

### 1. Initial Server Setup
```bash
# Connect to your VPS via SSH
ssh root@your-vps-ip

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git ufw htop nano

# Create a new user (replace 'username' with your preferred username)
sudo adduser username
sudo usermod -aG sudo username

# Setup SSH key authentication (recommended)
# Copy your public key to: ~/.ssh/authorized_keys
# Then disable password authentication in /etc/ssh/sshd_config
# sudo systemctl restart sshd

# Switch to your new user
su - username
```

### 2. Install Docker & Dependencies
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply docker group membership
exit
ssh username@your-vps-ip

# Verify Docker installation
docker --version
docker-compose --version
```

### 3. Install & Configure Nginx
```bash
# Install Nginx
sudo apt install nginx -y

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### 4. Setup Basic Security (Firewall)
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 5. Configure Domain (Optional but Recommended)
If you have a domain name, point it to your VPS IP:
- Create an A record: `your-domain.com` → `your-vps-ip`
- Create a CNAME record: `www.your-domain.com` → `your-domain.com`

If no domain, you can access via IP address directly.

### 6. Setup Application Directory
```bash
# Create application directory
mkdir -p ~/chatbot-app
cd ~/chatbot-app

# Create required directories
mkdir -p data logs
```

### 7. Copy Configuration Files
Upload these files to your VPS `~/chatbot-app/` directory:
- `docker-compose.prod.yml`
- `nginx.conf`

You can use SCP or SFTP:
```bash
# From your local machine (in project directory)
scp docker-compose.prod.yml username@your-vps-ip:~/chatbot-app/
scp nginx.conf username@your-vps-ip:~/chatbot-app/

# Or use a tool like FileZilla, WinSCP, or VS Code SFTP extension
```

### 8. Configure Nginx
```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/chatbot

# Enable the site
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 9. Test Initial Setup
```bash
# Test nginx is working
curl http://your-vps-ip

# You should see the nginx welcome page
# If using domain:
curl http://your-domain.com
```

## 🚀 Deployment Process

### 1. Pull and Run Container
```bash
cd ~/chatbot-app

# Pull latest image
docker pull your-dockerhub-username/chatbot-app:latest

# Start the application
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

### 2. Verify Deployment
```bash
# Check if container is running
docker ps

# Test application health
curl http://localhost:8000/api/health

# Test through nginx
curl http://your-domain.com/api/health
```

## 🔄 Update Process

### From Local Machine
```bash
# Build and push new version
./deploy.sh v1.1.0
```

### On VPS
```bash
cd ~/chatbot-app

# Pull new image
docker pull your-dockerhub-username/chatbot-app:v1.1.0

# Update docker-compose.prod.yml with new tag
# Then restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## 🔒 SSL Certificate Setup (Recommended)

### Option 1: Let's Encrypt (Free SSL - Recommended)

#### Prerequisites
- Domain name pointing to your VPS IP address
- Nginx configured and running
- Ports 80 and 443 open in firewall

#### Step 1: Install Certbot
```bash
# Update package list
sudo apt update

# Install certbot and nginx plugin
sudo apt install certbot python3-certbot-nginx -y

# Verify installation
certbot --version
```

#### Step 2: Obtain SSL Certificate
```bash
# Replace 'your-domain.com' with your actual domain
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow the prompts:
# 1. Enter email address for notifications
# 2. Agree to terms of service (type 'A')
# 3. Choose whether to share email with EFF (type 'Y' or 'N')
# 4. Choose redirect option (type '2' to redirect HTTP to HTTPS)
```

#### Step 3: Verify SSL Setup
```bash
# Test your SSL certificate
sudo certbot certificates

# Check SSL grade online
curl -I https://your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### Step 4: Configure Auto-Renewal
```bash
# Check if systemd timer is enabled (should be automatic)
sudo systemctl status certbot.timer

# If not enabled, enable it
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Alternative: Add cron job (if systemd timer not available)
sudo crontab -e
# Add this line: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Custom SSL Certificate (Paid SSL)

#### If you have a purchased SSL certificate:

#### Step 1: Upload Certificate Files
```bash
# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Upload your certificate files to the server
# - certificate.crt (or .pem)
# - private.key
# - intermediate.crt (if provided)

# Set proper permissions
sudo chmod 600 /etc/nginx/ssl/private.key
sudo chmod 644 /etc/nginx/ssl/certificate.crt
sudo chown root:root /etc/nginx/ssl/*
```

#### Step 2: Configure Nginx for Custom SSL
```bash
# Edit nginx configuration
sudo nano /etc/nginx/sites-available/chatbot

# Update the HTTPS server block with your certificate paths
```

Add this HTTPS server block to your nginx config:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Certificate Configuration
    ssl_certificate /etc/nginx/ssl/certificate.crt;
    ssl_certificate_key /etc/nginx/ssl/private.key;
    
    # If you have intermediate certificate
    # ssl_trusted_certificate /etc/nginx/ssl/intermediate.crt;

    # Modern SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    # HSTS (optional, uncomment after testing)
    # add_header Strict-Transport-Security "max-age=63072000" always;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Copy all location blocks from HTTP server block here
    # [Include all your existing location configurations]
}

# HTTP server block (redirect to HTTPS)
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### Option 3: Cloudflare SSL (Proxy + SSL)

#### If using Cloudflare as a proxy:

#### Step 1: Configure Cloudflare
1. Add your domain to Cloudflare
2. Update nameservers to Cloudflare's
3. Enable "Flexible" or "Full" SSL mode
4. Enable "Always Use HTTPS"

#### Step 2: Configure Nginx for Cloudflare
```bash
# Update nginx config to trust Cloudflare IPs
sudo nano /etc/nginx/sites-available/chatbot
```

Add Cloudflare real IP configuration:
```nginx
# Cloudflare real IP configuration
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
set_real_ip_from 103.31.4.0/22;
set_real_ip_from 104.16.0.0/13;
set_real_ip_from 104.24.0.0/14;
set_real_ip_from 108.162.192.0/18;
set_real_ip_from 131.0.72.0/22;
set_real_ip_from 141.101.64.0/18;
set_real_ip_from 162.158.0.0/15;
set_real_ip_from 172.64.0.0/13;
set_real_ip_from 173.245.48.0/20;
set_real_ip_from 188.114.96.0/20;
set_real_ip_from 190.93.240.0/20;
set_real_ip_from 197.234.240.0/22;
set_real_ip_from 198.41.128.0/17;
real_ip_header CF-Connecting-IP;
```

### Common SSL Issues & Troubleshooting

#### Issue 1: Certificate Not Valid
```bash
# Check certificate details
openssl x509 -in /etc/nginx/ssl/certificate.crt -text -noout

# Check if certificate matches private key
openssl rsa -in /etc/nginx/ssl/private.key -check
openssl x509 -in /etc/nginx/ssl/certificate.crt -noout -modulus
openssl rsa -in /etc/nginx/ssl/private.key -noout -modulus
```

#### Issue 2: Mixed Content Warnings
```bash
# Ensure all resources use HTTPS
# Check browser console for mixed content errors
# Update any hardcoded HTTP URLs in your application
```

#### Issue 3: Certificate Renewal Failed
```bash
# Check certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Manual renewal
sudo certbot renew --force-renewal

# Check nginx config before renewal
sudo nginx -t
```

#### Issue 4: Port 443 Not Accessible
```bash
# Check if port 443 is open
sudo netstat -tlnp | grep :443

# Open port in firewall
sudo ufw allow 443

# Check if nginx is listening on 443
sudo ss -tlnp | grep :443
```

### SSL Security Best Practices

#### 1. Use Strong SSL Configuration
```bash
# Test your SSL configuration
curl -I https://your-domain.com

# Online SSL test
# Visit: https://www.ssllabs.com/ssltest/
```

#### 2. Enable HSTS (HTTP Strict Transport Security)
```nginx
# Add to your HTTPS server block
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

#### 3. Regular Certificate Monitoring
```bash
# Check certificate expiration
echo | openssl s_client -servername your-domain.com -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -dates

# Create monitoring script
cat > ~/ssl-monitor.sh << 'EOF'
#!/bin/bash
DOMAIN="your-domain.com"
THRESHOLD=30

EXPIRY=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_DATE=$(date -d "$EXPIRY" +%s)
CURRENT_DATE=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_DATE - $CURRENT_DATE) / 86400 ))

if [ $DAYS_LEFT -lt $THRESHOLD ]; then
    echo "SSL certificate for $DOMAIN expires in $DAYS_LEFT days!"
    # Add notification logic here (email, webhook, etc.)
fi
EOF

chmod +x ~/ssl-monitor.sh

# Add to crontab to run daily
echo "0 9 * * * ~/ssl-monitor.sh" | crontab -
```

### Final Verification

#### Complete SSL Setup Checklist:
- [ ] Domain points to VPS IP
- [ ] Nginx configured and running
- [ ] SSL certificate obtained and installed
- [ ] HTTPS server block configured
- [ ] HTTP to HTTPS redirect working
- [ ] SSL test shows A+ grade
- [ ] Auto-renewal configured
- [ ] Security headers enabled
- [ ] Monitoring setup

#### Test Commands:
```bash
# Test HTTPS access
curl -I https://your-domain.com

# Test HTTP redirect
curl -I http://your-domain.com

# Test application through HTTPS
curl https://your-domain.com/api/health

# Check SSL certificate
echo | openssl s_client -servername your-domain.com -connect your-domain.com:443 -brief
```

## 📊 Monitoring

### View Logs
```bash
# Application logs
docker-compose -f docker-compose.prod.yml logs -f

# Nginx logs
sudo tail -f /var/log/nginx/chatbot_access.log
sudo tail -f /var/log/nginx/chatbot_error.log
```

### Health Checks
```bash
# Container health
docker ps
docker-compose -f docker-compose.prod.yml ps

# Application health
curl http://localhost:8000/api/health
```

## 🛠️ Troubleshooting

### Container Issues
```bash
# Check container logs
docker-compose -f docker-compose.prod.yml logs app

# Restart container
docker-compose -f docker-compose.prod.yml restart app

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker pull your-dockerhub-username/chatbot-app:latest
docker-compose -f docker-compose.prod.yml up -d
```

### Nginx Issues
```bash
# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Check nginx status
sudo systemctl status nginx
```

### Database Issues
```bash
# Backup database
cp ~/chatbot-app/data/app.db ~/chatbot-app/data/app.db.backup

# Check database permissions
ls -la ~/chatbot-app/data/
```

## 📋 Maintenance

### Regular Tasks
- Monitor disk space: `df -h`
- Monitor memory usage: `free -h`
- Update system: `sudo apt update && sudo apt upgrade`
- Clean Docker: `docker system prune -f`

### Backup Strategy
```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf ~/backups/chatbot_backup_$DATE.tar.gz ~/chatbot-app/data ~/chatbot-app/logs
find ~/backups -name "chatbot_backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x ~/backup.sh

# Add to crontab for daily backups
echo "0 2 * * * ~/backup.sh" | crontab -
```

## 🆘 Emergency Recovery
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down
sudo systemctl stop nginx

# Start from clean state
docker system prune -a -f
docker pull your-dockerhub-username/chatbot-app:latest
docker-compose -f docker-compose.prod.yml up -d
sudo systemctl start nginx
```

## 📞 Hostinger VPS Specific Notes

### Accessing Your VPS
- Use the IP address provided in your Hostinger panel
- Default SSH port is usually 22
- Login credentials are in your Hostinger account

### Common Hostinger Commands
```bash
# Check your VPS resources
htop
df -h
free -h

# View system information
lsb_release -a
uname -a
```

### If You Get Permission Errors
```bash
# Make sure you're in the right directory
cd ~/chatbot-app

# Check file permissions
ls -la

# Fix permissions if needed
sudo chown -R $USER:$USER ~/chatbot-app
```

## 🎯 Quick Start Checklist for Fresh VPS

- [ ] Connect to VPS via SSH
- [ ] Create new user account
- [ ] Install Docker & Docker Compose
- [ ] Install & configure Nginx
- [ ] Setup firewall (UFW)
- [ ] Create application directory
- [ ] Upload configuration files
- [ ] Configure Nginx site
- [ ] Test basic setup
- [ ] Build & push Docker image locally
- [ ] Pull & run container on VPS
- [ ] Verify deployment works
- [ ] Setup SSL certificate (optional)

**Total setup time: ~30-45 minutes for first-time setup**
