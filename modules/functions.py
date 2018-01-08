import botoptions, urllib.request, json, config, os


def CheckForString(msg):
    """Checks the message to see if it matches the hey eli strings"""
    for string in botoptions.hey_eli:
        if msg.content.lower().rfind(string) != -1:
            return True


def CheckResponseString(msg):
    if msg.content in botoptions.eli_responses:
        return botoptions.eli_responses.get(msg.content, "looks like this doesn't exist")
    else:
        return ''


def TwitchLive():
    """Checks to see if the twitch channel is live"""
    twitchURL = ('https://api.twitch.tv/kraken/streams/elimere')
    headers = {
        'Client-ID': config.twitchBotId,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8'}
    request_ = urllib.request.Request(twitchURL, None, headers)
    response = urllib.request.urlopen(request_, None, 15)
    stream_info = response.read().decode('utf-8')
    json_info = json.loads(stream_info)
    if json_info['stream'] is None:
        return False
    else:
        return True


def CheckForLogs():
    """This checks the warcraft logs site for new logs"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8'}
    apiKey = config.warcraftLogsAPI
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us?api_key="+apiKey
    request_ = urllib.request.Request(url, None, headers)
    response_ = urllib.request.urlopen(request_, None, 15)
    log_info = response_.read().decode('utf-8')
    json_info = json.loads(log_info)
    f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/LastWarcraftLog.txt", 'r')
    logId = f.readline().strip('/n')
    f.close()
    if json_info[len(json_info)-1]['id'] != logId:
        f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/LastWarcraftLog.txt", 'w')
        f.write(json_info[len(json_info)-1]['id'])
        return "https://www.warcraftlogs.com/reports/" + json_info[len(json_info) - 1]['id']
    else:
        return ""

