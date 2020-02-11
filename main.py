import argparse
import logging
import sys
from pathlib import Path

import requests
from mcstatus import MinecraftServer

# parse args
parser = argparse.ArgumentParser(description="Get the count of minecraft players online and send a groupme message if the count changes")
parser.add_argument("groupme", type=str, help="the groupme bot ID / token")
parser.add_argument('server', type=str, help="the minecraft server address")
parser.add_argument('--debug', '-d', default=False, action='store_true', help="Enable debug logging. defaults to false")
args = vars(parser.parse_args())

GROUPME_BOT_ID      = args['groupme']
SERVER_URL          = args['server']
DEBUG               = args['debug']

# setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if DEBUG else logging.WARN)
logger = logging.getLogger("minecraft_groupme_notifier")

server = MinecraftServer(SERVER_URL)
status = server.status()
count = status.players.online
logger.debug("{} players online".format(count))

# get file
p = Path("~", ".local", "minecraft_groupme").expanduser()
p.mkdir(parents=True, exist_ok=True)
# use the server name as the file name so we can run multiple instances of this
file = p / SERVER_URL


def write_count():
    """
    Write the current count to file
    """
    logger.debug("writing player count to disk")
    with open(file, "w") as f:
        f.write(str(count))


count_change = False
if file.exists():
    logger.debug("Previous count file exists")
    with open(file, "r") as f:
        prev_count = f.readline()
        # is it even a number?
        if prev_count.isdigit():
            if int(prev_count) != count:
                count_change = True
        else:
            # if last wasn't a number lets overwrite it
            count_change = True
else:
    logger.debug("Previous count file does not exist")
    write_count()

logger.debug("count changed? :" + str(count_change))
if count_change:
    # write the count to file
    write_count()
    logger.debug("Count has changed")

    # send groupme message
    res = requests.post("https://api.groupme.com/v3/bots/post", data={
        "text": "All players offline" if count == 0 else "{} player(s) online".format(count),
        "bot_id": GROUPME_BOT_ID
    })

    if res.status_code >= 300:
        logger.error("{} GroupMe message sent unsuccessfully {}".format(res.status_code, res.text))
