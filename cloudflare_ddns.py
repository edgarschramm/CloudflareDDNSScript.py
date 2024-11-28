import requests
import time
from datetime import datetime

class CloudflareDDNS:
    def __init__(self):
        # Replace this with your actual API token
        self.api_token = "<your_api_token>"
        self.zone_name = "<your_domain>"
        self.record_name = "<your_domain>"
        self.update_interval = 300  # updates every 5 minutes
        self.zone_id = None
        self.initialize_zone()

    def initialize_zone(self):
        """Get zone ID"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            print("Fetching zone information from Cloudflare...")
            response = requests.get(
                'https://api.cloudflare.com/client/v4/zones',
                headers=headers
            )
            
            if not response.ok:
                print(f"Error from Cloudflare API: {response.status_code}")
                print(f"Response: {response.text}")
                exit(1)
                
            data = response.json()
            if not data['success']:
                print(f"API request failed: {data['errors']}")
                exit(1)
                
            all_zones = data['result']
            for zone in all_zones:
                if zone['name'] == self.zone_name:
                    self.zone_id = zone['id']
                    print(f"Successfully found zone ID for {self.zone_name}")
                    return
            
            print(f"Error: Could not find zone {self.zone_name}")
            print("Available zones:", [zone['name'] for zone in all_zones])
            exit(1)
                
        except Exception as e:
            print(f"Error initializing zone: {e}")
            exit(1)

    def get_current_ip(self):
        """Get current public IP address"""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except Exception as e:
            print(f"Error getting current IP: {e}")
            return None

    def get_dns_records(self):
        """Get all DNS records from Cloudflare"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            print("Fetching DNS records...")
            response = requests.get(
                f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records',
                headers=headers
            )
            records = response.json()['result']
            print("\nFound these A records:")
            for record in records:
                if record['type'] == 'A':
                    print(f"- {record['name']} ({record['content']})")
            return records
        except Exception as e:
            print(f"Error getting DNS records: {e}")
            return None

    def update_dns_record(self, record_id, ip_address, record_name):
        """Update DNS record with new IP"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'type': 'A',
            'name': record_name,
            'content': ip_address,
            'proxied': True
        }
        
        try:
            response = requests.put(
                f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{record_id}',
                headers=headers,
                json=data
            )
            return response.json()['success']
        except Exception as e:
            print(f"Error updating DNS record: {e}")
            return False

    def run(self):
        """Main loop to check and update IP"""
        print(f"Starting Cloudflare DDNS updater for {self.zone_name}")
        
        # Get initial list of records
        records = self.get_dns_records()
        if not records:
            print("No DNS records found")
            exit(1)
            
        # Filter for A records
        a_records = [r for r in records if r['type'] == 'A']
        if not a_records:
            print("No A records found")
            exit(1)
        
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_ip = self.get_current_ip()
            
            if current_ip:
                for record in a_records:
                    if record['content'] != current_ip:
                        if self.update_dns_record(record['id'], current_ip, record['name']):
                            print(f"[{current_time}] Successfully updated IP for {record['name']} to {current_ip}")
                        else:
                            print(f"[{current_time}] Failed to update IP for {record['name']}")
                    else:
                        print(f"[{current_time}] IP hasn't changed ({current_ip}) for {record['name']}")
            else:
                print(f"[{current_time}] Failed to get current IP")
            
            time.sleep(self.update_interval)

if __name__ == "__main__":
    ddns = CloudflareDDNS()
    ddns.run()
