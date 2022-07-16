import discord
import os
import calendar
import random
import aiohttp
import asyncio
import json
import random
import datetime

from itertools import cycle
from discord import Member
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()  
intents.members = True  # not really recomended (as far as i remember)
client = commands.Bot(command_prefix="./", intents=intents) # use "bot"

@client.event
async def on_ready():
  print(f"{client.user.name} running..\nDeployment Time:{datetime.datetime.utcnow()}")

@tasks.loop(seconds=20)
async def change_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"to {len(client.users)} members")) # fun stuff

@client.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  e = discord.Embed(description=f"{member.name}#{member.discriminator} was kicked", timestamp=ctx.message.created_at)
  e.set_footer(text=f"By {ctx.author}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=e)
                               
@kick.error
async def kick_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await bot.send_message(ctx.message.channel, # Not sure if python supports this
                               f"Sorry {ctx.message.author}, you do not have permissions to do that!")


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  e = discord.Embed(description=f"{member.name}#{member.discriminator} was banned.", timestamp=ctx.message.created_at) #banned no?
  e.set_footer(text=f"By {ctx.author}", icon_url = ctx.author.avatar_url)
  await ctx.send(embed=e)

@client.command()
@commands.has_permissions(administrator=True) # ban_members no? (would use a mod role type system for this)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      e = discord.Embed(description=f"{member.name}#{member.discriminator} was unbanned.", timestamp=ctx.message.created_at)
      e.set_footer(text=f"By {ctx.author}", icon_url=ctx.author_avatar_url
      )
      await ctx.send(embed=e)


@client.command() # Naming inconsistency why?
async def today(ctx):
 
  e=discord.Embed(title="Today's Info", description=f"Today is {day}, {date}.", color=0x1f8b4c, timestamp=ctx.message.created_at)
  e.set_author(name=(f"Requested by {ctx.author.display_name}"), 
  icon_url=ctx.author.avatar_url)
  e.set_thumbnail(url="https://www.pngitem.com/pimgs/m/521-5216516_nap-calendar-iconwebsite-calendar-png-cartoon-transparent-png.png")
  #png probably will go extinct some day
  e.set_footer(text='\u200b')
  await ctx.send(embed=e)

@client.command() # Naming inconsistency why? pt2
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    e=discord.Embed(title=f"{member.display_name}'s Avatar", color=0x1f8b4c, timestamp=ctx.message.created_at)
    e.set_author(name=(f"Requested by {ctx.author.display_name}"), icon_url=ctx.author.avatar_url)
    e.set_image(url=member.avatar_url)
    e.set_footer(text='\u200b')
    await ctx.send(embed=e)

@client.command(name="8ball", help="Ask a Yes/No Question.") # Naming inconsistency why? pt3
#There are like ~20 responses
async def _8ball(ctx, *, question): # Function naming inconsistency why? pt3
  outcomeP = ["It is certain.", "It is decidedly so", "Without a doubt", "Yes definitely.", "You may rely on it.", "Yes.", "As I see it yes.",
              "Outlook good", "Most Likely", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
              "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", 
              "Outlook not so good.", "Very doubtful."]
  e=discord.Embed(title=f"🎱 Magic 8Ball", description=f"{ctx.member.name}: {question}\n8Ball: {random.choice(outcomeP)}", color=0x1f8b4c)
  await ctx.reply(embed=e, mention_author=False)


@client.command() # Naming inconsistency why? pt4
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

    e = discord.Embed(
        title=f"{name} Server Information",
        description=description,
        color=discord.Color(0x1f8b4c), timestamp=ctx.message.created_at
    ) # good stuff :)
    e.set_thumbnail(url=icon)
    e.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    e.set_footer(text='\u200b')
    e.add_field(name="Owner", value=owner)
    e.add_field(name="Server ID", value=id)
    e.add_field(name="Member Count", value=memberCount)
    e.add_field(name="Text Channels", value=text_channels)
    e.add_field(name="Voice Channels", value=voice_channels)
    e.add_field(name="Roles Count", value=roles)
    await ctx.send(embed=e)

@client.command() # Naming inconsistency why? pt5
async def userinfo(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author

    e=discord.Embed(title=f"User's Information", color=member.color, timestamp=ctx.message.created_at)
    e.set_author(name=(f"Requested by {ctx.author.display_name}"), icon_url=ctx.author.avatar_url)
    e.set_thumbnail(url = member.avatar_url)
    e.set_footer(text='\u200b')

    e.add_field(name="Name", value=member.display_name)
    e.add_field(name="ID", value=member.id)
    e.add_field(name="Account created at", value=member.created_at)
    e.add_field(name="Server Joined at", value=member.joined_at)
    e.add_field(name="Bot", value=member.bot)
    await ctx.send(embed=e)
  
@client.command(pass_context=True)
async def meme(ctx):
    e = discord.Embed(title="", description="")
    try:
      async with aiohttp.ClientSession() as cs:
          async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r: #?? use other APIs
              res = await r.json()
              embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
              await ctx.send(embed=embed)
    except:
      await ctx.send("error")

@client.command(aliases=["bal"])
async def balance(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author


  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  embed = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.green())
  embed.add_field(name = "Wallet balance", value = wallet_amt)
  embed.add_field(name = "Bank", value = bank_amt)
  await ctx.send(embed = embed)

@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.CommandOnCooldown):
    msg  = "Hey there Cool down. Dont be notkool."
    await ctx.send(msg)

@client.command()
@commands.cooldown(2,30,commands.BucketType.user)
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earnings = random.randrange(101)

  await ctx.send(f"Someone gave you {earnings} coins!") 

  users[str(user.id)]["wallet"]+=earnings

  with open("balance.json","w") as f:
    json.dump(users,f)


async def open_account(user):

  users = await get_bank_data()
  
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0

  with open("balance.json", "w") as f:
    json.dump(users, f)
  return True

async def get_bank_data():
  with open("balance.json", "r") as f:
    users = json.load(f)

  return users


client.run("OTM3NjYyMTUwMDQ0OTUwNTk5.Yfe_7Q.mh_11ZLvw35SY7ENlTubfT8Pga4")
