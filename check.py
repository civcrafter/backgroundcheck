#!/usr/bin/env python
import praw

playertocheck = "eeshaw123"
subreddittocheck = "Civcraft"

r = praw.Reddit(user_agent='my_cool_application')
results = list(r.search(playertocheck+" bounty", subreddit=subreddittocheck, sort="new", limit=None))
print("\n".join([str(r) for r in results]))
print()
results = list(r.search(playertocheck, subreddit=subreddittocheck, sort="new", limit=None))
print("\n".join([str(r) for r in results if "bounty" in r.title.lower() or "bounty" in r.selftext.lower()]))
