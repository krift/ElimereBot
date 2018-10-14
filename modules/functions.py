import asyncio, config, aiohttp


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


async def PullIOStats(realm, char_name):
    """This pulls stats from raiderio"""
    params = {'region': 'us', 'realm': realm, 'name': char_name, 'fields': 'mythic_plus_ranks'}
    url = 'https://raider.io/api/v1/characters/profile?'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            info = await resp.json()
            await asyncio.sleep(0.250)
        params['fields'] = 'mythic_plus_scores'
        async with session.get(url, params=params) as resp:
            score = await resp.json()
            await asyncio.sleep(0.250)
            session.close()
    # Return the base info, the ranks, and the scores into a tuple
    return info, info['mythic_plus_ranks'], score['mythic_plus_scores']
