import discord
from discord.ext import commands
from random import randint as r


class Komutlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def zar(self,ctx):
        await ctx.send(r(0, 6))

# Activiity = discord.Game(name = text)

    @commands.command()
    @commands.has_any_role('Admin','Developer','CEO')
    async def change_status(self, ctx, activity,*, text,url = ''):
        self.bind_text(text,url)
        await self.bot.change_presence(**self.activities.get(activity))
    
    def bind_text(self, text, url=''):
        self.activities = {
            "1":{'activity': discord.Game(name=text)},
            "2":{'activity': discord.Activity(Type=discord.ActivityType.listening, name=text)},
            "3":{'activity': discord.Activity(Type=discord.ActivityType.watching, name=text)},
            "4":{'activity': discord.Streaming(name=text, url=url)}
        }

def setup(bot):
    bot.add_cog(Komutlar(bot))
