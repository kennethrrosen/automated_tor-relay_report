# automated_tor-relay_report
A simple script to send the relay admin a weekly report on Tor stats and server activity (SSH, port scanning). This script assumes you've installed `sudo apt install mailx` and have setup accordingly. To run the script weekly, you can use a scheduling tool such as cron (as outlined below).

1. Copy the script to a directory on your Tor server, such as `/usr/local/bin` and make the script executable with `chmod +x /usr/local/bin/auto_report.py`

2. Open the crontab configuration and add a new line to the crontab file with the following forma:
```
crontab -e
0 0 * * 0 /usr/local/bin/auto_report.py
```
NOTE: This will run the script every Sunday at midnight (0:00).

3. Save and exit the crontab file. Then restart the cron daemon to apply the changes.
```
sudo service cron restart
```
