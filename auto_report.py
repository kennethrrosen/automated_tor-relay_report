import subprocess

# Get Nyx data
nyx_command = ['nyx', '-r', 'relay1', 'user', 'ips', 'bw', 'location', 'time']
nyx_data = subprocess.run(nyx_command, capture_output=True, text=True).stdout.strip()

# Get SSH login attempts
grep_command = ['grep', 'sshd.*Failed', '/var/log/auth.log']
ssh_data = subprocess.run(grep_command, capture_output=True, text=True).stdout.strip()

# Get system updates and upgrades
updates_command = ['apt-get', 'update']
subprocess.run(updates_command)
upgrade_command = ['apt-get', 'upgrade', '-s']
upgrade_data = subprocess.run(upgrade_command, capture_output=True, text=True).stdout.strip()

# Get port scanning messages
nmap_command = ['grep', '-i', 'nmap', '/var/log/syslog']
port_data = subprocess.run(nmap_command, capture_output=True, text=True).stdout.strip()

# Format the data
nyx_data = f'<h2>Nyx Data:</h2><pre>{nyx_data}</pre>'
ssh_data = f'<h2>SSH Login Attempts:</h2><pre>{ssh_data}</pre>'
upgrade_data = f'<h2>System Updates and Upgrades:</h2><pre>{upgrade_data}</pre>'
port_data = f'<h2>Port Scanning Messages:</h2><pre>{port_data}</pre>'

# Send email with Nyx, SSH, system update, and port scan data
postfix_command = ['sendmail', '-t']
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
stdout, stderr = process.communicate(input='From: sender@example.com\nTo: recipient@example.com\nSubject: Nyx Data Report\n\n' + data)
