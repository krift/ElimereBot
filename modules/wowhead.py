from datetime import datetime
import feedparser
import botoptions
import modules.database as db
import discord
import config


class Wowhead:
    def __init__(self):
        self.parser = feedparser.parse("https://www.wowhead.com/news&rss")
        self.database = db.Database()
        self.database.create_table('''CREATE TABLE IF NOT EXISTS options (option TEXT PRIMARY KEY unique, value TEXT)''')

    async def grab_stored_date(self):
        return await self.database.pull_data('''SELECT value FROM options WHERE option = ?''', 'wowhead_stored')

    async def grab_new_articles(self):
        articles = []
        stored = await self.grab_stored_date()
        stored = stored[0]
        for x in self.parser['entries']:  # Start at the bottom of the list and work up
            if self.check_date(stored, x.published) is True:
                break
            elif self.check_for_keyword(x.title):
                articles.append(x)
        await self.database.update_data('''UPDATE options SET value = ? WHERE option = ?''', (self.parser['entries'][0].published, 'wowhead_stored',))
        return articles

    def create_summary(self, value):
        return value[0:int(len(value) / 2)].replace('<p>', ' ').replace('<br>', ' ') + '...'  # Removes html code and reduces the length of the summary

    def check_for_keyword(self, title):
        for word in botoptions.keywords:
            if word in title.lower():  # Format title so the string is all lowercase.
                return True
        return False

    def check_date(self, stored, new):
        if stored.rfind(new) != -1:  # The stored date is the same as the new date
            return True
        else:
            return False

    async def PostNewArticle(self, bot):
        articles = await self.grab_new_articles()
        channel = bot.get_guild(config.devServerID).get_channel(356544379885846552)
        for x in articles:
            e = discord.Embed(title=x.title, colour=discord.Colour.purple())
            e.add_field(name='Summary', value=self.create_summary(x.summary))
            e.url = x.link
            e.timestamp = datetime.strptime(x.published,'%a, %d %b %Y %X %z')
            e.set_thumbnail(url='https://wow.zamimg.com/images/logos/wh-logo.png')
            await channel.send(embed=e)
