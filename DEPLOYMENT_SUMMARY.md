# Quick Deployment Summary for Nevagu.com

## What's Already Done ✅

Your Django application is **already configured** for multi-domain hosting:

1. ✅ **Settings updated** - `nevagu.com` added to `ALLOWED_HOSTS`
2. ✅ **Domain routing configured** - `DOMAIN_URLCONF_MAP` maps nevagu.com to the Nevagu app
3. ✅ **Nevagu app complete** - Products, cart, and quote request system ready
4. ✅ **Middleware active** - Domain routing middleware is in place

## What You Need to Do 🚀

### 1. Register and Configure Domain (15 minutes)

**A. Register nevagu.com** (if not already done)
- Use any domain registrar (GoDaddy, Namecheap, Google Domains, etc.)

**B. Configure DNS Records**

In your domain registrar's DNS settings, add these A records:

```
Type: A
Name: @
Value: 18.236.154.235
TTL: 3600

Type: A  
Name: www
Value: 18.236.154.235
TTL: 3600
```

⏰ **Wait 5 minutes to 2 hours** for DNS propagation

---

### 2. Deploy to Your EC2 Instance (10 minutes)

**Option A: Manual Deployment**

SSH into your EC2 instance:

```bash
ssh -i your-key.pem ubuntu@18.236.154.235
```

Then run these commands:

```bash
# Navigate to your project
cd /path/to/portfolioapp

# Pull latest code
git pull origin main

# Activate virtual environment
source /path/to/venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Restart services
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```

**Option B: Use Deployment Script**

1. Edit `deploy_to_ec2.sh` and update these variables:
   - `KEY_FILE` - Path to your EC2 key file
   - `PROJECT_PATH` - Path to portfolioapp on EC2
   - `VENV_PATH` - Path to your virtual environment

2. Make it executable and run:
   ```bash
   chmod +x deploy_to_ec2.sh
   ./deploy_to_ec2.sh
   ```

---

### 3. Update Web Server Configuration (5 minutes)

**If using Nginx:**

```bash
sudo nano /etc/nginx/sites-available/portfolio
```

Add `nevagu.com www.nevagu.com` to the `server_name` line:

```nginx
server_name rodolfonevarezg.com www.rodolfonevarezg.com nevagu.com www.nevagu.com;
```

Then:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

**If using Apache:**

```bash
sudo nano /etc/apache2/sites-available/portfolio.conf
```

Add to `ServerAlias`:
```apache
ServerAlias nevagu.com
ServerAlias www.nevagu.com
```

Then:
```bash
sudo systemctl restart apache2
```

---

### 4. Set Up SSL Certificate (5 minutes)

Run Certbot to add SSL for nevagu.com:

```bash
# For Nginx
sudo certbot --nginx -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d nevagu.com -d www.nevagu.com

# For Apache
sudo certbot --apache -d rodolfonevarezg.com -d www.rodolfonevarezg.com -d nevagu.com -d www.nevagu.com
```

Follow the prompts. Certbot will automatically configure HTTPS.

---

### 5. Test Everything (5 minutes)

Visit these URLs in your browser:

1. ✅ **https://rodolfonevarezg.com** - Should show your portfolio
2. ✅ **https://nevagu.com** - Should show Nevagu medical equipment site
3. ✅ **https://nevagu.com/nevagu/products/** - Should show products
4. ✅ **https://nevagu.com/nevagu/cart/** - Should show cart

**Test the cart:**
- Add products to cart
- View cart
- Fill out quote request form
- Submit and verify success message

---

## Troubleshooting

### DNS not resolving yet?
- Check propagation: https://dnschecker.org
- Wait up to 48 hours (usually 1-2 hours)

### Getting 400 Bad Request?
- Verify `nevagu.com` is in `ALLOWED_HOSTS` in settings.py
- Restart web server: `sudo systemctl restart nginx`

### Both domains showing same content?
- Clear browser cache
- Check middleware is active in settings.py
- Verify `DOMAIN_URLCONF_MAP` has correct entries

### Static files not loading?
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

---

## Files Changed

These files have been updated with nevagu.com:

1. ✅ `portfolioapp/aiagentbase/settings.py`
   - `ALLOWED_HOSTS` includes nevagu.com
   - `DOMAIN_URLCONF_MAP` routes nevagu.com correctly

2. 📄 `NEVAGU_DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
3. 📄 `DEPLOYMENT_SUMMARY.md` - This quick reference (you are here)
4. 📄 `deploy_to_ec2.sh` - Automated deployment script

---

## Quick Command Reference

```bash
# SSH to EC2
ssh -i your-key.pem ubuntu@18.236.154.235

# Check Nginx status
sudo systemctl status nginx

# Check Gunicorn status
sudo systemctl status gunicorn

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# View Gunicorn logs
sudo journalctl -u gunicorn -f

# Restart all services
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```

---

## Timeline

| Step | Time | Status |
|------|------|--------|
| Register domain | 5 min | ⏳ To do |
| Configure DNS | 5 min | ⏳ To do |
| Wait for DNS propagation | 1-2 hrs | ⏳ To do |
| Deploy code to EC2 | 10 min | ⏳ To do |
| Update web server config | 5 min | ⏳ To do |
| Set up SSL | 5 min | ⏳ To do |
| Test everything | 5 min | ⏳ To do |
| **Total** | **~2 hours** | |

---

## Need Help?

1. Check the detailed guide: `NEVAGU_DEPLOYMENT_GUIDE.md`
2. Review multi-domain setup: `MULTI_DOMAIN_SETUP.md`
3. Check Django logs on EC2
4. Verify DNS propagation at https://dnschecker.org

---

## After Deployment

Once live, consider:
- [ ] Set up email notifications for quote requests
- [ ] Configure Google Analytics
- [ ] Add more products and images
- [ ] Set up automated backups
- [ ] Configure monitoring (UptimeRobot, Pingdom)
- [ ] Create custom 404/500 error pages

---

**Ready to deploy? Start with Step 1! 🚀**
