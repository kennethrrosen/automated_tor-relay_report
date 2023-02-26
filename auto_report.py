import subprocess

# Use Nyx to retrieve the data
nyx_command = ['nyx', '-r', 'relay1', 'user', 'ips', 'bw', 'location', 'time']
result = subprocess.run(nyx_command, capture_output=True, text=True)

# Format the data
data = result.stdout.strip()

# Use mailx to send the email
mailx_command = ['mailx', '-s', 'Nyx Data Report', '-r', 'sender@example.com', 'recipient@example.com']
subprocess.run(mailx_command, input=data, text=True)
