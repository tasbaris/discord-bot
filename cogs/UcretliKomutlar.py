import discord
from discord.ext import commands
import random

class UcretliKomutlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities={}

    @commands.command()
    @commands.has_role("CEO")
    async def Selamss(self, ctx):
        await ctx.send("CEO giriş yaptı! Dikkat!")
    
    @commands.command()
    @commands.has_role('Çekilişçi')
    async def cekilis(self,ctx):
        await ctx.send(f'Kazanan kullanıcı :tada: {(random.choice(self.bot.guilds[0].members).mention)} :tada: ')


def setup(bot):
    bot.add_cog(UcretliKomutlar(bot))
