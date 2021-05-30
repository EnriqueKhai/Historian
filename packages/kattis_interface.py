# Standard Library.
import requests
from tqdm import tqdm
from datetime import datetime
from itertools import count
from typing import List

# Custom modules.
from packages import html_parser

# ---

LOGIN_PAGE    = 'https://open.kattis.com/login/email?'
PROBLEMS_PAGE = 'https://open.kattis.com/problems'

def login_form(CSRF_token: str, username: str, password: str):

    login_json = {
        'csrf_token': CSRF_token,
        'user'      : username,
        'password'  : password,
        'submit'    : 'Submit'
    }

    return login_json

def scrape_user(username: str, password: str, sites: List[str]):

    # Begin new web session.
    s = requests.Session()

    # Visit login page.
    resp = s.get(LOGIN_PAGE)
    html = resp.text

    # Get CSRF token in login form.
    CSRF_token = html_parser.extract_CSRF_token(html)

    # Construct request payload.
    payload = login_form(CSRF_token, username, password)

    # Log in.
    resp = s.post(LOGIN_PAGE, data=payload)
    html = resp.text

    # Exit if login was unsuccessful.
    if 'Unknown Username/Password' in html:
        print('Login failed!', flush=True)
        exit(0)

    # Extract user's Kattis handle.
    handle = html_parser.extract_kattis_handle(html)

    # Scrape all problems solved by user.
    problems_solved = []

    url_queries = {
        'show_solved' : 'on',
        'show_tried'  : 'off',
        'show_untried': 'off',
    }

    print(f'Profiling user {handle}...', end='', flush=True)

    for i in count():

        url_queries['page'] = i

        resp = s.get(PROBLEMS_PAGE, params=url_queries)
        html = resp.text

        extracts = html_parser.extract_problems_solved(html)

        if len(extracts) == 0:
            break

        problems_solved += extracts

    print(' done!', flush=True)
    print(f'Problems solved: {len(problems_solved)}\n', flush=True)

    # Backdate all problems solved to their first AC.
    print('Backdating ACs:', flush=True)
    print('---------------', flush=True)

    for problem in tqdm(problems_solved, ncols=100):

        # For each problem solved, the first AC could be at any of the sites.
        for site in sites:
            for i in count():

                resp = s.get(f'{site}/users/{handle}/submissions/{problem["id"]}?page={i}')
                html = resp.text

                date, nrows = html_parser.extract_first_solved(html)

                if date:
                    if 'first_solved' not in problem:
                        problem['first_solved'] = date

                    elif date < problem['first_solved']:
                        problem['first_solved'] = date

                # Optimisation; break on the last page.
                if nrows != 100:
                    break

    print(flush=True)

    # Group problems by when they were first solved.
    calendar = {}

    for problem in problems_solved:

        date_solved = problem['first_solved']

        # Update points earned on that day.
        if date_solved not in calendar:
            calendar[date_solved]  = problem['difficulty']

        else:
            calendar[date_solved] += problem['difficulty']

    # Order keys chronologically.
    timeline = []

    for date, points in calendar.items():
        timeline.append((date, points))

    timeline.sort()

    # Reconstruct user's score over time.
    print('Reconstructing user\'s score history...', end='', flush=True)

    cum_timeline = []
    cum_score = 1

    for date, points in timeline:

        cum_score += points
        cum_score  = round(cum_score, 1)

        cum_timeline.append((date, cum_score))

    print(' done!', flush=True)

    return handle, cum_timeline
