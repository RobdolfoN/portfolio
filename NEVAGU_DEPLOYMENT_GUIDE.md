# Deploying Nevagu.com to Your EC2 Instance

This guide will help you add **nevagu.com** to your existing EC2 instance that's already running **rodolfonevarezg.com**.

## Overview

Your Django application is already configured for multi-domain hosting:
- **rodolfonevarezg.com** → Your portfolio (portfolioapp)
- **nevagu.com** → Medical equipment e-commerce site (nevagu app)

Both sites will run on the same EC2 instance (18.236.154.235) and share the same database.

---

## Step 1: Domain Registration & DNS Configuration

### 1.1 Register nevagu.com
If you haven't already, register the domain **nevagu.com** with your preferred domain registrar (GoDaddy, Namecheap, Google Domains, etc.).

### 1.2 Configure DNS Records
In your domain registrar's DNS settings, create these A records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 18.236.154.235 | 3600 |
| A | www | 18.236.154.235 | 3600 |

**What this does:** Points both `nevagu.com` and `www.nevagu.com` to your EC2 instance's IP address.

**Note:** DNS propagation can take 5 minutes to 48 hours (usually within 1-2 hours).

---

## Step 2: Update Your EC2 Instance

### 2.1 SSH into Your EC2 Instance

```bash
ssh -i your-key.pem ubuntu@18.236.154.235
```

### 2.2 Navigate to Your Project Directory

```bash
cd /path/to/your/portfolioapp
# Example: cd /home/ubuntu/portfolio/portfolioapp
```

### 2.3 Pull Latest Code

```bash
git pull origin main
# Or however you deploy your code
```

### 2.4 Activate Virtual Environment

```bash
source /path/to/venv/bin/activate
# Example: source ../venv/bin/activate
```

### 2.5 Install Dependencies (if any new ones)

```bash
pip install -r requirements.txt
```

### 2.6 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2.7 Run Migrations

```bash
python manage.py migrate
```

---

## Step 3: Update Web Server Configuration

### Option A: If Using Nginx + Gunicorn (Recommended)

#### 3.1 Update Nginx Configuration

Edit your Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/portfolio
```

Update the `server_name` line to include nevagu.com:

```nginx
server {
    listen 80;
    server_name rodolfonevarezg.com www.rodolfonevarezg.com nevagu.com www.nevagu.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/portfolioapp/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/portfolioapp/portfolioapp/images/;
    }
}
```

#### 3.2 Test Nginx Configuration

```bash
sudo nginx -t
```

#### 3.3 Restart Nginx

```bash
sudo systemctl restart nginx
```

#### 3.4 Restart Gunicorn

```bash
sudo systemctl restart gunicorn
```

---

### Option B: If Using Apache + mod_wsgi

#### 3.1 Update Apache Virtual Host

Edit your Apache configuration:

```bash
sudo nano /etc/apache2/sites-available/portfolio.conf
```

Update the `ServerAlias` line:

```apache
<VirtualHost *:80>
    ServerName rodolfonevarezg.com
    ServerAlias www.rodolfonevarezg.com
    ServerAlias nevagu.com
    ServerAlias www.nevagu.com
    
    WSGIDaemonProcess aiagentbase python-path=/path/to/portfolioapp python-home=/path/to/venv
    WSGIProcessGroup aiagentbase
    WSGIScriptAlias / /path/to/portfolioapp/aiagentbase/wsgi.py
    
    <Directory /path/to/portfolioapp/aiagentbase>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    Alias /static /path/to/portfolioapp/staticfiles
    <Directory /path/to/portfolioapp/staticfiles>
        Require all granted
    </Directory>
    
    Alias /media /path/to/portfolioapp/portfolioapp/images
    <Directory /path/to/portfolioapp/portfolioapp/images>
        Require all granted
    </Directory>
</VirtualHost>
```

#### 3.2 Restart Apache

```bash
sudo systemctl restart apache2
```

---

## Step 4: SSL Certificate Setup (HTTPS)

### 4.1 Install Certbot (if not already installed)

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt-get install certbot python3-certbot-apache  # For Apache
```

### 4.2 Get SSL Certificate for Both Domains

**For Nginx:**
```bash
sudo certbot --nginx -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d nevagu.com -d www.nevagu.com
```

**For Apache:**
```bash
sudo certbot --apache -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d nevagu.com -d www.nevagu.com
```

Follow the prompts. Certbot will automatically configure HTTPS redirects.

### 4.3 Update Django Settings for Production

Edit `settings.py` on your EC2 instance:

```python
# In production, set these to True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 4.4 Restart Services

```bash
sudo systemctl restart nginx  # or apache2
sudo systemctl restart gunicorn  # if using gunicorn
```

---

## Step 5: Verify Deployment

### 5.1 Test Both Domains

Open your browser and visit:

1. **https://rodolfonevarezg.com** → Should show your portfolio
2. **https://nevagu.com** → Should show the Nevagu medical equipment site

### 5.2 Check Cart Functionality

On nevagu.com:
1. Go to Products page
2. Click "Add to Cart" on a product
3. Check cart icon updates
4. Visit cart page
5. Fill out quote request form
6. Submit and verify success message

### 5.3 Test on Mobile

Test both sites on mobile devices to ensure responsive design works correctly.

---

## Step 6: Monitoring & Maintenance

### 6.1 Check Logs

**Nginx logs:**
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

**Apache logs:**
```bash
sudo tail -f /var/log/apache2/error.log
sudo tail -f /var/log/apache2/access.log
```

**Gunicorn logs:**
```bash
sudo journalctl -u gunicorn -f
```

### 6.2 Set Up Auto-Renewal for SSL

Certbot automatically sets up a cron job, but verify it:

```bash
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Issue: "Bad Request (400)" Error

**Solution:**
- Verify `nevagu.com` is in `ALLOWED_HOSTS` in settings.py
- Restart your web server and application

### Issue: Both domains show the same content

**Solution:**
- Check that `DomainRoutingMiddleware` is in the `MIDDLEWARE` list in settings.py
- Verify domain names in `DOMAIN_URLCONF_MAP` match exactly (no typos)
- Clear browser cache and cookies
- Check the `Host` header is being passed correctly in your proxy configuration

### Issue: Static files not loading on nevagu.com

**Solution:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx  # or apache2
```

### Issue: Cart not working

**Solution:**
- Check that sessions are enabled in Django settings
- Verify CSRF token is present in forms
- Check browser console for JavaScript errors

### Issue: DNS not resolving

**Solution:**
- Wait for DNS propagation (can take up to 48 hours)
- Check DNS records with: `nslookup nevagu.com`
- Verify A records point to 18.236.154.235

---

## Production Checklist

Before going live, ensure:

- [ ] DNS records are configured and propagated
- [ ] SSL certificates are installed and working
- [ ] `DEBUG = False` in production settings
- [ ] Secret key is secure (not the default one)
- [ ] Static files are collected
- [ ] Database migrations are run
- [ ] Both domains load correctly
- [ ] Cart and quote request functionality works
- [ ] Mobile responsive design tested
- [ ] Error pages (404, 500) are customized
- [ ] Backup strategy is in place
- [ ] Monitoring/logging is set up

---

## Quick Reference Commands

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@18.236.154.235

# Navigate to project
cd /path/to/portfolioapp

# Pull latest code
git pull origin main

# Activate virtual environment
source /path/to/venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart services (Nginx + Gunicorn)
sudo systemctl restart nginx
sudo systemctl restart gunicorn

# Restart services (Apache)
sudo systemctl restart apache2

# Check logs
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u gunicorn -f
```

---

## Support

If you encounter issues:
1. Check the logs (see Step 6.1)
2. Verify DNS propagation: https://dnschecker.org
3. Test locally first by modifying your hosts file
4. Review the MULTI_DOMAIN_SETUP.md for additional details

---

## Next Steps After Deployment

1. **Set up email notifications** for quote requests
2. **Create a database backup strategy**
3. **Set up monitoring** (e.g., UptimeRobot, Pingdom)
4. **Configure Google Analytics** for both domains
5. **Add product images** to the Nevagu site
6. **Create custom 404/500 error pages**
7. **Set up automated deployments** (CI/CD)

Good luck with your deployment! 🚀
