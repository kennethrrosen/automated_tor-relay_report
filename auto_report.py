###UNDER REVIEW

import subprocess
import datetime

# Get Nyx version & stats
nyx_command = ['nyx','-v']
nyx_data = subprocess.run(nyx_command, capture_output=True, text=True).stdout.strip()

# Get Tor stats
stats_command = ['cat', '/var/lib/tor/stats/*']
stats_data = subprocess.run(stats_command, capture_output=True, text=True).stdout.strip()
if not stats_data:
    stats_data = 'Nothing to show'

# Check and get system logs for error messages
log_command = ['cat', '/var/log/syslog']
log_data = subprocess.run(log_command, capture_output=True, text=True).stdout.strip()
log_command = ['grep', '-E', 'error|critical|fail|warning', '/var/log/syslog']
log_data_filtered = subprocess.run(log_command, capture_output=True, text=True).stdout.strip()
if not log_data_filtered:
    log_data_filtered = 'Nothing to show'

# Get SSH login attempts from the past 48 hours
ssh_command = ['grep', 'sshd.*Failed', '/var/log/auth.log', '-n', f'-e "{(datetime.datetime.now() - datetime.timedelta(hours=48)).strftime("%b %d %H:%M:%S")}"']
ssh_data = subprocess.run(ssh_command, capture_output=True, text=True).stdout.strip()
if not ssh_data:
    ssh_data = 'Nothing to show'

# Get system updates and upgrades
updates_command = ['apt-get', 'update']
subprocess.run(updates_command)
upgrade_command = ['apt-get', 'upgrade', '-s']
upgrade_data = subprocess.run(upgrade_command, capture_output=True, text=True).stdout.strip()
if not upgrade_data:
    upgrade_data = 'Nothing to show'

# Get port scanning messages
nmap_command = ['grep', '-i', 'nmap', '/var/log/syslog']
port_data = subprocess.run(nmap_command, capture_output=True, text=True).stdout.strip()
if not port_data:
    port_data = 'Nothing to show'

# Format the data
nyx_data = f'<h3>Nyx Version:</h3><pre>{nyx_data}</pre>'
stats_data = '<h3>Tor Stats:</h3><pre>{}</pre>'.format(stats_data)
log_data_filtered = f'<h3>System Logs:</h3><pre>{log_data_filtered}</pre>'
ssh_data = f'<h3>SSH Login Attempts:</h3><pre>{ssh_data}</pre>'
upgrade_data = f'<h3>System Updates and Upgrades:</h3><pre>{upgrade_data}</pre>'
port_data = f'<h3>Port Scanning Messages:</h3><pre>{port_data}</pre>'

# Send email with Nyx, SSH, system update, and port scan data
postfix_command = ['sendmail', '-t']
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
body = f'<html><body>{nyx_data}<br>{stats_data}<br>{log_data_filtered}<br>{ssh_data}<br>{upgrade_data}<br>{port_data}</body></html>'
stdout, stderr = process.communicate(input=f'From: sender@example.com\nTo: recipient@example.com\nSubject: Tor Node Report\nContent-Type: text/html\n\n{body}')


# Send email with Nyx, SSH, system update, and port scan data
postfix_command = ['sendmail', '-t']
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
body = f'<html><body>{nyx_data}<br>{stats_data}<br>{log_data_filtered}<br>{ssh_data}<br>{upgrade_data}<br>{port_data}</body></html>'
stdout, stderr = process.communicate(input=f'From: sender@example.com\nTo: recipient@example.com\nSubject: Tor Node Report\nContent-Type: text/html\n\n{body}')
