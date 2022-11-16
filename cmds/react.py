import nextcord
from nextcord.ext import commands
import sys
import datetime

sys.path.insert(0, 'C:/WorkPlace/Python WorkPlace/selfbot')
from core.classes import Cog_Extension 
class react(Cog_Extension):

    @commands.command(help="Yummy")
    async def liang(self, ctx):
        embed=nextcord.Embed(title="Liang Liang Time", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description="A lot of liang liang is here.",
        color=0xe90707, timestamp=datetime.datetime.now())
        embed.set_author(name="Liang Bot", url="https://www.youtube.com/watch?v=K1PCl5D-IpU", icon_url="https://i.imgur.com/dmw92to.png")
        embed.set_thumbnail(url="https://i.imgur.com/z1LycAF.gif")
        embed.add_field(name="First", value="Just", inline=False)
        embed.add_field(name="Second", value="For", inline=False)
        embed.add_field(name="Third", value="Sleep", inline=False)
        embed.set_footer(text="Best Liang Liang TW")
        await ctx.send(embed=embed)

    @commands.command(help="No use")
    async def leo(self, ctx):
        await ctx.send("Leo is no use!")

    @commands.command(help="Update consistently")
    async def BBL(self, ctx):
        await ctx.send("BBL is in his 20 BOs now!")

def setup(client):
	client.add_cog(react(client))
