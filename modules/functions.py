import botoptions, asyncio, config, os, aiohttp
import datetime
import modules.database as db

# This is the main directory of the bot
# This is especially needed if it's running as a background task
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def CheckForString(msg):
    """Checks the message to see if it matches the hey eli strings"""
    for string in botoptions.hey_eli:  # For each string in hey_eli list
        if msg.content.lower().rfind(string) != -1:  # If it is found, return True
            return True


async def CheckResponseString(dict, msg):
    """This checks a dictionary of strings and returns appropriately"""
    for response in dict.keys():  # This looks at all the keys in the dictionary
        if msg.content.lower().rfind(response) != -1:  # If the key is found
            return dict.get(response)  # Return the value of the key
    return ''  # Else return and empty string


async def TwitchLive():
    """Checks to see if the twitch channel is live"""
    twitchURL = 'https://api.twitch.tv/kraken/streams/elimere'
    headers = {'Client-ID': config.twitchBotId}  # This is needed to access the twitch api
    async with aiohttp.ClientSession() as session:  # Open a new session
        async with session.get(twitchURL, headers=headers) as resp:  # Pull the response
            json_info = await resp.json()  # Put the response into json format and store it
            await asyncio.sleep(0.250)  # Wait to close the session
            session.close()  # Close the session
    if json_info['stream'] is None:  # If the stream value is None, return False, else return True
        return False
    else:
        return True


async def RetrieveTwitchClip(channel):
    """Retrieves the newest twitch clip from the channel"""
    # Docs located here https://dev.twitch.tv/docs/v5/reference/clips
    twitchURL = 'https://api.twitch.tv/kraken/clips/top'
    headers = {
        'Client-ID': config.twitchBotId,
        'Accept': 'application/vnd.twitchtv.v5+json'
    }
    params = {
        'channel': channel,
        'period': 'all',
        'limit': '1'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(twitchURL, headers=headers, params=params) as resp:
            json_info = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    return json_info['clips'][0]['url']


async def CheckForLogs():
    """This checks the WarcraftLogs site for new logs"""
    params = {'api_key': config.warcraftLogsAPI}  # Needed to access the WarcraftLogs api
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us?"  # This is the URL to pull logs
    async with aiohttp.ClientSession() as session:  # Start a new session
        async with session.get(url, params=params) as resp:  # Get the response
            log_info = await resp.json()  # Store json information
            await asyncio.sleep(0.250)  # Wait to close
            session.close()  # Close
    log = log_info[len(log_info)-1]
    date = datetime.datetime.fromtimestamp(log['start'] / 1e3)
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    database = db.Database()
    log_exists = await database.check_log_by_id(log['id'])
    if log_exists:
        return None
    else:
        await database.insert_log_data(log['id'], date, log['title'], log['zone'])
        await database.close()
        return log


async def PullIOStats(realm, char_name):
    """This pulls stats from raiderio"""
    params = {'region': 'us', 'realm': realm, 'name': char_name, 'fields': 'mythic_plus_ranks'}
    url = 'https://raider.io/api/v1/characters/profile?'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            log = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    # print(log)
    return log
