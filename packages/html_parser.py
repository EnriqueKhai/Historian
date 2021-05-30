# Standard Library.
import re
from bs4 import BeautifulSoup
from datetime import datetime

# ---

CSRF_PATTERN   = r'name="csrf_token" value="([0-9]{40})"'
HANDLE_PATTERN = r'<div class="user-infobox-name">[^<]*<a href="/users/(.+)">'

def extract_CSRF_token(html: str):
    match = re.search(CSRF_PATTERN, html)

    if match:
        CSRF_token = match.expand(r'\1')
        return CSRF_token

    else:
        return None

def extract_kattis_handle(html: str):
    match = re.search(HANDLE_PATTERN, html)

    if match:
        handle = match.expand(r'\1')
        return handle

    else:
        return None

def extract_problems_solved(html: str):
    problems_solved = []

    soup = BeautifulSoup(html, 'lxml')
    table = soup.tbody

    for row in table.find_all('tr'):
        cols = row.find_all('td')

        problem_id = cols[0].a['href'].split('/')[2]
        difficulty = cols[8].text.strip()[-3:]

        problem = {
            'id'        : problem_id,
            'difficulty': float(difficulty)
        }

        problems_solved.append(problem)

    return problems_solved

def extract_first_solved(html: str):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.tbody
    rows  = table.find_all('tr')

    for row in rows[::-1]:
        cols = row.find_all('td')

        if 'Accepted' in cols[3].text:
            date = cols[1].text.strip()
            date = date.split(' ')[0]

            first_solve = datetime.strptime(date, '%Y-%m-%d')

            return first_solve, len(rows)

    return None, len(rows)
