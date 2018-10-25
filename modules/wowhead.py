from datetime import datetime
import feedparser
import botoptions
import discord
import config


class Wowhead:
    def __init__(self, bot):
        self.bot = bot
        self.parser = feedparser.parse("https://www.wowhead.com/news&rss")
        self.bot.database.create_table('''CREATE TABLE IF NOT EXISTS options (option TEXT PRIMARY KEY unique, value TEXT)''')
        self.ensure_option_exists()

    def ensure_option_exists(self):
        """Check the database for stored options. Seed if they don't exist."""
        value = self.bot.event_loop.create_task(self.bot.database.read_table('''SELECT option FROM options WHERE option = ?''', 'wowhead_stored'))
        if value is True:
            return
        else:
            self.bot.event_loop.create_task(self.bot.database.insert_data('''INSERT INTO options (option, value) VALUES(?,?)''', botoptions.wowhead_initial_seed))

    async def grab_stored_date(self):
        return await self.bot.database.pull_data('''SELECT value FROM options WHERE option = ?''', 'wowhead_stored')

    async def grab_new_articles(self):
        articles = []
        stored = await self.grab_stored_date()
        stored = stored[0]
        for x in self.parser['entries']:  # Start at the bottom of the list and work up
            if self.check_date(stored, x.published) is True:
                break
            elif self.check_for_keyword(x.title):
                articles.append(x)
        await self.bot.database.update_data('''UPDATE options SET value = ? WHERE option = ?''', (self.parser['entries'][0].published, 'wowhead_stored',))
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

    async def post_new_article(self):
        articles = await self.grab_new_articles()
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildGenChanID)
        for x in articles:
            e = discord.Embed(title=x.title, colour=discord.Colour.purple())
            e.add_field(name='Summary', value=self.create_summary(x.summary))
            e.url = x.link
            e.timestamp = datetime.strptime(x.published,'%a, %d %b %Y %X %z')
            e.set_thumbnail(url='https://wow.zamimg.com/images/logos/wh-logo.png')
            await channel.send(embed=e)
