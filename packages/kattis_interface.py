# Standard Library.
import requests
from tqdm import tqdm
from datetime import datetime
from itertools import count
from time import sleep

# Custom modules.
from packages import html_parser

# ---

LOGIN_PAGE    = 'https://open.kattis.com/login/email?'
PROBLEMS_PAGE = 'https://open.kattis.com/problems'

def login_form(CSRF_token: str, username: str, password: str):
    """Fill up Kattis' login form and return it as a JSON object."""
    login_json = {
        'csrf_token': CSRF_token,
        'user'      : username,
        'password'  : password,
        'submit'    : 'Submit'
    }

    return login_json

def scrape_user(username: str, password: str, sites: []) -> []:
    """Scrapes the user's Kattis account and returns his/her 'timeline'.

    Historian logs into Kattis on behalf of the user and determines
    which questions have been solved. From there, the first accepted
    solution for each of those questions is identified, and its date
    recorded.

    With a collection of problems and the dates on which they were
    first solved, Historian reconstructs the user's score history by
    crediting those dates with a score equal to the sum of the
    difficulties of the problems solved on those dates. Knowing how
    many points the user earned across these various dates, the user's
    score history is simply a running sum.
    
    Assuming a certain user earns 1.0, 5.0 and 3.2 points on days 1, 4
    and 7, his/her corresponding cumulative score will be:

        day           |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |
        ---------------------------------------------------------------
        points earned | 1.0 |  -  |  -  | 5.0 |  -  |  -  | 3.2 |  -  |
        cum. score    | 1.0 | 1.0 | 1.0 | 6.0 | 6.0 | 6.0 | 9.2 | 9.2 |

    This cum. score is returned as the user's 'timeline' or score
    change over time.

    Note that all users start with 1.0 point upon sign up.
    """
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
    sleep(0.5)

    cum_timeline = []
    cum_score = 1

    for date, points in timeline:

        cum_score += points
        cum_score  = round(cum_score, 1)

        cum_timeline.append((date, cum_score))

    print(' done!', flush=True)

    return handle, cum_timeline
