import botoptions, asyncio, config, os, aiohttp


async def CheckForString(msg):
    """Checks the message to see if it matches the hey eli strings"""
    for string in botoptions.hey_eli:
        if msg.content.lower().rfind(string) != -1:
            return True


async def CheckResponseString(dict, msg):
    """This checks a dictionary of strings and returns appropriately"""
    for response in dict.keys():
        if msg.content.lower().rfind(response) != -1:
            return dict.get(response)
    return ''


async def TwitchLive():
    """Checks to see if the twitch channel is live"""
    twitchURL = 'https://api.twitch.tv/kraken/streams/elimere'
    headers = {'Client-ID': config.twitchBotId}  # This is needed to access the twitch api
    async with aiohttp.ClientSession() as session:
        async with session.get(twitchURL, headers=headers) as resp:
            json_info = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    if json_info['stream'] is None:
        return False
    else:
        return True


async def RetrieveTwitchClip():
    """Retrieves the newest twitch clip from the channel"""
    # https://dev.twitch.tv/docs/v5/reference/clips
    # Docs located here
    twitchURL = 'https://api.twitch.tv/kraken/clips/top?channel=elimere&period=all&limit=1'
    #twitchURL = 'https://api.twitch.tv/kraken/clips/top?channel=Twitch&period=month&trending=true&limit=1'
    headers = {'Client-ID': config.twitchBotId,
               'Accept': 'application/vnd.twitchtv.v5+json'}
    async with aiohttp.ClientSession() as session:
        async with session.get(twitchURL, headers=headers) as resp:
            json_info = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    print(json_info['clips'])
    print(json_info['clips'][0]['url'])
    return json_info['clips'][0]['url']

async def CheckForLogs():
    """This checks the WarcraftLogs site for new logs"""
    params = {'api_key': config.warcraftLogsAPI}  # Needed to access the WarcraftLogs api
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us?"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            log_info = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/LastWarcraftLog.txt", 'r')
    logID = f.readline().strip('/n')
    f.close()
    if log_info[len(log_info)-1]['id'] != logID:
        f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/LastWarcraftLog.txt", 'w')
        f.write(log_info[len(log_info)-1]['id'])
        return "https://www.warcraftlogs.com/reports/" + log_info[len(log_info) - 1]['id']
    else:
        return ""
