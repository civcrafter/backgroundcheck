#!/usr/bin/env python
import logging
from os import environ as env
import praw
import time
import re
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify

SUBREDDIT = "Devoted+Civcraft"
SEARCHSTRING = "{}"
LOGPATH = "{}/.minecraft/logs/latest.log".format(env["HOME"])

def check_player(player):
    searchstring = SEARCHSTRING.format(player)
    r = praw.Reddit(user_agent='my_cool_application')
    results = list(r.search(searchstring, subreddit=SUBREDDIT, sort="new", limit=None))

    return [result.title for result in results]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    already_checked = []
    snitchlog_regex = re.compile("(.*[ \\\\*]+.*entered snitch at.*)|(.*world.*\\\\])")
    Notify.init("Civcraft Player Background Check")

    with open(LOGPATH, "r") as file:
        #line = "[15:32:02] [Client thread/INFO]: [CHAT]  * jasiel entered snitch at Endeavour_Dam_East [volans -618 129 138]"
        while 1:
            where = file.tell()
            line = file.readline()

            if not line:
                time.sleep(1)
                file.seek(where)
            elif "[CHAT]" in line:

                if re.match(snitchlog_regex, line.split("[CHAT]")[1]) :
                    chatline = line.split("[CHAT]")[1].strip()
                    logging.info("matching chat line: \"{}\"".format(chatline))
                    player = chatline.split()[1]
                    if player in already_checked:
                        logging.info("player '{}' already checked".format(player))
                        continue

                    logging.info("checking player '{}'".format(player))
                    submissions = check_player(player)
                    already_checked.append(player)

                    if len(submissions) > 0:
                        logging.info("found {} submissions mentioning player '{}'".format(len(submissions), player))
                        summary = "WARNING: {}\n".format(player)
                        body = "\n".join(check_player(player))
                        Notify.Notification.new(summary, body).show()
                    else:
                        logging.info("No submissions found for player '{}'".format(player))
