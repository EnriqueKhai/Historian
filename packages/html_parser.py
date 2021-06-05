# Standard Library.
import re
from bs4 import BeautifulSoup
from datetime import datetime

# ---

CSRF_PATTERN   = r'name="csrf_token" value="([0-9]{40})"'
HANDLE_PATTERN = r'<div class="user-infobox-name">[^<]*<a href="/users/(.+)">'

def extract_CSRF_token(html: str) -> str:
    """Returns the 40-digit CSRF token found in Kattis' login form."""
    match = re.search(CSRF_PATTERN, html)

    if match:
        CSRF_token = match.expand(r'\1')
        return CSRF_token

    else:
        return None

def extract_kattis_handle(html: str) -> str:
    """Returns the user's kattis handle."""
    match = re.search(HANDLE_PATTERN, html)

    if match:
        handle = match.expand(r'\1')
        return handle

    else:
        return None

def extract_problems_solved(html: str) -> []:
    """Formats and returns a list of problems solved by the user.

    The html page supplied should cotain a list of problems that
    have been solved by the user. Such a list should exist as a
    HTML table, with each table row corresponding to a unique
    problem solved.

    From there, each table row will be extracted and parsed using
    BeautifulSoup4. Specifically, the problem's id and difficulty
    will be extracted from said rows and stored as a dictionary
    of the form:

        problem = {
            'id'        : ...,
            'difficulty': ...
        }

    A list of such dictionaries is returned once all rows have
    been parsed.
    """
    problems_solved = []

    soup = BeautifulSoup(html, 'lxml')
    table = soup.tbody

    for row in table.find_all('tr'):
        cols = row.find_all('td')

        # Extract id from path stub.
        problem_id = cols[0].a['href'].split('/')[2]

        # Some difficulties exist as a range, e.g. '1.7 - 3.4'.
        difficulty = cols[8].text.strip()[-3:]

        problem = {
            'id'        : problem_id,
            'difficulty': float(difficulty)
        }

        problems_solved.append(problem)

    return problems_solved

def extract_first_solved(html: str) -> (datetime, int):
    """Extracts the date of the first accepted submission.

    The html supplied should contain a list of submissions
    for a particular problem. Such a list should exist as
    a HTML table, with each row corresponding to a particular
    submission. Further, this list should contain submissions
    that are ordered chronologically, with the lastest
    submission as the first row.

    From there, the first accepted submission (i.e. earliest)
    is determined and its corresponding date returned.

    The length of the list (or HTML table) is also returned.
    Kattis displays submissions in pages of 100. Thus, the
    html supplied is the last page of submissions for a
    particular problem if said length is less than 100. This
    return field is intended as an optimization, allowing the
    caller to make one less HTTP call (to the 'next page').
    """
    soup = BeautifulSoup(html, 'lxml')

    table = soup.tbody
    rows  = table.find_all('tr')

    # Iterate from the back to find the earliest AC.
    for row in rows[::-1]:
        cols = row.find_all('td')

        # Problems with subtask scoring have the 'Accepted (100)' status.
        if 'Accepted' in cols[3].text:
            date = cols[1].text.strip()
            date = date.split(' ')[0]

            first_solve = datetime.strptime(date, '%Y-%m-%d')

            return first_solve, len(rows)

    return None, len(rows)
