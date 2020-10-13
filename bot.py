# Libs
import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os
import random

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('-')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Defining a few things
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=271612318947868673)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = '6'

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, my names {bot.user.name}.\nUse - to interact with me!")) # This changes the bots 'activity'

@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

@client.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount=15):
	await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
	await ctx.send(member.name + " Been Kicked from the server for:"+reason)
	await member.kick(reason = reason)


@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

@client.command(aliases=['user', 'info',])
async def whois(ctx, member : discord.Member):
     embed = discord.Embed(title = member.name, description = member.mention , color = discord.Color.blue())
     embed.add_field(name = "ID", value = member.id, inline = True )
     embed.set_thumbnail(url = member.avatar_url)
     await ctx.send(embed=embed)
     
     
@client.command()
async def say(ctx, *, arg):
    await ctx.send(arg)



#The below code bans player.
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
	await ctx.send(member.name + " Has Been banned from the server for:"+reason)
	await member.ban(reason = reason)


#The below code unbans player.
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command()
@commands.has_permissions(administrator = True)
async def poll(ctx, *,message):
     pemb=discord.Embed(title="Poll!", description=f"{message}")
     msg=await ctx.channel.send(embed=pemb)
     await msg.add_reaction('👍')
     await msg.add_reaction('👎')


@client.command(aliases=['m'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx,member : discord.Member):
       muted_role = ctx.guild.get_role(Muted)
       
       await member.add_roles(muted_role)
       
       await ctx.send(member.mention + " has been muted!")


@client.command(aliases=['unm'])
@commands.has_permissions(manage_roles=True)
async def unmute(ctx,member : discord.Member):
       muted_role = ctx.guild.get_role("Muted")
       
       await member.remove_roles(muted_role)
       
       await ctx.send(member.mention + " has been unmuted!")


@client.command(aliases=['h'])
async def help(ctx):
	hemb=discord.Embed(title="Help!", description="All Vyra's help commands 😁",
 color=0xffffff)
	await ctx.send(embed=hemb)

	

@client.command()
@commands.has_permissions(view_audit_log=True)
async def announce(ctx, *, arg):
    await ctx.send(arg)

    
    
    
    #A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    #Whenever the bot is tagged, respond with its prefix
    if f"<@!{bot.user.id}>" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '-'
        prefixMsg = await message.channel.send(f"My prefix here is `{prefix}`")
        await prefixMsg.add_reaction('👀')

    await bot.process_commands(message)

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
