import botoptions, asyncio, config, os, aiohttp


async def CallGit():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:
            print(resp.status)
            session.close()
            print(session.closed)


async def CheckForString(msg):
    """Checks the message to see if it matches the hey eli strings"""
    for string in botoptions.hey_eli:
        if msg.content.lower().rfind(string) != -1:
            return True


async def CheckResponseString(msg):
    if msg.content in botoptions.eli_responses:
        return botoptions.eli_responses.get(msg.content, "looks like this doesn't exist")
    else:
        return ''


async def TwitchLive():
    """Checks to see if the twitch channel is live"""
    twitchURL = ('https://api.twitch.tv/kraken/streams/elimere')
    headers = {'Client-ID': config.twitchBotId}
    async with aiohttp.ClientSession() as session:
        async with session.get(twitchURL, headers=headers) as resp:
            json_info = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    if json_info['stream'] is None:
        return False
    else:
        return True


async def CheckForLogs():
    """This checks the warcraftlogs site for new logs"""
    params = {'api_key': config.warcraftLogsAPI}
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us"
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
