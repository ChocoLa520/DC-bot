import nextcord
from nextcord.ext import commands
import json
import sys
sys.path.insert(0, 'C:/WorkPlace/Python WorkPlace/selfbot')
from core.classes import Cog_Extension 

with open('setting.json', 'r', encoding='utf8') as jFile:
    jdata = json.load(jFile)

class events(Cog_Extension):
	
	@commands.Cog.listener()
	async def on_connect(self):
	    print("Bot connected!")

	@commands.Cog.listener()
	async def on_disconnect(self):
		print("Bot disconnected!")

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author == self.client.user:
			return
		if msg.author.id == 527502176789200927 or '<@527502176789200927>' in msg.content:
			emoji = await msg.guild.fetch_emoji(954787454693564437)
			await msg.add_reaction(emoji)

def setup(client):
	client.add_cog(events(client))