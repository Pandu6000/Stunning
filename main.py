import discord
import os
from datetime import date
import calendar
import random
from discord.ext import commands, tasks
import aiohttp
import asyncio
import json
from itertools import cycle

intents = discord.Intents.default()  
intents.members = True  
client = commands.Bot(command_prefix=".", intents=intents)
today = date.today()
date = today.strftime("%B %d, %Y")
day = calendar.day_name[today.weekday()]
status = cycle(["Stunning Things","Discord","Youtube","Netflix","Twitch","Tiktok","Chrome"])


@client.event
async def on_ready():
  change_status.start()
  await client.change_presence(status=discord.Status.idle)
  print("Bot is ready.")

@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  embed = discord.Embed(description=f"{member.name}#{member.discriminator} was kicked", timestamp=ctx.message.created_at)
  embed.set_footer(text=f"By {ctx.author}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  embed = discord.Embed(description = f"{member.name}#{member.discriminator} was kicked.", timestamp = ctx.message.created_at)
  embed.set_footer(text = f"By {ctx.author}", icon_url = ctx.author.avatar_url)
  await  ctx.send(embed=embed)

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      embed = discord.Embed(description=f"{member.name}#{member.discriminator} was unbanned.", timestamp=ctx.message.created_at)
      embed.set_footer(text=f"By {ctx.author}", icon_url=ctx.author_avatar_url
      )
      await ctx.send(embed=embed)


@client.command(name="today", help="See todya's Date.")
async def today(ctx):
 
  embed=discord.Embed(title="Today's Info", description=f"Today is {day}, {date}.", color=0x1f8b4c, timestamp=ctx.message.created_at)
  embed.set_author(name=(f"Requested by {ctx.author.display_name}"), 
  icon_url=ctx.author.avatar_url)
  embed.set_thumbnail(url="https://www.pngitem.com/pimgs/m/521-5216516_nap-calendar-iconwebsite-calendar-png-cartoon-transparent-png.png")
  embed.set_footer(text='\u200b')
  await ctx.send(embed=embed)

@client.command(name='avatar', help='Fetch avatar of a user.')
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    embed=discord.Embed(title=f"{member.display_name}'s Avatar", color=0x1f8b4c, timestamp=ctx.message.created_at)
    embed.set_author(name=(f"Requested by {ctx.author.display_name}"), icon_url=ctx.author.avatar_url)
    embed.set_image(url = userAvatar)
    embed.set_footer(text='\u200b')
    await ctx.send(embed=embed)

@client.command(name="8ball", help="Ask a Yes/No Question.")
async def _8ball(ctx, *, question):
  ball = [
"No - definitely",
"Yes – definitely",
"Yes - If sun would rise from west."
"Absolutely Not",
"An Absolute Yes"]
  embed=discord.Embed(title=f"🎱{question}", description=f"{random.choice(ball)}", color=0x1f8b4c)
  await ctx.reply(embed=embed, mention_author=False)


@client.command(name="serverinfo", help="Fetch server's info.")
@commands.guild_only()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner.display_name)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    roles = len(ctx.guild.roles)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=f"{name} Server Information",
        description=description,
        color=discord.Color(0x1f8b4c), timestamp=ctx.message.created_at
    )
    embed.set_thumbnail(url=icon)
    embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed.set_footer(text='\u200b')
    embed.add_field(name="Owner", value=owner)
    embed.add_field(name="Server ID", value=id)
    embed.add_field(name="Member Count", value=memberCount)
    embed.add_field(name="Text Channels", value=text_channels)
    embed.add_field(name="Voice Channels", value=voice_channels)
    embed.add_field(name="Roles Count", value=roles)
    await ctx.send(embed=embed)

@client.command(name='userinfo', help="Fetch user's info.")
async def userinfo(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author

    embed=discord.Embed(title=f"User's Information", color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=(f"Requested by {ctx.author.display_name}"), icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(text='\u200b')

    embed.add_field(name="Name", value=member.display_name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Account created at", value=member.created_at)
    embed.add_field(name="Server Joined at", value=member.joined_at)
    embed.add_field(name="Bot", value=member.bot)
    await ctx.send(embed=embed)
  
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


@client.event
async def on_message(message):
    if not message.author.bot:
        print('function load')
        with open('level.json','r') as f:
            users = json.load(f)
            print('file load')
        await update_data(users, message.author,message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author,message.channel, message.guild)

        with open('level.json','w') as f:
            json.dump(users, f)
    await client.process_commands(message)




async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))
  if str(user.guild.id) != '757383943116030074':
    if lvl_start < lvl_end:
      await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end


@client.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):

    if not member:
        user = ctx.message.author
        with open('level.json','r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
      with open('level.json','r') as f:
          users = json.load(f)
      lvl = users[str(ctx.guild.id)][str(member.id)]['level']
      exp = users[str(ctx.guild.id)][str(member.id)]['experience']
      embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP" ,color = discord.Color.green())
      embed.set_author(name = member, icon_url = member.avatar_url)

      await ctx.send(embed = embed)

client.run("OTM3NjYyMTUwMDQ0OTUwNTk5.Yfe_7Q.mh_11ZLvw35SY7ENlTubfT8Pga4")
