# Standard Library.
from getpass import getpass
from datetime import datetime
from time import sleep
import csv

# Custom modules.
from packages import kattis_interface as kattis

# ---

# Prompt user for login details.
username = input('Username: ')
password = getpass('Password: ')

print(flush=True)

# Locations to scrape user submissions.
sites = [
    'https://open.kattis.com',
    'https://nus.kattis.com'
]

# Scrape all problems solved.
handle, timeline = kattis.scrape_user(username, password, sites)

# Write results to a CSV file.
print(f'Preparing {handle}.csv...', end='', flush=True)
sleep(0.5)

with open(f'{handle}.csv', 'w') as fd:
    writer = csv.writer(fd)

    # CSV header.
    writer.writerow(['Date', 'Cumulative Score'])

    # CSV body.
    for date, cum_score in timeline:
        formatted_date = date.strftime('%Y-%m-%d')
        writer.writerow([formatted_date, cum_score])

print(' done!', flush=True)

