import nextcord
from nextcord.ext import commands
import json
import os

'''
with open('setting.json', 'r', encoding='utf8') as jFile:
    jdata = json.load(jFile)
'''
intents = nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="[",intents=intents)

@client.event
async def on_ready():
    print("login id:", client.user)
    game = nextcord.Game("哲瑋的覺覺")
    await client.change_presence(status=nextcord.Status.idle, activity=game)

@client.command()
async def load(ctx, extension):
    client.load_extension(F'cmds.{extension}')
    await ctx.send(F'Loaded {extension} done.')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(F'cmds.{extension}')
    await ctx.send(F'Un-Loaded {extension} done.')

@client.command()
async def reload(ctx, extension):
    client.reload_extension(F'cmds.{extension}')
    await ctx.send(F'Re-Loaded {extension} done.')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        client.load_extension(F'cmds.{filename[:-3]}')

if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
    #client.run(jdata['TOKEN'])