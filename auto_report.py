import subprocess

# Use Nyx to retrieve the data
nyx_command = ['nyx', '-r', 'relay1', 'user', 'ips', 'bw', 'location', 'time']
result = subprocess.run(nyx_command, capture_output=True, text=True)

# Format the data
data = result.stdout.strip()

# Use postfix to send the email
postfix_command = ['sendmail', '-t']
process = subprocess.Popen(postfix_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
stdout, stderr = process.communicate(input='From: sender@example.com\nTo: recipient@example.com\nSubject: Nyx Data Report\n\n' + data)
