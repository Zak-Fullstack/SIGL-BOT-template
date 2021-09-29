from discord.utils import get

async def get_member(ctx, arg):
  member = get(ctx.guild.members, name = arg)
  if member == None and arg[3:-1].isnumeric():
    member = ctx.guild.get_member(int(arg[3:-1]))
  else:
    await ctx.send(arg + " User Not Found")
  return member