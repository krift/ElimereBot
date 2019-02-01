from datetime import datetime
import feedparser
import botoptions
import discord
from modules.models.models import GeneralBotOptions, Discord


class Wowhead:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def ensure_option_exists():
        """Check the database for stored options. Seed if they don't exist."""
        value = None
        try:
            value = GeneralBotOptions.get(GeneralBotOptions.name == "wowhead_date")
        except Exception:
            pass
        if value is not None:
            return
        else:
            parser = feedparser.parse("https://www.wowhead.com/news&rss")
            GeneralBotOptions.create(name="wowhead_date", value=parser['entries'][0].published)

    async def grab_new_articles(self):
        articles = []
        parser = feedparser.parse("https://www.wowhead.com/news&rss")
        stored = GeneralBotOptions.get(GeneralBotOptions.name == "wowhead_date")
        stored = stored.value
        for x in parser['entries']:  # Start at the bottom of the list and work up
            if self.check_date(stored, x.published) is True:
                break
            elif self.check_for_keyword(x.title):
                articles.append(x)
        update = GeneralBotOptions.get(GeneralBotOptions.name == "wowhead_date")
        update.value = parser['entries'][0].published
        update.save()
        return articles

    @staticmethod
    def create_summary(value):
        return value[0:int(len(value) / 2)].replace('<p>', ' ').replace('<br>', ' ') + '...'  # Removes html code and reduces the length of the summary

    @staticmethod
    def check_for_keyword(title):
        for word in botoptions.keywords:
            if word in title.lower():  # Format title so the string is all lowercase.
                return True
        return False

    @staticmethod
    def check_date(stored, new):
        if stored.rfind(new) != -1:  # The stored date is the same as the new date
            return True
        else:
            return False

    async def post_new_article(self, server_id):
        discord_server = Discord.select().where(Discord.server_id == server_id)
        if len(discord_server) == 0:
            return
        if discord_server[0].wowhead_channel_id is None:
            return
        articles = await self.grab_new_articles()
        channel = self.bot.get_guild(int(server_id)).get_channel(int(discord_server[0].wowhead_channel_id))
        for x in articles:
            e = discord.Embed(title=x.title, colour=discord.Colour.purple())
            e.add_field(name='Summary', value=self.create_summary(x.summary))
            e.url = x.link
            e.timestamp = datetime.strptime(x.published, '%a, %d %b %Y %X %z')
            e.set_thumbnail(url='https://wow.zamimg.com/images/logos/wh-logo.png')
            await channel.send(embed=e)
