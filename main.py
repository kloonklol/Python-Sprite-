#IMPORTS
import os
import discord
from discord.ext import commands, tasks
import random
import asyncio
from itertools import cycle
from keep_alive import keep_alive
import traceback, sys, math, time, datetime
import aiohttp
import json
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import numpy as np
import gc
from datetime import datetime


#PREFIX


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]




bot=commands.Bot(command_prefix=(get_prefix))


bot.remove_command('help')
@bot.event
async def on_guild_join(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = 's?!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)
		
		
@bot.command(pass_context=True, name="prefix")
@has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix has changed to: **{prefix}**')
		
		
		

#VARIABLE
lol = random.randrange(101)

coloremb = random.randint(0, 0xFFFFFF)

memem = cycle(['Dankmemes', 'philippines', 'memes'])

status = cycle(['with my baby', 'with tipen', 'Mobile Legends'])


#GIF - PAGES


punch_name = ['Agoi', '/kill @e', 'Wapaww!', 'Dead']

punch_gif = [
'https://c.tenor.com/SwMgGqBirvcAAAAM/saki-saki-kanojo-mo-kanojo.gif',
'https://c.tenor.com/xWqmJMePsqEAAAAM/weaboo-otaku.gif',
    'https://c.tenor.com/EdV_frZ4e_QAAAAM/anime-naruto.gif',
    'https://c.tenor.com/6a42QlkVsCEAAAAM/anime-punch.gif',
    'https://c.tenor.com/n7LKoJVrwM8AAAAM/anime-punch.gif',
    'https://c.tenor.com/dLaisLGeL1cAAAAM/shy-punch.gif']

#PAGE - HELP

page1 = discord.Embed(
    title="Help Command",
    description="Use the buttons below to navigate between help pages.",
    colour=discord.Colour.orange())
page3 = discord.Embed(
    title="Category - General",
    description="**Ping** - Shows bot latency.\n**Help** - Shows this command",
    colour=discord.Colour.orange())
page2 = discord.Embed(
    title="Category - Fun",
    description=
    "**Bayot** - Bayot machine\n**Meme** - Shows a meme from reddit\n**Punch** - Punches mentioned user",
    colour=discord.Colour.orange())
page4 = discord.Embed(
    title="Category - Miscellaneous",
    description=
    "**Purge** - Delete(s) messages\n**Info** - Information about this server\n**Bot** - Information about Me\n**Prefix** - Changes server prefix",
    colour=discord.Colour.orange())
bot.help_pages = [page1, page2, page3, page4]

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

#BOT - EVENT ON START

@tasks.loop(seconds=20)
async def status_swap():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_ready():
    status_swap.start()
    print(f'{bot.user} has connected to Discord!')

################################################
####################COMMANDS####################
################################################
	

#BAYOT COMMAND


@bot.command(pass_context=True, name="bayot", aliases=('agoi', 'Agoi'))
async def agoi(ctx):
    embed = discord.Embed(
        title="B4yot rate machine",
        description=f"You are {random.randrange(101)}% bayot",
        color=coloremb)
    await ctx.send(embed=embed)


#CLEAN COMMAND


@bot.command(pass_context=True, name='purge', aliases=('Clean', 'clean'))
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send('Cleared by {}\nClearead {int} message(s)'.format(ctx.author.mention))
    await ctx.message.delete()

	
#PING COMMAND


@bot.command(name='ping', aliases=['Ping', 'latency'])
async def ping(ctx):
    embed = discord.Embed(
        title="ðŸ“ Pong!",
        description=f"The bot latency is {round(bot.latency*1000)}ms.",
        color=0x42F56C)
    await ctx.send(embed=embed)

	
#MEME COMMAND


@bot.command(pass_context=True, name='meme')
async def meme(ctx):
    embed = discord.Embed(title="Meme", description="Funni meme")
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                f'https://reddit.com/r/{next(memem)}/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            embed.set_footer(text=f'Requested by {ctx.message.author.name}')
            await ctx.send(embed=embed)


#PUNCH COMMAND


@bot.command(pass_context=True, name="punch")
async def punch(ctx, member: discord.Member):
    embed = discord.Embed(
        title=f"{random.choice(punch_name)}",
        description="**{1}** Punched **{0}**! Ouch that hurt!".format(
            member.name, ctx.message.author.name))
    embed.set_image(url=f"{random.choice(punch_gif)}")
    await ctx.send(embed=embed)


#HELP COMMAND


@bot.command(name='server', aliases=('info', 'Info'))
@commands.guild_only()
async def serverinfo(ctx):
    embed = discord.Embed(color=coloremb)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url=str(ctx.guild.icon_url))
    embed.add_field(
        name=f"Information About **{ctx.guild.name}**: ",
        value=
        f"â€¢  ID: **{ctx.guild.id}** \nâ€¢  Owner: **{ctx.guild.owner}** \nâ€¢  Reigion: **{ctx.guild.region}** \nâ€¢  Creation: **{ctx.guild.created_at.strftime(format)}** \nâ€¢  Members: **{ctx.guild.member_count}** \nâ€¢  Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \nâ€¢  Verification: **{str(ctx.guild.verification_level).upper()}**"
    )
    await ctx.send(embed=embed)



#PAGE - HELP

@bot.command(name='help')
async def help(ctx):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1",
               u"\u23E9"]
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])
    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == ctx.author and reaction.
                emoji in buttons,
                timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages) - 1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages) - 1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])


#ERRORS

#PUNCH ERROR

@punch.error
async def punch_err(error, ctx):
    if isinstance(error, commands.RequiredMissingArgument):
        await ctx.send('Please Mention a user to do this')

bot.launch_time = datetime.utcnow()

@bot.command(name='bot', aliases=('bot_info', 'Bot'))
async def bot_info(ctx):
  delta_uptime = datetime.utcnow() -bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  embed = discord.Embed(title='Bot Info', description=f'**Information for <@949154804645625896>** \n**Program** - Python \n**Bot Owner** - Mini#4140\n**Uptime** - {days}d, {hours}h, {minutes}m, {seconds}s\n**Prefix** - s?',  color=coloremb)
  await ctx.send(embed=embed)

#CLEAN ERROR

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

#Memory Cleaner


a = np.array([discord,bot])
del a
gc.collect()



		

#START BOT
os.system('clear')
print('Terminal cleaned ready to go!\n.\n.\n.')

my_secret = os.environ['DISCORD_BOT_SECRET']
keep_alive()
bot.run(my_secret)
