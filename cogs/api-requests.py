import discord
from discord.ext import commands
import aiohttp

from button import Next


class ApiRequests(commands.Cog):
    """Cluster of commands that reference an API to work."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ApiRequests Cog loaded.")

    @commands.command()
    async def cat(self, ctx):
        async def command_info():
            async with aiohttp.request('GET', 'https://api.thecatapi.com/v1/images/search') as response:
                cat_arr = await response.json()
            embed = discord.Embed(title="AWW")
            embed.set_image(url=cat_arr[0]["url"])
            return embed

        embed = await command_info()
        view = Next(command_info)
        await ctx.reply(embed=embed, mention_author=False, view=view)

    @commands.command()
    async def dog(self, ctx):
        async def command_info():
            async with aiohttp.request('GET', '') as response:
                dog_arr = await response.json()
            embed = discord.Embed(title="AWW")
            embed.set_image(url=dog_arr["message"])
            return embed

        embed = await command_info()
        view = Next(command_info)
        await ctx.reply(embed=embed, mention_author=False, view=view)


def setup(bot):
    bot.add_cog(ApiRequests(bot))
