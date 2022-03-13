import asyncio
import datetime
import json
import os
import random
import sys
import time as t

import discord
import motor.motor_asyncio
import requests
from discord.ext import commands
from button import *
import aiohttp

intents = discord.Intents.all()

start_time = t.time()
key = os.environ['MONGOKEY']
cluster = motor.motor_asyncio.AsyncIOMotorClient(key)


def get_prefix(client, message) -> str:
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    except:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(message.author.guild.id)] = ';'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=(get_prefix), case_insensitive=True, intents=intents)
client.remove_command('help')
tree = discord.app_commands.CommandTree(client)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_guild_join(guild) -> None:
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ';'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild) -> None:
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_command_error(ctx, error) -> None:
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(str(error))
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"**Error:** {error}", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        with open("runtime_errors.txt", "a") as f:
            f.write(t.strftime("%m/%d/%Y, %I:%M") + " || " + str(error) + "\n")


@client.event
async def on_ready() -> None:
    print(f'My name is {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my server"))
    await tree.sync(guild=discord.Object(id=920490332876046336))


# Bot Commands
@client.command()
async def hello(ctx) -> None:
    hello = [f"Yo Fam how ya do {ctx.author.mention}", "k", "...", "sup nerd", "ㅤ"]
    await ctx.send(random.choice(hello))


@client.command()
async def invite(ctx) -> None:
    embed = discord.Embed(title="Bot Invite Link",
                          url="https://discord.com/api/oauth2/authorize?client_id=919279296412020756&permissions=8"
                              "&scope=applications.commands%20bot",
                          description="https://discord.com/api/oauth2/authorize?client_id=919279296412020756"
                                      "&permissions=8&scope=applications.commands%20bot",
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.group(name='help', invoke_without_command=True)
async def help(ctx) -> None:
    embed = discord.Embed(title="Commands List", color=discord.Color.blue())
    embed.set_footer(text="This bot was made by Moondark876.")
    for cog, cls in client.cogs.items():
        cmds = "\n".join([cmd.name for cmd in cls.get_commands()])
        embed.add_field(name=cog, value=f'*{cls.__doc__}*\n>>> {cmds}', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def time(ctx) -> None:
    current_time = datetime.datetime.now()
    if current_time.strftime("%H") <= "12":
        am_pm = "AM"
    else:
        am_pm = "PM"
    embed = discord.Embed(title="The Time Is:", description=f'`{t.strftime("%m/%d/%Y, %I:%M")} {am_pm}`',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


@tree.command()
async def rolldice(interaction) -> None:
    """Returns a random number from one to six!"""
    dice = random.randint(1, 6)
    embed = discord.Embed(title=f'You rolled a {dice}!',
                          color=discord.Colour.blue() if dice > 3 else discord.Colour.red())
    if dice == 1:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356608809271387/dice1.png')
    elif dice == 2:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356609237074031/dice2.png')
    elif dice == 3:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356609660694598/dice3.png')
    elif dice == 4:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356609899757568/dice4.png')
    elif dice == 5:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356610285658122/dice5.png')
    elif dice == 6:
        embed.set_image(url='https://cdn.discordapp.com/attachments/778342545431855155/920356610650554418/dice6.png')
    await interaction.response.send(embed=embed)


@tree.command(guild=discord.Object(id=920490332876046336))
async def ping(interaction) -> None:
    """Get the bot's Latency and Uptime!"""
    current_time = t.time()
    difference = int(round(current_time - start_time))
    text = f"`{str(datetime.timedelta(seconds=difference)).split(':')[0]}hrs`"
    embed = discord.Embed(title='🏓 Pong! 🏓', color=discord.Color.blue())
    embed.add_field(name="Latency", value=f"`{round(client.latency * 1000)}ms`")
    embed.add_field(name='Uptime', value=text)
    try:
        await interaction.response.send_message(embed=embed)
    except discord.HTTPException:
        pass


tree.add_command(ping)


@client.command()
async def math(ctx, num1: float, operand, num2: float) -> None:
    if operand == '*':
        await ctx.send(f"Result: `{num1 * num2}`")

    elif operand == '/':
        await ctx.send(f"Result: `{num1 / num2}`")

    elif operand == '+':
        await ctx.send(f"Result: `{num1 + num2}`")

    elif operand == '-':
        await ctx.send(f"Result: `{num1 - num2}`")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix) -> None:
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: ```{prefix}```')


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None) -> None:
    if member.id != "748609140896694394":
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned from the server.")
    else:
        await ctx.send("Please think this over")


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member) -> None:
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}.')
            return


@client.command()
async def sadge(ctx) -> None:
    embed = discord.Embed(title='Sad', description=f'{ctx.author.name} is very sad :(', color=discord.Color.blue())
    await ctx.send(embed=embed)
    await ctx.message.delete()


@client.command()
async def laugh(ctx) -> None:
    await ctx.message.add_reaction("<:KEKW:936756232457449473>")


@client.command()
async def what(ctx) -> None:
    await ctx.message.add_reaction("<:youwhat:940030770645446706>")


@tree.command()
async def restart(interaction) -> None:
    if str(interaction.response.author.id) == "748609140896694394":
        msg = await interaction.response.send_message("Restarting Bot...", ephemeral=True)
        await asyncio.sleep(3)
        await msg.delete()
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        msg = await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        await asyncio.sleep(3)
        await msg.delete()


@client.command(aliases=['eval', 'execute', 'exec'])
async def evaluate(ctx, *, content) -> None:
    if str(ctx.author.id) == "748609140896694394":
        msg = await exec(content)
        await asyncio.sleep(5)
        await msg.delete()
    else:
        msg = await ctx.send("You don't have permission to use this command.")
        await asyncio.sleep(3)
        await msg.delete()


@client.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title=f"{ctx.author.name}'s Avatar",
                              url=str(ctx.author.display_avatar.url),
                              color=discord.Color.blue())
        # noinspection PyUnresolvedReferences
        embed.set_image(url=str(member.display_avatar.url))
    else:
        embed = discord.Embed(title=f"{member.name}'s Avatar",
                              url=str(member.display_avatar.url),
                              color=discord.Color.blue())
        embed.set_image(url=str(member.display_avatar.url))
    await ctx.send(embed=embed)


@client.command()
async def draw(ctx, *, description):
    image = requests.post("https://api.deepai.org/api/text2img", data={'text': str(description)},
                          headers={'api-key': 'a48622d2-38cb-40c2-a1d8-c5020b776914'})
    image_arr = json.loads(image.content)
    embed = discord.Embed(title=str(description.title()), url=image_arr['output_url'])
    embed.set_image(url=image_arr['output_url'])
    embed.set_footer(text="This image was created using the deepai api.")
    await ctx.reply(embed=embed, mention_author=False)


@client.command()
async def stats(ctx, member):
    response = requests.get(f"https://www.codewars.com/api/v1/users/{member}")
    stats = json.loads(response.content)
    print(stats)
    try:
        embed = discord.Embed(title=stats['username'], color=discord.Color.blue())
        embed.add_field(name="Rank",
                        value=f"""{stats['ranks']['overall']['name']}\n {stats['ranks']['overall']['score']}""")
        embed.add_field(name="Languages", value="".join([i + "\n" for i in stats['ranks']['languages'].keys()]))
        embed.add_field(name="Completed Katas", value=stats['codeChallenges']["totalCompleted"])
        await ctx.send(embed=embed)
    except:
        await ctx.send("Uh oh, something went wrong...")


@client.command()
async def kata(ctx, *, name):
    response = requests.get(f"https://www.codewars.com/api/v1/code-challenges/{name}")
    stats = json.loads(response.content)
    try:
        embed = discord.Embed(title=stats['name'], url=stats['url'], description=stats['description'],
                              color=discord.Color.blue())
        await ctx.send(embed=embed)
    except:
        await ctx.send("Uh oh, something went wrong...")


# Command Errors
@math.error
async def math_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error 404", description=f"Missing a required argument: `{error.param}`.")
        await ctx.send(embed=embed)

    elif isinstance(error, ZeroDivisionError):
        embed = discord.Embed(title="Error 404",
                              description="Either you multiplied a number by Zero or you are missing more than one argument.")
        await ctx.send(embed=embed)


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cannot change my prefix in a server you aren't an admin in.")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cannot ban members in a server you aren't an admin in.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("The member you have specified is unknown.")
    else:
        await ctx.send("A required argument is missing: `Member`.")


my_secret = os.environ['TOKEN']
client.run(my_secret)
