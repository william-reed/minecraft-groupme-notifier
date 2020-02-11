# Minecraft GroupMe Notifier
Get notified in GroupMe when players go on (or off) a Minecraft server

```
usage: main.py [-h] [--debug] groupme server

Get the count of minecraft players online and send a groupme message if the
count changes

positional arguments:
  groupme      the groupme bot ID / token
  server       the minecraft server address

optional arguments:
  -h, --help   show this help message and exit
  --debug, -d  Enable debug logging. defaults to false

```

## Setup
```
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

## Running
Meant to be run as a cron job every 5 minutes to detect changes and act as a debounce window
e.g. `*/5 * * * *`