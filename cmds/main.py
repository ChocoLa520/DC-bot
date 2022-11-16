import nextcord
from nextcord.ext import commands
import sys
sys.path.insert(0, 'C:/WorkPlace/Python WorkPlace/selfbot')
from core.classes import Cog_Extension 

class main(Cog_Extension):

	@commands.command(help="Close the Bot")
	async def close(self, ctx):
		await self.client.close()

def setup(client):
	client.add_cog(main(client))