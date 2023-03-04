import subprocess
import datetime

# Get Nyx data
nyx_command = ['nyx', '-r', 'relay1', 'user', 'ips', 'bw', 'location', 'time', 'version', 'uptime', 'id', 'name', 'family', 'flags']
nyx_data = subprocess.run(nyx_command, capture_output=True, text=True).stdout.strip()

# Check if Nyx data is empty
if not nyx_data:
    nyx_data = 'Nothing to show'

# Get SSH login attempts from the past 48 hours
ssh_command = ['grep', 'sshd.*Failed', '/var/log/auth.log', '-n', f'-e "{(datetime.datetime.now() - datetime.timedelta(hours=48)).strftime("%b %d %H:%M:%S")}"']
ssh_data = subprocess.run(ssh_command, capture_output=True, text=True).stdout.strip()

# Check if SSH data is empty
if not ssh_data:
    ssh_data = 'Nothing to show'

# Get system updates and upgrades
updates_command = ['apt-get', 'update']
subprocess.run(updates_command)
upgrade_command = ['apt-get', 'upgrade', '-s']
upgrade_data = subprocess.run(upgrade_command, capture_output=True, text=True).stdout.strip()

# Check if upgrade data is empty
if not upgrade_data:
    upgrade_data = 'Nothing to show'

# Get port scanning messages
nmap_command = ['grep', '-i', 'nmap', '/var/log/syslog']
port_data = subprocess.run(nmap_command, capture_output=True, text=True).stdout.strip()

# Check if port scanning data is empty
if not port_data:
    port_data = 'Nothing to show'

# Format the data
nyx_data = f'<h2>Nyx Data:</h2><pre>{nyx_data}</pre>'
ssh_data = f'<h2>SSH Login Attempts:</h2><pre>{ssh_data}</pre>'
upgrade_data = f'<h2>System Updates and Upgrades:</h2><pre>{upgrade_data}</pre>'
port_data = f'<h2>Port Scanning Messages:</h2><pre>{port_data}</pre>'

# Send email with Nyx, SSH, system update, and port scan data
postfix_command = ['sendmail', '-t']
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
body = f'<html><body>{nyx_data}<br>{ssh_data}<br>{upgrade_data}<br>{port_data}</body></html>'
stdout, stderr = process.communicate(input=f'From: sender@example.com\nTo: recipient@example.com\nSubject: Tor Node Report\nContent-Type: text/html\n\n{body}')
