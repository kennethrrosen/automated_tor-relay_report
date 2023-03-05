import subprocess
import datetime
import os

def get_command_output(command, no_output_message='Nothing to show'):
    """Runs a command and returns its output, or a default message if the output is empty."""
    output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
    return output if output else no_output_message

# Get Nyx version
nyx_command = ['nyx', '-v']
nyx_data = get_command_output(nyx_command, no_output_message='Unable to get Nyx version')

# Get Tor stats
stats_command = ['sudo', 'cat', '/var/lib/tor/stats/hidserv-v3-stats', '/var/lib/tor/stats/hidserv-stats', '/var/lib/tor/stats/dirreq-stats', '/var/lib/tor/stats/bridge-stats']
stats_data = get_command_output(stats_command)
stats_data = stats_data.replace('\n', '<br>')
if not stats_data:
    stats_data = 'Nothing to show'

# Get system logs for error messages
log_command = ['grep', '-E', 'error|critical|fail|warning', '/var/log/syslog']
log_data_filtered = get_command_output(log_command)
log_data_filtered = log_data_filtered.replace('\n', '<br>')
if not log_data_filtered:
    log_data_filtered = 'Nothing to show'

# Get SSH login attempts from the past 48 hours
ssh_command = ['grep', 'sshd.*Failed', '/var/log/auth.log', '-n', f'-e "{(datetime.datetime.now() - datetime.timedelta(hours=48)).strftime("%b %d %H:%M:%S")}"']
ssh_data = get_command_output(ssh_command)

# Get system updates and upgrades
upgrade_command = ['apt-get', 'upgrade', '-s']
upgrade_data = get_command_output(upgrade_command)

# Get port scanning messages
nmap_command = ['grep', '-i', 'nmap', '/var/log/syslog']
port_data = get_command_output(nmap_command)

# Save all data to a file
output_filename = 'auto_report.txt'
with open(output_filename, 'w') as output_file:
    output_file.write(f'<h3>Nyx Version:</h3>\n{nyx_data}\n\n')
    output_file.write(f'<h3>Tor Stats:</h3>\n{stats_data}\n\n')
    output_file.write(f'<h3>System Logs:</h3>\n{log_data_filtered}\n\n')
    output_file.write(f'<h3>SSH Login Attempts:</h3>\n{ssh_data}\n\n')
    output_file.write(f'<h3>System Updates and Upgrades:</h3>\n{upgrade_data}\n\n')
    output_file.write(f'<h3>Port Scanning Messages:</h3>\n{port_data}\n\n')

# Send email with auto report in body
postfix_command = ['sendmail', '-t']
with open(output_filename, 'r') as report_file:
    report_data = report_file.read()
body = f'<html><body>Please find the auto report below.</body></html>\n\n{report_data}'
message = f'From: sender@example.com\nTo: recipient@example.com\nSubject: Tor Node Report\nContent-Type: text/html\n\n{body}'
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
stdout, stderr = process.communicate(input=message)
