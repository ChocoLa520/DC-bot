import nextcord
from nextcord.ext import commands
from youtube_dl import YoutubeDL
import sys
sys.path.insert(0, 'C:/WorkPlace/Python WorkPlace/selfbot')
from core.classes import Cog_Extension 

class music(commands.Cog):
    global s
    def __init__(self, client):
        self.client = client
    
        self.is_playing = False
        # 2d array [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title'], 'loop': False}

    def play_next(self):
        global s
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            if(self.music_queue[0][0]['loop'] == False):
                s=self.music.query[0][0]['title']
                self.music_queue.pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        global s
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            if(self.music_queue[0][0]['loop'] == False):
                s=self.music_queue[0][0]['title']
                self.music_queue.pop(0)
            
            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song")
            else:
                self.music_queue.append([song, voice_channel])

                em = nextcord.Embed(title=f":musical_note: ** {self.music_queue[-1][0]['title']} ** :musical_note:", colour=nextcord.Color.purple())
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=em)

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(help="Displays the current songs in queue")
    async def list(self, ctx):
        global s
        if len(self.music_queue) > 0:
            em = nextcord.Embed(title=f'Now ~ {s}\n\nQueue:', colour=nextcord.Color.gold())
            [em.add_field(name=self.music_queue[i][0]['title'] + '\nLoop = ' + str(self.music_queue[i][0]['loop']) + '\n', value="\u200b", inline=False) for i in range(0, len(self.music_queue))]
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            em = nextcord.Embed(title=f'Now ~ {s}\n\nQueue is empty!', colour=nextcord.Color.gold())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(help="Loop the songs")
    async def loop(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song")
            else:
                await ctx.send("Song added to the queue")
                song['loop'] = True
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()    

    @commands.command(help="Skips the current song being played")
    async def skip(self, ctx):
        if(len(self.music_queue) != 0 and self.music_queue[0][0]['loop']==True):
            self.music_queue.pop(0)
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music() 

    @commands.command(help="Disconnecting bot from DC")
    async def d(self, ctx):
        for i in range(0, len(self.music_queue)):
            self.music_queue.pop(0)
        await self.vc.disconnect()

def setup(client):
    client.add_cog(music(client))