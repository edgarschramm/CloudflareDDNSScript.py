# Cloudflare Dynamic DNS (DDNS) Updater

## Overview

This Python script provides a Dynamic DNS (DDNS) solution using Cloudflare's API. It automatically updates your DNS A records with your current public IP address, ensuring that your domain always points to the correct IP, even when it changes.

## Features

- Automatically detects your current public IP address
- Updates Cloudflare DNS A records when IP changes
- Configurable update interval
- Runs as a system service
- Supports multiple DNS records

## Prerequisites

- Python 3.x
- Cloudflare account
- Cloudflare API token with appropriate permissions

## Installation Steps

### 1. Cloudflare API Token Preparation

1. Log in to your Cloudflare account
2. Go to "My Profile" > "API Tokens"
3. Click "Create Token"
4. Choose "Edit zone DNS" template
5. Select your specific zone (domain)
6. Copy the generated token

### 2. Modify the Script

Edit `cloudflare_ddns.py` and update the following variables:
- `self.api_token`: Replace with your Cloudflare API token
- `self.zone_name`: Your domain name (e.g., 'example.com')
- `self.record_name`: The specific record to update (e.g., 'home.example.com')
- `self.update_interval`: Time between IP checks (default: 300 seconds)

### 3. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

### 4. Install the Service

```bash
# Make installation script executable
chmod +x install_cloudflare_ddns.sh

# Install the service
sudo ./install_cloudflare_ddns.sh
```

## Service Management

After installation, you can manage the service using systemctl:

```bash
# Check service status
sudo systemctl status cloudflare-ddns

# Start the service
sudo systemctl start cloudflare-ddns

# Stop the service
sudo systemctl stop cloudflare-ddns

# Restart the service
sudo systemctl restart cloudflare-ddns
```

## Troubleshooting

- Ensure your API token has the correct permissions
- Check system logs for detailed error messages:
  ```bash
  journalctl -u cloudflare-ddns
  ```

## Customization

- Modify `update_interval` to change how frequently the IP is checked
- Adjust logging and error handling in the script as needed
