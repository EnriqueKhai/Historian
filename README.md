# Historian

Historian is a Kattis webscraper built to reconstruct a user's score history
over time. Here's how it works.

Historian will log into Kattis on behalf of its user and determine which problems
have been solved so far. From there, it will locate each problems' first accepted
submission and record the corresponding dates.

Historian then credits those problem's difficulties (as a score) to those dates,
effectively backdating the user's ACs and determining the total number of points
earned on those dates.

Once done, the cumulative total (or the user's 'timeline') can be reconstructed by
computing a running total. Suppose the user earns 1.0, 5.0 and 3.2 points on days 1,
4 and 7 respectively. The reconstructed timeline will then be:

```
Days           |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |
----------------------------------------------------------------
Points Earned  | 1.0 |  -  |  -  | 5.0 |  -  |  -  | 3.2 |  -  |
Cum. Score     | 1.0 | 1.0 | 1.0 | 6.0 | 6.0 | 6.0 | 9.2 | 9.2 |
```

As the final step, Historian will save the user's timeline as a `.csv` file for
plotting (using Excel, Pandas, etc).

# Installation

```
git clone https://github.com/EnriqueKhai/Historian.git
pip3 install -r requirements.txt
python3 historian.py
```
# For non-NUS users

Replace `'https://nus.kattis.com'` in `sites` (`historian.py`, line 21) with your school's
Kattis site or remove it altogether. This ensures that Historian knows where to scrape your
submissions from.
