#!/bin/bash

# Cloudflare DDNS Service Installer

set -e

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo." 
   exit 1
fi

# Configuration
SERVICE_NAME="cloudflare-ddns"
SCRIPT_NAME="cloudflare_ddns.py"
INSTALL_DIR="/opt/cloudflare-ddns"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Detect Python version (prefer Python 3)
PYTHON_CMD=$(which python3)
if [[ -z "$PYTHON_CMD" ]]; then
    echo "Python 3 is required. Please install Python 3."
    exit 1
fi

# Ensure required packages are installed
echo "Checking and installing required dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv

# Create installation directory
echo "Creating installation directory..."
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install requests

# Copy the script (now using current directory)
echo "Copying DDNS script..."
cp "$(dirname "$0")/$SCRIPT_NAME" $INSTALL_DIR/$SCRIPT_NAME

# Create systemd service file
echo "Creating systemd service file..."
cat > $SERVICE_FILE << EOL
[Unit]
Description=Cloudflare DDNS Updater
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/$SCRIPT_NAME
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOL

# Set correct permissions
chmod 644 $SERVICE_FILE
chmod +x $INSTALL_DIR/$SCRIPT_NAME

# Reload systemd, enable and start service
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "Cloudflare DDNS service installed successfully!"
echo "You need to edit the script to add your Cloudflare API token and domain details."
echo "You can edit the script at: $INSTALL_DIR/$SCRIPT_NAME"
echo ""
echo "Useful commands:"
echo "- Check service status: systemctl status $SERVICE_NAME"
echo "- Stop service: systemctl stop $SERVICE_NAME"
echo "- Start service: systemctl start $SERVICE_NAME"
echo "- Restart service: systemctl restart $SERVICE_NAME"
