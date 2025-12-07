# Multi-Domain Django Setup Guide

This project is configured to serve multiple domains from a single Django application running on AWS.

## Architecture Overview

The project uses **domain-based routing** to serve different content based on the incoming domain name:
- **Domain 1** (`rodolfonevarezg.com`) → serves `portfolioapp` (your portfolio)
- **Domain 2** (`nevagu.com`) → serves `nevagu` (medical equipment e-commerce)

## How It Works

1. **Custom Middleware** (`aiagentbase/middleware.py`): Inspects the incoming request's domain and sets the appropriate URL configuration.

2. **Domain-Specific URL Configs**:
   - `aiagentbase/urls_domain1.py` - Routes for rodolfonevarezg.com
   - `aiagentbase/urls_domain2.py` - Routes for your new domain

3. **Settings Configuration** (`settings.py`):
   - `DOMAIN_URLCONF_MAP` dictionary maps domains to their URL configurations
   - `ALLOWED_HOSTS` includes all domains that can access the application

## Setup Instructions

### 1. Configure Your New Domain Name

Edit `portfolioapp/aiagentbase/settings.py`:

```python
ALLOWED_HOSTS = [
    '18.236.154.235',
    'rodolfonevarezg.com',
    'www.rodolfonevarezg.com',
    'yournewdomain.com',        # Replace with your actual domain
    'www.yournewdomain.com',    # Replace with your actual domain
    '127.0.0.1',
    'localhost'
]

DOMAIN_URLCONF_MAP = {
    'rodolfonevarezg.com': 'aiagentbase.urls_domain1',
    'www.rodolfonevarezg.com': 'aiagentbase.urls_domain1',
    '18.236.154.235': 'aiagentbase.urls_domain1',
    'yournewdomain.com': 'aiagentbase.urls_domain2',      # Replace with your actual domain
    'www.yournewdomain.com': 'aiagentbase.urls_domain2',  # Replace with your actual domain
    '127.0.0.1': 'aiagentbase.urls_domain1',
    'localhost': 'aiagentbase.urls_domain1',
}
```

### 2. AWS Configuration

#### A. DNS Configuration (Route 53 or your DNS provider)

For **both domains**, create the following DNS records:

**Domain 1** (rodolfonevarezg.com) - Already configured:
- `A` record: `rodolfonevarezg.com` → `18.236.154.235`
- `A` record: `www.rodolfonevarezg.com` → `18.236.154.235`

**Domain 2** (your new domain):
- `A` record: `yournewdomain.com` → `18.236.154.235` (same AWS IP)
- `A` record: `www.yournewdomain.com` → `18.236.154.235` (same AWS IP)

#### B. AWS EC2 Security Group

Ensure your EC2 instance's security group allows:
- **HTTP** (Port 80) from `0.0.0.0/0`
- **HTTPS** (Port 443) from `0.0.0.0/0` (if using SSL)
- **SSH** (Port 22) from your IP

#### C. Web Server Configuration

**If using Apache**, update your virtual host configuration:

```apache
<VirtualHost *:80>
    ServerName rodolfonevarezg.com
    ServerAlias www.rodolfonevarezg.com
    ServerAlias yournewdomain.com
    ServerAlias www.yournewdomain.com
    
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
</VirtualHost>
```

**If using Nginx + Gunicorn**:

```nginx
server {
    listen 80;
    server_name rodolfonevarezg.com www.rodolfonevarezg.com yournewdomain.com www.yournewdomain.com;
    
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
}
```

### 3. SSL/HTTPS Setup (Recommended)

Use **Let's Encrypt** with Certbot to get free SSL certificates for both domains:

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-apache  # For Apache
# OR
sudo apt-get install certbot python3-certbot-nginx   # For Nginx

# Get certificates for both domains
sudo certbot --apache -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d yournewdomain.com -d www.yournewdomain.com
# OR
sudo certbot --nginx -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d yournewdomain.com -d www.yournewdomain.com
```

Update `settings.py` for production:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 4. Deploy to AWS

1. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Restart your web server**:
   ```bash
   # Apache
   sudo systemctl restart apache2
   
   # Nginx + Gunicorn
   sudo systemctl restart nginx
   sudo systemctl restart gunicorn
   ```

### 5. Testing

Test each domain locally first by modifying your `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```
127.0.0.1 yournewdomain.com
127.0.0.1 www.yournewdomain.com
```

Then visit:
- `http://rodolfonevarezg.com` → Should show portfolioapp
- `http://yournewdomain.com` → Should show nevagu

## Project Structure

```
portfolioapp/
├── aiagentbase/
│   ├── middleware.py          # Domain routing middleware
│   ├── settings.py            # Main settings with domain config
│   ├── urls.py                # Default URL config (fallback)
│   ├── urls_domain1.py        # URLs for rodolfonevarezg.com
│   └── urls_domain2.py        # URLs for your new domain
├── portfolioapp/              # Portfolio app (rodolfonevarezg.com)
└── nevagu/                    # Medical equipment e-commerce app (new domain)
    ├── views.py
    ├── urls.py
    ├── templates/
    └── ...
```

## Customizing the New App

Edit `portfolioapp/nevagu/views.py` to add your custom views:

```python
from django.shortcuts import render

def home_view(request):
    return render(request, 'nevagu/home.html', {})
```

Create templates in `portfolioapp/nevagu/templates/nevagu/`.

## Troubleshooting

### Issue: Both domains show the same content
- Check that `DomainRoutingMiddleware` is in `MIDDLEWARE` list
- Verify domain names in `DOMAIN_URLCONF_MAP` match exactly
- Clear browser cache and cookies

### Issue: 400 Bad Request
- Add domain to `ALLOWED_HOSTS` in settings.py
- Restart web server

### Issue: Static files not loading
- Run `python manage.py collectstatic`
- Check web server static file configuration
- Verify `STATIC_ROOT` and `STATIC_URL` in settings.py

## Additional Notes

- Both domains share the same database
- Both domains share the same admin panel (accessible via `/admin/` on either domain)
- You can create separate admin sites if needed by customizing the URL configs
- Consider using environment variables for domain names in production

## Next Steps

1. Replace `'yournewdomain.com'` with your actual domain name
2. Configure DNS records to point to your AWS IP
3. Set up SSL certificates
4. Customize the `nevagu` app with your content
5. Test thoroughly before going live
