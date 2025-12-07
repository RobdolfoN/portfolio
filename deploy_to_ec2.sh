#!/bin/bash

# Deployment Script for Nevagu.com on EC2
# This script helps deploy updates to your EC2 instance

set -e  # Exit on error

echo "🚀 Starting deployment to EC2..."

# Configuration - UPDATE THESE VALUES
EC2_IP="18.236.154.235"
EC2_USER="ubuntu"
KEY_FILE="path/to/your-key.pem"  # UPDATE THIS
PROJECT_PATH="/home/ubuntu/portfolio/portfolioapp"  # UPDATE THIS
VENV_PATH="/home/ubuntu/portfolio/venv"  # UPDATE THIS

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "  EC2 IP: $EC2_IP"
echo "  User: $EC2_USER"
echo "  Project Path: $PROJECT_PATH"
echo ""

# Function to run commands on EC2
run_on_ec2() {
    ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" "$1"
}

# Step 1: Test SSH connection
echo -e "${YELLOW}1. Testing SSH connection...${NC}"
if run_on_ec2 "echo 'Connection successful'"; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${RED}✗ SSH connection failed. Check your KEY_FILE path and EC2 credentials.${NC}"
    exit 1
fi

# Step 2: Pull latest code
echo -e "${YELLOW}2. Pulling latest code from repository...${NC}"
run_on_ec2 "cd $PROJECT_PATH && git pull origin main"
echo -e "${GREEN}✓ Code updated${NC}"

# Step 3: Activate virtual environment and install dependencies
echo -e "${YELLOW}3. Installing dependencies...${NC}"
run_on_ec2 "source $VENV_PATH/bin/activate && cd $PROJECT_PATH && pip install -r requirements.txt"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 4: Collect static files
echo -e "${YELLOW}4. Collecting static files...${NC}"
run_on_ec2 "source $VENV_PATH/bin/activate && cd $PROJECT_PATH && python manage.py collectstatic --noinput"
echo -e "${GREEN}✓ Static files collected${NC}"

# Step 5: Run migrations
echo -e "${YELLOW}5. Running database migrations...${NC}"
run_on_ec2 "source $VENV_PATH/bin/activate && cd $PROJECT_PATH && python manage.py migrate"
echo -e "${GREEN}✓ Migrations complete${NC}"

# Step 6: Restart services
echo -e "${YELLOW}6. Restarting services...${NC}"

# Check which web server is running
if run_on_ec2 "systemctl is-active --quiet nginx"; then
    echo "  Restarting Nginx..."
    run_on_ec2 "sudo systemctl restart nginx"
    echo -e "${GREEN}✓ Nginx restarted${NC}"
fi

if run_on_ec2 "systemctl is-active --quiet apache2"; then
    echo "  Restarting Apache..."
    run_on_ec2 "sudo systemctl restart apache2"
    echo -e "${GREEN}✓ Apache restarted${NC}"
fi

if run_on_ec2 "systemctl is-active --quiet gunicorn"; then
    echo "  Restarting Gunicorn..."
    run_on_ec2 "sudo systemctl restart gunicorn"
    echo -e "${GREEN}✓ Gunicorn restarted${NC}"
fi

# Step 7: Check service status
echo -e "${YELLOW}7. Checking service status...${NC}"
run_on_ec2 "systemctl status nginx --no-pager -l | head -n 10" || true
run_on_ec2 "systemctl status gunicorn --no-pager -l | head -n 10" || true

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "🌐 Your sites should now be live at:"
echo "  - https://rodolfonevarezg.com"
echo "  - https://nevagu.com"
echo ""
echo "📊 To check logs, run:"
echo "  ssh -i $KEY_FILE $EC2_USER@$EC2_IP"
echo "  sudo tail -f /var/log/nginx/error.log"
echo ""
