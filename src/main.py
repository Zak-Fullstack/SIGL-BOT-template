import os
from discord.ext import commands
from utils import get_member
import discord

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=discord.Intents().all()
)
server_id = 892819821039869983
guild = None

bot.author_id = 0000000  # Change to your discord id!!!

muted  = []

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


# @bot.event
# async def on_message(msg):
#     print()


# @bot.event
# async def on_name(msg):
#     print(msg)
#     if (msg == "!pong"):
#         await pong(bot.get_guild(server_id).get_channel(892819821476069419))

@bot.command()
async def pong(ctx):
    print(ctx)
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author)

@bot.command()
async def count(ctx):
    members = ctx.guild.members
    status_count = {
        "online": 0,
        "idle": 0,
        "offline": 0,
        "disturb": 0
    }
    print(members)
    for m in members:
        print(m.status)
        if str(m.status) == "online":
            status_count["online"] += 1
        elif str(m.status) == "offline":
            status_count["offline"] += 1
        elif str(m.status) == "idle":
            status_count["idle"] += 1
        else:
            status_count["disturb"] += 1

    await ctx.send('{} members are online, {} should not be disturbed, {} are idle, {} are offline'.format(status_count["online"], status_count["disturb"], status_count["idle"], status_count["offline"]))

@bot.command()
async def admin(ctx, arg):
    # add role to user given in argument
    member = await get_member(ctx, arg)
    if member == None:
        return

    # create role if does not exist
    role = discord.utils.get(ctx.guild.roles, name = "Admin")
    if role == None:
        role = await ctx.guild.create_role(name = "Admin", permissions=discord.Permissions(8))


    await member.add_roles(role)

@bot.command()
async def mute(ctx, arg):
    try:
        member = await get_member(ctx, arg)
        if member == None:
            return

        # Check if user is muted
        for m,r in muted:
            if m == member.id:
                print(*(member.roles[1:]))
                await member.remove_roles(*(member.roles[1:]))
                await member.add_roles(*r)
                return

        # create role if does not exist
        role = discord.utils.get(ctx.guild.roles, name = "Ghost")
        if role == None:
            role = await ctx.guild.create_role(name = "Ghost", permissions=discord.Permissions(send_messages=False))

        # add role to user given in argument

        muted.append((member.id, member.roles[1:]))
        print(*(member.roles[1:]))
        await member.remove_roles(*(member.roles[1:]))
        await member.add_roles(role)

    except e:
        msg = "Error: " + e
        ctx.send(msg)

@bot.command()
async def ban(ctx, arg):
    member = await get_member(ctx, arg)
    if member == None:
        return

    await ctx.guild.ban(member)

token = "ODkyODIxNzE1OTcxODY2NjU0.YVSfBA._u_qFrGBWqZVBj5vSlBdMg2xaoU"
bot.run(token)  # Starts the bot