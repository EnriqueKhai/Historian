# Introduction

[Kattis](https://open.kattis.com/) is an Online Judge platform where users can
create an account, solve algorithmic problems and earn points to climb the ranks.
That said, Kattis has neither an inbuilt feature nor an API that allows users to
visualise their score change (i.e. progress) over time.

It is this problem that Historian attempts to solve.

# Overview

Historian is a Kattis webscraper built to **reconstruct a user's score history**
over time. For a video demo, click [here](https://www.loom.com/share/a97cd7d9ac94473aa41317424e5bfd7e).

![image](https://user-images.githubusercontent.com/42400406/121766091-2c0a6d80-cb82-11eb-8cdb-ca9970ab69b1.png)

Otherwise, here's how it works.

Historian will log into Kattis on behalf of its user and determine which problems
have been solved so far. From there, it will locate each problems' first accepted
submission and record the corresponding dates.

Historian then credits those problem's difficulties (as a score) to those dates,
effectively backdating the user's ACs and determining the total number of points
earned on those dates.

Once done, the cumulative total (or the user's *timeline*) can be reconstructed by
computing a running sum. Suppose the user earns `1.0`, `5.0` and `3.2` points on days
1, 4 and 7 respectively. The reconstructed *timeline* will then be:

```
Days           |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |
----------------------------------------------------------------
Points Earned  | 1.0 |  -  |  -  | 5.0 |  -  |  -  | 3.2 |  -  |
Cum. Score     | 1.0 |  -  |  -  | 6.0 |  -  |  -  | 9.2 |  -  |
```

As the final step, Historian will save the user's *timeline* as a `.csv` file. This
allows users to plot (using Excel, Pandas, etc) graphs like this:

![image](https://user-images.githubusercontent.com/42400406/120999366-9ce50a80-c7bb-11eb-8a10-e8c8be1a34cf.png)

# Installation

```
git clone https://github.com/EnriqueKhai/Historian.git
cd Historian
pip3 install -r requirements.txt
python3 historian.py
```
# For non-NUS users

Replace `'https://nus.kattis.com'` in `sites[]` (`historian.py`, line 21) with your own school's
Kattis site (e.g. `'https://kth.kattis.com'`) or remove it altogether. This ensures that Historian
knows where to look in trying to scrape your submissions.

```Python3
16   print(flush=True)
17
18   # Locations to scrape user submissions.
19   sites = [
20       'https://open.kattis.com',
21       'https://nus.kattis.com'       # <------- replace this line!
22   ]
23 
24   # Scrape all problems solved.
25   handle, timeline = kattis.scrape_user(username, password, sites)
```
