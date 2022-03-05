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
from button import Confirm


intents = discord.Intents.all()

start_time = t.time()
key = os.environ['MONGOKEY']
cluster = motor.motor_asyncio.AsyncIOMotorClient(key)


def get_prefix(client, message):
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


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ';'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(str(error))
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title=f"**Error:** {error}", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        with open("runtime_errors.txt", "a") as f:
            f.write(t.strftime("%m/%d/%Y, %I:%M") + " || " + str(error) + "\n")


@client.event
async def on_ready():
    print(f'My name is {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my server"))


# Bot Commands
@client.command()
async def hello(ctx):
    hello = [f"Yo Fam how ya do {ctx.author.mention}", "k", "...", "sup nerd", "ㅤ"]
    await ctx.send(random.choice(hello))


@client.command()
async def invite(ctx):
    embed = discord.Embed(title="Bot Invite Link",
                          url="https://discord.com/api/oauth2/authorize?client_id=919279296412020756&permissions=8&scope=bot",
                          description="https://discord.com/api/oauth2/authorize?client_id=919279296412020756&permissions=8&scope=bot",
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.group(name='help', invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Commands List", description=f"""```
  hello
  invite
  time
  math
  rolldice
  ping```""", color=discord.Color.blue())
    embed.set_footer(text="This bot was made by Moondark876.")
    await ctx.send(embed=embed)


@help.command()
async def hello(ctx):
    await ctx.send("```hello - sends a random hello message.```")


@help.command()
async def invite(ctx):
    await ctx.send(f"```invite - sends the invite link for the bot.```")


@client.command()
async def time(ctx):
    current_time = datetime.datetime.now()
    if current_time.strftime("%H") <= "12":
        am_pm = "AM"
    else:
        am_pm = "PM"
    embed = discord.Embed(title="The Time Is:", description=f'`{t.strftime("%m/%d/%Y, %I:%M")} {am_pm}`',
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def rolldice(ctx):
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
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    current_time = t.time()
    difference = int(round(current_time - start_time))
    text = f"`{str(datetime.timedelta(seconds=difference)).split(':')[0]}hrs`"
    embed = discord.Embed(title='🏓 Pong! 🏓', color=discord.Color.blue())
    embed.add_field(name="Latency", value=f"`{round(client.latency * 1000)}ms`")
    embed.add_field(name='Uptime', value=text)
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        pass


@client.command()
async def math(ctx, num1: float, operand, num2: float):
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
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: ```{prefix}```')


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.id != "748609140896694394":
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned from the server.")
    else:
        await ctx.send("Please think this over")


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}.')
            return


@client.command()
async def sadge(ctx):
    embed = discord.Embed(title='Sad', description=f'{ctx.author.name} is very sad :(', color=discord.Color.blue())
    await ctx.send(embed=embed)
    await ctx.message.delete()


@client.command()
async def laugh(ctx):
    await ctx.message.add_reaction("<:KEKW:936756232457449473>")


@client.command()
async def what(ctx):
    await ctx.message.add_reaction("<:youwhat:940030770645446706>")


@client.command()
async def restart(ctx):
    if str(ctx.author.id) == "748609140896694394":
        msg = await ctx.send("Restarting Bot...")
        await asyncio.sleep(3)
        await msg.delete()
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        msg = await ctx.send("You don't have permission to use this command.")
        await asyncio.sleep(3)
        await msg.delete()


@client.command(aliases=['eval', 'execute', 'exec'])
async def evaluate(ctx, *, content):
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
                              url=str(ctx.author.avatar_url),
                              color=discord.Color.blue())
        embed.set_image(url=str(ctx.author.avatar_url))
    else:
        embed = discord.Embed(title=f"{member.name}'s Avatar",
                              url=str(member.avatar_url),
                              color=discord.Color.blue())
        embed.set_image(url=str(member.avatar_url))
    await ctx.send(embed=embed)


@client.command()
async def cat(ctx):
    cats = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_arr = json.loads(cats.content)
    embed = discord.Embed(title="AWW")
    embed.set_image(url=cat_arr[0]["url"])
    button = discord.ui.Button(label='Next', style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        cats = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_arr = json.loads(cats.content)
        embed = discord.Embed(title="AWW")
        embed.set_image(url=cat_arr[0]["url"])
        await interaction.response.edit_message(embed=embed)

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)
    await ctx.reply(embed=embed, mention_author=False, view=view)


@client.command()
async def dog(ctx):
    dogs = requests.get("https://dog.ceo/api/breeds/image/random")
    dog_arr = json.loads(dogs.content)
    embed = discord.Embed(title="AWW")
    embed.set_image(url=dog_arr["message"])
    button = discord.ui.Button(label='Next', style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        dogs = requests.get("https://dog.ceo/api/breeds/image/random")
        dog_arr = json.loads(dogs.content)
        embed = discord.Embed(title="AWW")
        embed.set_image(url=dog_arr["message"])
        await interaction.response.edit_message(embed=embed)

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)
    await ctx.reply(embed=embed, mention_author=False, view=view)


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


# Trying economy again...sigh

async def open_account(user: discord.Member):
    try:
        post = {"_id": str(user.id), "Balance": 0}
        await cluster.Botswag.Accounts.insert_one(post)
    except:
        pass


@client.command(aliases=["bal"])
async def balance(ctx):
    await open_account(ctx.author)
    stats = await cluster.Botswag.Accounts.find_one({"_id": str(ctx.author.id)})
    embed = discord.Embed(description=f"You currently have ${stats['Balance']}.",
                          color=discord.Color.green())
    embed.set_author(name=f"{ctx.author.name.title()}'s Balance:", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command(aliases=['swaggy', 'swagger'])
@commands.cooldown(1, 30, commands.BucketType.user)
async def swag(ctx):
    await open_account(ctx.author)

    swagger = ["Your fans give you $* for being a swag master.",
               "You swagged so hard you forgot to breathe, and they paid you $* to stay alive.",
               "When you step into the building, everybody's hands go up and stay there, and you take the opportunity to rob them all of a collective $*."]
    money = random.randint(100, 500)

    await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)}, {"$inc": {"Balance": money}})
    embed = discord.Embed(description=random.choice(swagger).replace('*', str(money)),
                          color=discord.Color.green())
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                     icon_url='https://cdn.discordapp.com/avatars/748609140896694394/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
    await ctx.send(embed=embed)


@client.command(aliases=["lend", "send"])
async def give(ctx, user: discord.Member, amount):
    await open_account(ctx.author)
    await open_account(user)
    print(str(user.id))

    stats = await cluster.Botswag.Accounts.find_one({"_id": str(ctx.author.id)})

    if not amount.isnumeric() and amount.lower() not in ["all", 'half']:
        embed = discord.Embed(title="Invalid `amount` Argument Given",
                              description="Your `amount` argument is unrecognised.",
                              color=discord.Color.red())
        embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
        embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                         icon_url='https://cdn.discordapp.com/avatars/748609140896694394/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
        await ctx.send(embed=embed)
        return

    elif amount.isnumeric():
        if int(amount) > stats['Balance'] or int(amount) <= 0:
            embed = discord.Embed(title="Invalid `amount` Argument Given",
                                  description="Your `amount` argument is either above your balance, 0 or below 0.",
                                  color=discord.Color.red())
            embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
            embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                             icon_url='https://cdn.discordapp.com/avatars/748609140896694394/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
            await ctx.send(embed=embed)
            return
        else:
            amount = int(amount)
            await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)}, {"$inc": {"Balance": -amount}})
            await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})

    elif not amount.isnumeric():
        if amount.lower() == 'all':
            amount = stats['Balance']
            await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)}, {"$inc": {"Balance": -amount}})
            await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})
        elif amount.lower() == 'half':
            amount = stats['Balance'] // 2
            await cluster.Botswag.Accounts.update_one({"_id": str(ctx.author.id)}, {"$inc": {"Balance": -amount}})
            await cluster.Botswag.Accounts.update_one({"_id": str(user.id)}, {"$inc": {"Balance": amount}})

    embed = discord.Embed(title="Sharing is Caring",
                          description=f"You gave **{user.name}** ${amount}!",
                          color=discord.Color.green())
    embed.set_thumbnail(url="https://www.bing.com/images/blob?bcid=Tncj8lzDV-EDFPSHOUayPnCwk3lS.....3c")
    embed.set_footer(text="N.B. This command is under development. It may not work as expected",
                     icon_url='https://cdn.discordapp.com/avatars/748609140896694394/216c2e4a3ab7574609c049a7d3ebbdaa.webp?size=1024')
    await ctx.send(embed=embed)

# Command Errors
@swag.error
async def swag_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command On Cooldown", description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Color.red())
        await ctx.send(embed=em)


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
