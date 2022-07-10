from dis import dis
from http import client
from multiprocessing.connection import Client
from webbrowser import get
import discord
from discord.ext import commands, tasks
from utils import *
from functions import *
import time
import os


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="*",intents=intents)

class Social:
    INSTAGRAM = 'https://instagram.com'
    TWITTER = 'https://twitter.com'
    YOUTUBE = 'https://youtube.com'


all_social_media = {
    'INSTAGRAM': 'btsoftwareworld',
    'TWITTER': 'btsoftwareworld',
    'YOUTUBE': 'btsoftwareworld'
}

room = 0
@Bot.event
async def on_ready():
    #mustafakemalataturk.start()
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="*help"))
    print("Ben Hazırım")


@Bot.command()
async def setSocial(ctx, s, absolute_path):
    """ s must be twitter, instagram or youtube"""
    all_social_media[s] = absolute_path
    print(all_social_media)


@Bot.command()
async def socialpush(ctx, room:discord.TextChannel):
    global ROOM
    ROOM = room
    social_media_push.start()

@Bot.command
async def social_stop(ctx):
    social_media_push.stop()

@tasks.loop(seconds=10)
async def social_media_push():
    await ROOM.send(getSocials())

def getSocials() ->str:
    return f"""
    {Social.YOUTUBE}/{all_social_media.get('YOUTUBE')}
    {Social.TWITTER}/{all_social_media.get('TWITTER')}
    {Social.INSTAGRAM}/{all_social_media.get('INSTAGRAM')}
    """

@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="hos-geldiniz")
    await channel.send(f"{member.mention} aramıza katıldı. Hoş Geldi!")
    print(f"{member} aramıza katıldı. Hoş Geldi!")

@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="gule-gule")
    await channel.send(f"{member.mention} aramıza ayrıldı!")
    print(f"{member} aramıza ayrıldı!")


@Bot.command()
async def selam(ctx):
        await ctx.send("slm")


@Bot.command()
@commands.has_any_role('Admin','CEO','Developer')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} satır silindi!",delete_after = 2)

@Bot.command(aliases=["copy"])
@commands.has_any_role('Admin','CEO','Developer')
async def clone_channel(ctx, amount=1):
    for i in range(amount):
        await ctx.channel.clone()



@Bot.command()
@commands.has_any_role('Admin','CEO')
async def kick(ctx,member:discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)
    await ctx.send(f'{member.display_name} kicked!',delete_after = 2)

@Bot.command()
@commands.has_any_role('Admin','CEO')
async def ban(ctx,member:discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)
    dm(ctx,member,"Banlandınız")
    await ctx.send(f'{member.mention} Banned!', delete_after = 2)

@Bot.command()
@commands.has_any_role('Admin','CEO')
async def unban(ctx,*, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for bans in banned_users:
        user = bans.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned user {user.mention}",delete_after = 2)
            dm(ctx,user,"Banınız kaldırıldı!")
            return

@Bot.command()
@commands.has_any_role('Admin','CEO','Developer')
async def load(ctx, extension):
   Bot.load_extension(f'cogs.{extension}')
   print(f'{extension} eklentisi eklendi')
   await ctx.send(f'{extension} eklentisi eklendi!',delete_after = 2)



@Bot.command()
@commands.has_any_role('Admin','CEO','Developer')
async def unload(ctx, extension):
   Bot.unload_extension(f'cogs.{extension}')
   print(f'{extension} eklentisi kaldırıldı')
   await ctx.send(f'{extension} eklentisi Kaldırıldı!',delete_after = 2)


@Bot.command()
@commands.has_any_role('Admin','CEO','Developer')
async def reload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
    Bot.load_extension(f'cogs.{extension}')
    print(f'{extension} eklentisi yeniden yüklendi!')
    await ctx.send(f'{extension} yeniden Yüklendi!',delete_after = 2)

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        Bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename} eklentisi Eklendi')

@Bot.command()
async def dm(ctx,user:discord.User,text):
    user.send(text)

Bot.run(TOKEN)
