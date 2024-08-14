#Music Module
#Imports
import logs
import discord
import datetime
import numpy as np
import math
import requests
import os
import shutil
import mutagen
import asyncio
import Globals as g
import audioread
import subprocess
import yt_dlp as youtube_dl
import threading
import spotipy
from spotipy import SpotifyClientCredentials
from StringProgressBar import progressBar
import database as db
#/Imports
#Startup
logs.info("Music Module Started Successfully!")
enabled = True
queues = []
queueindex = 0
#Check if the module is running or not
def running():
    return True
def init(client: discord.Client):
    global Pl, Em
    logs.info("Initialising Music Module")
    queues.append(Player(client))
    Pl = queues[0]
    Em = embeds()
first = True
genericthumburl = "https://raw.githubusercontent.com/ItBePhill/Creme-Egg-Bot-ReWritten/main/Songs/Images/generic-thumb.png"
thumbsmall = "https://i.ytimg.com/vi/{_ID_}/default.jpg"
#/Startup

#Em


class embeds():
    def __init__(self):
        logs.info("Initialising embeds Class")
        self.volabel = None
        self.volumelabels = [
            ":black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :black_large_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :black_large_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :black_large_square: ",
            ":red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: :red_square: "
        ]
        self.ogmessage = None
        self.embed = None
        self.view = None
        self.total = 100
        self.started = None
    async def callback(self, i: discord.Interaction, x: str):
        await i.response.send_message(content =  "Thinking...", ephemeral=False)
        await i.delete_original_response()
        match x:
            case "sh":
                await ShuffleCommand(i)
            case "sk":
                await Pl.skip(i, Pl.client)
            case "p":
                if Pl.paused:
                    await Pl.resume()
                    view = discord.ui.View()
                    embed =  self.embed
                    shuffleButton = discord.ui.Button(emoji="🔀")
                    shuffleButton.callback=lambda i: self.callback(i, "sh")
                    pausePlayButton = discord.ui.Button(emoji="⏸️")
                    pausePlayButton.callback=lambda i: self.callback(i, "p")
                    restartButton = discord.ui.Button(emoji="🔁")
                    restartButton.callback=lambda i: self.callback(i, "r")
                    skipButton = discord.ui.Button(emoji="⏭️")
                    skipButton.callback=lambda i: self.callback(i, "sk")
                    stopButton = discord.ui.Button(emoji="⏹️")
                    stopButton.callback=lambda i: self.callback(i, "st")
                    volumeDownButton=discord.ui.Button(emoji="🔉")
                    volumeDownButton.callback = lambda i: self.callback(i, "vd")
                    volumeUpButton=discord.ui.Button(emoji="🔊")
                    volumeUpButton.callback=lambda i: self.callback(i, "vu")
                    # refreshButton = discord.ui.Button(emoji="🔃")
                    # refreshButton.callback=lambda i: self.callback(i, "rf")
                    view.add_item(shuffleButton)
                    view.add_item(pausePlayButton)
                    view.add_item(restartButton)
                    view.add_item(skipButton)
                    view.add_item(stopButton)
                    view.add_item(volumeUpButton)
                    view.add_item(volumeDownButton)
                    # if not self.started:
                    #     self.view.add_item(refreshButton)
                    await self.ogmessage.edit(view=view)
                else:
                    await Pl.pause()
                    view = discord.ui.View()
                    embed =  self.embed
                    shuffleButton = discord.ui.Button(emoji="🔀")
                    shuffleButton.callback=lambda i: self.callback(i, "sh")
                    pausePlayButton = discord.ui.Button(emoji="▶️")
                    pausePlayButton.callback=lambda i: self.callback(i, "p")
                    restartButton = discord.ui.Button(emoji="🔁")
                    restartButton.callback=lambda i: self.callback(i, "r")
                    skipButton = discord.ui.Button(emoji="⏭️")
                    skipButton.callback=lambda i: self.callback(i, "sk")
                    stopButton = discord.ui.Button(emoji="⏹️")
                    stopButton.callback=lambda i: self.callback(i, "st")
                    # refreshButton = discord.ui.Button(emoji="🔃")
                    # refreshButton.callback=lambda i: self.callback(i, "rf")
                    volumeDownButton=discord.ui.Button(emoji="🔉")
                    volumeDownButton.callback = lambda i: self.callback(i, "vd")
                    volumeUpButton=discord.ui.Button(emoji="🔊")
                    volumeUpButton.callback=lambda i: self.callback(i, "vu")
                    view.add_item(shuffleButton)
                    view.add_item(pausePlayButton)
                    view.add_item(restartButton)
                    view.add_item(skipButton)
                    view.add_item(stopButton)
                    view.add_item(volumeUpButton)
                    view.add_item(volumeDownButton)
                    # if not self.started:
                    #     self.view.add_item(refreshButton)
                    await self.ogmessage.edit(view=view)
            case "r":
                await Pl.restart(i, Pl.client)
            case "st":
                await Pl.stop()
            case "vu":
                await Pl.volume_up()
                embed = self.embed
                view = self.view
                embed.set_field_at(len(embed._fields) - 1, name= "Volume", value = self.volumelabels[Pl.volume], inline = False)
                await self.ogmessage.edit(embed=embed)
            case "vd":
                await Pl.volume_down()
                embed = self.embed
                view = self.view
                embed.set_field_at(len(embed._fields) - 1, name= "Volume", value = self.volumelabels[Pl.volume], inline = False)
                await self.ogmessage.edit(embed=embed)
            case "rf":
                embed = self.embed
                view = self.view
                # Assign values to total and current values
                current = (g.variables["timelapsed"] / Pl.queue[0]["dur"]) * 100
                # First two arguments are mandatory
                bardata = progressBar.splitBar(self.total, int(current), size = 9)
                embed.set_field_at(len(embed._fields) - 2, name = "Time Elapsed", value = f"{datetime.timedelta(seconds=g.variables['timelapsed'])}|{bardata[0]}|{datetime.timedelta(seconds=Pl.queue[0]['dur'])}", inline = False)
                await self.ogmessage.edit(embed=embed)

    #Create the "Playing" Embed, has a variation for Now Playing and Started Playing
    async def CreateEmbedPlaying(self, interaction: discord.Interaction, song: dict, started: bool):
        message = await interaction.channel.send(content = "Thinking...")
        await message.delete()
        self.started = started
        if started:
            title = f":notes: Started Playing :notes:"
        else:
            title = f":notes: Now Playing :notes:"
        self.embed = discord.Embed(title = title, description = f"{song['title']}\nfrom {song['author']}")
        import urllib.request
        url = song["url"]
        id = url.removeprefix("https://www.youtube.com/watch?v=")
        imgURL = thumbsmall.replace("{_ID_}", id)
        print(imgURL)
        print(f"{os.getcwd()}/{id}_small.jpg")
        try:
            path = urllib.request.urlretrieve(imgURL, f"{os.getcwd()}/{id}_small.jpg")[0]
            import colorthief
            colourthief = colorthief.ColorThief(path)
            dominant_color = colourthief.get_color(quality=1)
            self.embed.colour = discord.Colour.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])
            os.remove(path)
        except Exception as e:
            print(e)
            self.embed.colour = discord.Colour.red()
        self.embed.add_field(name = "Duration", value = str(datetime.timedelta(seconds=song["dur"])))
        self.embed.add_field(name = "URL", value = song["url"])
        if not started:            # Assign values to total and current values
            current = (g.variables["timelapsed"] / song["dur"]) * 100
            # First two arguments are mandatory
            bardata = progressBar.splitBar(self.total, int(current), size = 9)
            self.embed.add_field(name = "Time Elapsed", value = f"{bardata[0]}-{datetime.timedelta(seconds=g.variables['timelapsed'])}-{datetime.timedelta(seconds=song['dur'])}", inline = False)
            # self.embed.add_field(name= "Time Left", value = datetime.timedelta(seconds=song["dur"] - g.variables["timelapsed"]))
        self.embed.add_field(name= "Volume", value = self.volumelabels[Pl.volume], inline = False)
        self.embed.set_image(url = song["coverart"])
        self.embed.set_footer(text = f"Requested By: {song['user']}", icon_url=song["user"].avatar.url)
        self.embed.timestamp = datetime.datetime.now()
        self.view = discord.ui.View()
        shuffleButton = discord.ui.Button(emoji="🔀")
        shuffleButton.callback=lambda i: self.callback(i, "sh")
        pausePlayButton = discord.ui.Button(emoji="⏸️")
        pausePlayButton.callback=lambda i: self.callback(i, "p")
        restartButton = discord.ui.Button(emoji="🔁")
        restartButton.callback=lambda i: self.callback(i, "r")
        skipButton = discord.ui.Button(emoji="⏭️")
        skipButton.callback=lambda i: self.callback(i, "sk")
        stopButton = discord.ui.Button(emoji="⏹️")
        stopButton.callback=lambda i: self.callback(i, "st")
        volumeDownButton=discord.ui.Button(emoji="🔉")
        volumeDownButton.callback = lambda i: self.callback(i, "vd")
        volumeUpButton=discord.ui.Button(emoji="🔊")
        volumeUpButton.callback=lambda i: self.callback(i, "vu")
        # refreshButton = discord.ui.Button(emoji="🔃")
        # refreshButton.callback=lambda i: self.callback(i, "rf")
        
        self.view.add_item(shuffleButton)
        self.view.add_item(pausePlayButton)
        self.view.add_item(restartButton)
        self.view.add_item(skipButton)
        self.view.add_item(stopButton)
        self.view.add_item(volumeUpButton)
        self.view.add_item(volumeDownButton)
        # if not started:
        #     self.view.add_item(refreshButton)
        self.ogmessage = await interaction.channel.send(content = None, embed = self.embed, file = None, view=self.view)
        

    # Create Embed for Addition / Info about a song
    async def CreateEmbedAdded(self, interaction: discord.Interaction, song: dict, added: bool): 
        message = await interaction.channel.send("Thinking...")
        await message.delete()
        if added:
            title = "Added A Song"
        else:
            title = "Info"
        embed = discord.Embed(title = title, description = f"{song['title']}\nfrom {song['author']}")
        import urllib.request
        url = song["url"]
        id = url.removeprefix("https://www.youtube.com/watch?v=")
        imgURL = thumbsmall.replace("{_ID_}", id)
        print(imgURL)
        print(f"{os.getcwd()}/{id}_small.jpg")
        try:
            path = urllib.request.urlretrieve(imgURL, f"{os.getcwd()}/{id}_small.jpg")[0]
            import colorthief
            colourthief = colorthief.ColorThief(path)
            dominant_color = colourthief.get_color(quality=1)
            embed.colour = discord.Colour.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])
            os.remove(path)
        except Exception as e:
            print(e)
            embed.colour = discord.Colour.red()
        embed.add_field(name = "Position", value = str(song["id"]))
        embed.add_field(name = "Duration", value = str(datetime.timedelta(seconds=song["dur"])))
        embed.add_field(name = "URL", value = song["url"])
        total = 0
        x = 0
        for i in Pl.queue:
            if x != len(Pl.queue)-1:
                total += int(i["dur"])
            x += 1
        timel = total - int(g.variables["timelapsed"])
        logs.info(timel)
        totaltime = datetime.timedelta(seconds=timel)
        embed.add_field(name="Time until played", value = totaltime)
        embed.set_image(url = song["coverart"])
        embed.set_footer(text = f"Requested By: {song['user']}", icon_url=song["user"].avatar.url)
        embed.timestamp = datetime.datetime.now()
        

        await interaction.channel.send(content = None, embed = embed, file = None)
#/Embeds
# Youtube DL Stuff
        
# Set up for yt-dlp / ffmpeg
youtube_dl.utils.bug_reports_message = lambda: ''
nowplaying_default={
    "filename": "N/A",
    "title": "Nothing",
    "url": "N/A",
    "author" : "N/A",
    "coverart": "N/A",
    "user": "N/A",
    "dur": "N/A",
    "id": 0,
    "userfile": False,
}
ytdl_format_options = {
    'format': 'bestaudio/best',
    'audio-quality': 0,
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
    'concurrent-fragments': 1,
    'paths': {'home': f"{os.getcwd()}//Songs"}
}   
ytdl_format_options_no_down = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
    'skip-download' : True,
}

ffmpeg_options = {
    'options': '-vn'
}

#functions for downloading and getting a song
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
ytdl_no_down = youtube_dl.YoutubeDL(ytdl_format_options_no_down)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.3):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = os.path.join(f"{os.getcwd()}//Songs", data['title']) if stream else ytdl.prepare_filename(data)
        return filename
    
    @classmethod
    async def from_url_without_download(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl_no_down.extract_info(url, download=False))
        if 'entries' in data:
            data = data['entries'][0]
        # logs.info(data['entries'])
        return data
#/Youtube DL Stuff

#Player and Related

#Set Timelapsed Variable
g.variables["timelapsed"] = 0

#Player Class
class Player():
    #player - plays the music and cycles through the queue
    def __init__(self, client):
            logs.info("Initialising Player Class")
            self.client = client
            self.queue = []
            self.paused =  False
            self.playing = False
            self.volume = 3
            self.timestamp = 0
    async def player(self, interaction: discord.Interaction, client: discord.Client):
        def play():
            self.voiceclient.play(discord.FFmpegPCMAudio(source=self.queue[0]["filename"], before_options=f"-ss {self.timestamp}"))
            self.voiceclient.source = discord.PCMVolumeTransformer(self.voiceclient.source, volume = self.volume / 10)
        self.voiceclient = client.voice_clients[0]
        if self.voiceclient.is_playing() and not self.paused:
            await Em.CreateEmbedAdded(interaction, self.queue[-1], True)
        else:
            self.paused = False
            self.playing = True
            g.variables["nowplaying"] = self.queue[0]
            self.timestamp = self.queue[0]["starttime"]
            g.variables["timelapsed"] = self.queue[0]["starttime"]
            logs.info("Player Started!")
            await client.change_presence(status = discord.Status.online, activity=discord.Activity(type = discord.ActivityType.listening, name = self.queue[0]["title"], state = f"🎵{self.queue[0]['title']} || {self.queue[0]['author']}🎵", details = "I don't know how you've seen this lol"))
            await Em.CreateEmbedPlaying(interaction, self.queue[0], True)
            waitask = None
            waitask = asyncio.create_task(coro = self.waitforend(interaction, client), name = "Wait Task")
            self.thread = waitask
            playthread = threading.Thread(target=play, name="Play Thread", daemon=True)
            playthread.start()
            await asyncio.wait([waitask])
    #Reorder the queue
    async def queuereorder(self):
        print("Reordering Queue")
        for i in range(0, len(self.queue)):
            self.queue[i]["id"] = i
    #waitforend - Waits for the end of the current song and moves on to the next song, also handles pausing
    async def waitforend(self, interaction, client):
        logs.info(g.variables["timelapsed"])
        logs.info(self.queue[0]["dur"])
        while g.variables["timelapsed"] <= self.queue[0]["dur"]:
            # Assign values to total and current values
            total = 100
            current = (g.variables["timelapsed"] / self.queue[0]["dur"]) * 100
            # First two arguments are mandatory
            bardata = progressBar.splitBar(total, int(current), size=10)
            print(f"Time Elapsed: {g.variables['timelapsed']}|{bardata[0]}|{self.queue[0]['dur']} | {Pl.volume} | {self.queue[0]['title']}", end="\r")
            if not self.paused:
                g.variables["timelapsed"] += 1
            await asyncio.sleep(1.0)



        if self.queue[0]["userfile"]:
            os.remove(self.queue[0]["filename"])
            if self.queue[0]["coverart"] != f"{os.getcwd()}//Songs//Images//generic-thumb.png":
                os.remove(self.queue[0]["coverart"])
        #remove the last played song from the queue
        self.queue.pop(0)
        #Output the length of the queue
        logs.info(f"Queue Length: {len(self.queue)}")
        #Check if there are still songs left in the queue and continue or stop and leave the channel
        if self.queue != []:
            logs.info("Queue not empty moving on to next song")
            g.variables["timelapsed"] = self.queue[0]["starttime"]
            await self.player(interaction, client)
            await self.queuereorder()
            print(type(self.queue), type(Pl.queue))
            return
        else:
            await interaction.channel.send("Reached the end of the queue!\nuse /play to add more!")
            await self.voiceclient.disconnect()
            logs.info("Queue empty exiting player")
            self.playing = False
            self.queue = []
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Nothing"))
            print(f"{type(self.queue)} {len(self.queue)} | {type(Pl.queue)} {len(self.queue)}")
            return
        

    #stop - stops the currently playing song and clears the queue
    async def stop(self):
        logs.info("Stopped")
        self.voiceclient.stop()
        self.queue = []
        self.thread.cancel()
        await self.voiceclient.disconnect()
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Nothing"))
        g.variables["timelapsed"] = 0
    #stop - stops the currently playing song and removes it from the queue before starting the player again
    async def skip(self, interaction, client):
        logs.info("Skipped")
        self.voiceclient.stop()
        self.queue.pop(0)
        self.thread.cancel()
        g.variables["timelapsed"] = self.queue[0]["starttime"]
        await self.player(interaction, client)
    #restart - stops the current song and starts player again from the same song
    async def restart(self, interaction, client):
        logs.info("Restarted")
        self.voiceclient.stop()
        self.thread.cancel()
        g.variables["timelapsed"] = self.queue[0]["starttime"]
        await self.player(interaction, client)
    #pause - pause playing and update paused so waitforend doesnt keep counting
    async def pause(self):
        logs.info("Paused")
        self.paused = True
        self.voiceclient.pause()
     #pause - resume playing and update paused so waitforend continues counting
    async def resume(self):
        logs.info("Resuming")
        self.paused = False
        self.voiceclient.resume()
    
    async def queuechange(self):
        logs.info("Stopping and Saving time")
        self.timestamp = g.variables["timelapsed"]
        self.stop(self)

    async def queuechangeplay(self, interaction):
        logs.info("starting from where we left off")
        self.player(interaction, self.client)

    async def volume_up(self):
        self.volume += 1
        self.voiceclient.source.volume = self.volume / 10
    async def volume_down(self):
        self.volume -= 1
        self.voiceclient.source.volume = self.volume / 10


#/Player and Related
#Commands

#PlayCommand - Takes a Query, and plays it on discord
async def PlayCommand(interaction: discord.Interaction, query: str, starttime:str|None, client: discord.Client):
    #Prepare for downloading a playlist
    async def DownPrep(interaction: discord.Interaction, queries: list):
        #This function will find out how many threads are needed for a playlist
        pass
    #Download each song in the queries list
    async def Down(interaction: discord.Interaction, queries: list, thread: int):
        logs.info("Started Down Function")
        songs = []
        x = 0
        for i in queries:
            logs.warn(f"Thread: {thread} has started download {x}")
            filename = await YTDLSource.from_url(i)
            songs.append(filename)
            x+=1
        logs.info(f"Thread {thread} finished all downloads")
        return songs
    #youtube - download a youtube link and return the filename
    async def youtube(interaction: discord.Interaction, query: str):
        songs = await Down(interaction, [f'https://www.youtube.com/watch?v={data["id"]}'], 0)
        return songs
    #spotify - Search for the song on spotify and get the name and artist and search for it on youtube and return the filename
    async def spotify(interaction: discord.Interaction, query: str):
        await interaction.edit_original_response(content="Looking for the Song on Spotify...")
        with open(os.getcwd()+"/key.txt", "r") as r:
            keys = r.readlines()
            client_secret = str(keys[1]).removesuffix("\n")
            client_id = str(keys[2]).removesuffix("\n")
            print(client_id)
            print(client_secret)
            r.close()
            spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
            track = spotify.track(query)
            artists = ""
            first = True
            for i in track["artists"]:
                if first:
                    logs.info(i["name"])
                    artists += f"{i['name']}"
                else:
                    logs.info(i["name"])
                    artists += f", {i['name']}"
                first = False
        await interaction.edit_original_response(content=f"Found! {track['name']} by {artists}")
        logs.info(f"Found! {track['name']} by {artists}")
        ytlink = f"{track['name']} by {artists}"
        logs.info(ytlink)
        return [ytlink]
    

    logs.info(f"Play command was called! by: {interaction.user}, with Query: {query}")
    await interaction.response.send_message(f"Thinking...")
    if client.voice_clients == []:
         # connect to the channel the user is in
        channel = interaction.user.voice.channel
        await interaction.edit_original_response(content="Joining the voice channel..")
        await channel.connect(self_deaf=True)
    if "open.spotify" in query:
            file = None
            files = await spotify(interaction, query)
            file = files[0]
            query = file
    await interaction.edit_original_response(content=f"Searching for the song on Youtube...")
    if "playlist?list" in query:
        await interaction.edit_original_response(content = f"Found a playlist!")



    else:
        print(type(Pl.queue))
        data = await get_info(query)
        await interaction.edit_original_response(content=f"Found! {data['title']} by {data['channel']}")
        result = db.song.DB(data["title"])
        if result == None:
            await interaction.edit_original_response(content = "Song not cached, Downloading the song...")
            files = await youtube(interaction, query)
            file = files[0]
            song = {
                "filename": file,
                "title": data["title"],
                "url": f'https://www.youtube.com/watch?v={data["id"]}',
                "author" : data['channel'],
                "coverart": "",
                "channelart": "",
                "user": interaction.user,
                "dur": data['duration'],
                "id": len(Pl.queue),
                "userfile": False,
                "starttime": starttime,
            }
            try:
                song["coverart"] = data["thumbnail"]
            except:
                song["coverart"] = genericthumburl
            # try:
            #     song["channelart"] = data[""]
            # except:
            #     song["channelart"] = genericthumburl
            db.song.add(song)
        else:
            await interaction.edit_original_response(content =  "Found the song, using cached song")
            song = {
                "filename": result['filename'],
                "title": result["title"],
                "url": result['url'],
                "author" : result['author'],
                "coverart": result['coverart'],
                "user": interaction.user,
                "dur": result['dur'],
                "id": len(Pl.queue),
                "userfile": False,
                "starttime": starttime,
            }
        await interaction.edit_original_response(content = "Adding the song to the queue...")
        await interaction.delete_original_response()
        Pl.queue.append(song)
        await Pl.player(interaction, client)

queuepage = 0
#QueueCommand - Get and show the queue, in a nice format
async def QueueCommand(interaction: discord.Interaction):
    logs.info(f"queue command was called! by: {interaction.user}")
    global queuepage
    async def callback(i, x, ii):
        global queuepage
        # i = button interaction, ii = command interaction
        if queuepage == len(temptemp)-1 and x == "r":
            await i.response.send_message("you can't go forward anymore!", ephemeral=True)
            return queuepage
        if queuepage == 0 and x == "l":
            await i.response.send_message("you can't go back anymore!", ephemeral=True)
            return queuepage
        else:
            await i.response.send_message("Thinking...", ephemeral=False)
            await i.delete_original_response()
            if x == "r":
                queuepage += 1
            else:
                queuepage -= 1

            embed = discord.Embed(title=f"page: {queuepage+1} / {len(temptemp)}")
            for i in temptemp[queuepage]:
                embed.add_field(name=i["id"], value = f"Title: {i['title']}\n\nChannel: {i['author']}\n\nURL: {i['url']}\n\nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
            totalp = 0
            totalq = 0
            for i in temptemp[queuepage]:
                totalp += i["dur"]
            for i in Pl.queue:
                totalq += i["dur"]
            embed.colour = discord.Colour.red()
            embed.add_field(name=f"Total page Length", value = datetime.timedelta(seconds =  totalp))
            embed.add_field(name=f"Total queue Length", value =  datetime.timedelta(seconds = totalq))
            view = discord.ui.View()
            leftbutton = discord.ui.Button(emoji="⬅️")
            rightbutton = discord.ui.Button(emoji="➡️")
            leftbutton.callback = lambda i: callback(i, "l", interaction)
            rightbutton.callback = lambda i: callback(i, "r", interaction)
            view.add_item(leftbutton)
            view.add_item(rightbutton)
            await ii.edit_original_response(embed=embed, view = view)
            return queuepage

    if Pl.queue != []:
        await interaction.response.send_message("Thinking...", ephemeral=False)
        queuepages = len(Pl.queue) / 10  # Amount of Items Per queuepage
        if queuepages == 0:
            queuepages = 1
        elif queuepages % 1 != 0:
            queuepages = math.floor(queuepages) + 1
        logs.info(f"The amount of queuepages we need is: {queuepages}")
        temp = np.array_split(Pl.queue, queuepages)
        temptemp = []
        for i in temp:
            temptemp.append(i.tolist())
        logs.info(queuepage)
        embed = discord.Embed(title=f"queuepage: {queuepage+1} / {len(temptemp)}")
        for i in temptemp:
            logs.info(i)
        for i in temptemp[queuepage]:
            embed.add_field(name=i["id"], value = f"Title: {i['title']}\n\nChannel: {i['author']}\n\nURL: {i['url']}\n\nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
        totalp = 0
        totalq = 0
        for i in temptemp[queuepage]:
            totalp += i["dur"]
        for i in Pl.queue:
            totalq += i["dur"]
        embed.colour = discord.Colour.red()
        embed.add_field(name=f"Total queuepage Length", value = datetime.timedelta(seconds =  totalp))
        embed.add_field(name=f"Total queue Length", value =  datetime.timedelta(seconds = totalq))
        view = discord.ui.View()
        leftbutton = discord.ui.Button(emoji="⬅️")
        rightbutton = discord.ui.Button(emoji="➡️")
        leftbutton.callback = lambda i: callback(i, "l", interaction)
        rightbutton.callback = lambda i: callback(i, "r", interaction)
        view.add_item(leftbutton)
        view.add_item(rightbutton)
        await interaction.edit_original_response(embed=embed, view = view)
        return queuepage
    else:
        await interaction.response.send_message("The queue is Empty!")
        return queuepage
    
# --------------------------------------------- Not ready for stable ---------------------------------------------------
# #ChangeQueueCommand - Change current queue
# async def ChangeQueueCommand(interaction: discord.Interaction, client, index, cont):
#     global Pl
#     logs.info(f"Changing Queue to queue at {index} Requested by {interaction.user}")
#     queueindex = index
#     Pl.queuechange()
#     if queues[queueindex] == None:
#         await interaction.response.send_message("There isn't a queue at that index!")
#     else:
#         Pl = queues[queueindex]
#     if Pl.queue != [] and cont == True:
#         Pl.queuechangeplay(interaction)


# #CreateQueueCommand - Create a new queue
# async def CreateQueueCommand(interaction: discord.Interaction, client, change):
#     global queue
    

# async def Listqueues(interaction: discord.Interaction):
#     await interaction.response.send_message("Thinking...")
#     for i in queues:
#         await interaction.channel.send(i.queue[0]["name"])

# ----------------------------------------------------------------------------------------------------------------------

#ShuffleCommand - Shuffle the queue
async def ShuffleCommand(interaction: discord.Interaction):
    import random, pprint, time, datetime
    pp = pprint.PrettyPrinter()
    logs.info(f"Shuffle command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Shuffling...")
    t1 = time.time()
    shufflequeue = Pl.queue.copy()
    newqueue=[]
    for i in range(len(shufflequeue) -1):
        newqueue.append(0)
    first = shufflequeue.pop(0)
    for num in range(len(shufflequeue)):
        newqueue[num] = shufflequeue.pop(random.randint(0, len(shufflequeue) - 1))
    newqueue.insert(0, first)
    for i in range(0, len(newqueue)):
        newqueue[i]["id"] = i
    

    Pl.queue = newqueue
    t2 = time.time()
    print(f"Shuffle took: {datetime.timedelta(seconds=t2-t1)}")
    
        
wrappedpage = 0
#Wrapped Command - List most listened to songs
async def WrappedCommand(interaction: discord.Interaction):
    database = db.song.load()
    database.sort(key=lambda i: i[8] , reverse=True)
    logs.info(f"wrapped command was called! by: {interaction.user}")
    global wrappedpage
    async def callback(i, x, ii):
        global wrappedpage
        # i = button interaction, ii = command interaction
        if wrappedpage == len(temptemp)-1 and x == "r":
            await i.response.send_message("you can't go forward anymore!", ephemeral=True)
            return wrappedpage
        if wrappedpage == 0 and x == "l":
            await i.response.send_message("you can't go back anymore!", ephemeral=True)
            return wrappedpage
        else:
            await i.response.send_message("Thinking...", ephemeral=False)
            await i.delete_original_response()
            if x == "r":
                wrappedpage += 1
            else:
                wrappedpage -= 1

            embed = discord.Embed(title=f"page: {wrappedpage+1} / {len(temptemp)}")
            for i in temptemp[wrappedpage]:
                embed.add_field(name=i[0], value = f"Title: {i[2]}\n\nChannel: {i[4]}\n\nURL: {i[3]}\n\nTimes Played:  {i[8]}\n\nTotal Estimated Time Played: {datetime.timedelta(seconds=float(i[6])*float(i[8]))}\n\nDuration: {datetime.timedelta(seconds = float(i[6]))}", inline = True)
            embed.colour = discord.Colour.red()
            view = discord.ui.View()
            leftbutton = discord.ui.Button(emoji="⬅️")
            rightbutton = discord.ui.Button(emoji="➡️")
            leftbutton.callback = lambda i: callback(i, "l", interaction)
            rightbutton.callback = lambda i: callback(i, "r", interaction)
            view.add_item(leftbutton)
            view.add_item(rightbutton)
            await ii.edit_original_response(embed=embed, view = view)
            return wrappedpage

    if database != []:
        await interaction.response.send_message("Thinking...", ephemeral=False)
        wrappedpages = len(database) / 10  # Amount of Items Per wrappedpage
        if wrappedpages == 0:
            wrappedpages = 1
        elif wrappedpages % 1 != 0:
            wrappedpages = math.floor(wrappedpages) + 1
        logs.info(f"The amount of pages we need is: {wrappedpages}")
        temp = np.array_split(database, wrappedpages)
        temptemp = []
        for i in temp:
            temptemp.append(i.tolist())
        logs.info(wrappedpage)
        embed = discord.Embed(title=f"page: {wrappedpage+1} / {len(temptemp)}")
        for i in temptemp:
            logs.info(i)
        for i in temptemp[wrappedpage]:
            embed.add_field(name=i[0], value = f"Title: {i[2]}\n\nChannel: {i[4]}\n\nURL: {i[3]}\n\nTimes Played:  {i[8]}\n\nTotal Estimated Time Played: {datetime.timedelta(seconds=float(i[6])*float(i[8]))}\n\nDuration: {datetime.timedelta(seconds = float(i[6]))}", inline = True)
        embed.colour = discord.Colour.red()
        view = discord.ui.View()
        leftbutton = discord.ui.Button(emoji="⬅️")
        rightbutton = discord.ui.Button(emoji="➡️")
        leftbutton.callback = lambda i: callback(i, "l", interaction)
        rightbutton.callback = lambda i: callback(i, "r", interaction)
        view.add_item(leftbutton)
        view.add_item(rightbutton)
        await interaction.edit_original_response(embed=embed, view = view)
        return wrappedpage
    else:
        await interaction.response.send_message("The database is Empty!")
        return wrappedpage
    



#RemoveCommand - Remove a video from the queue
async def RemoveCommand(interaction: discord.Interaction, index):
    logs.info(f"Remove command was called! by: {interaction.user}")
    
    name = Pl.queue[index]["title"]
    if Pl.queue != []:
        if index != 0:
            try:
                await interaction.response.send_message(f"Removing: {name} from {index}")
                Pl.queue.pop(index)
            except Exception as e:
                await interaction.edit_original_response(content=e)
            else:
                await interaction.edit_original_response(content=f"Removed: {name} from {index}")
                x = 0
                for i in Pl.queue:
                    i["id"] = x
                    x += 1

        else:
            await interaction.response.send_message(content=f"Can't remove the song you are listening to!, use /skip instead")
    else:
        await interaction.response.send_message(content=f"There is nothing to remove!")




#PauseCommand -  Pause playing
async def PauseCommand(interaction: discord.Interaction):
    logs.info(f"Pause command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Pausing!")
    await Pl.pause()




#ResumeCommand -  Resume from pausing
async def ResumeCommand(interaction: discord.Interaction):
    logs.info(f"Resume command was called by: {interaction.user}")
    await interaction.response.send_message(f"Resuming...")
    await Pl.resume()



#SkipCommand - Skip the current video
async def SkipCommand(interaction: discord.Interaction, client):
    logs.info(f"Skip command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Skipping...")
    voiceclient = client.voice_clients[0]
    if not voiceclient.is_playing():
        await interaction.followup.send("Nothing is playing!")
    else:
        await Pl.skip(interaction, client)





#StopCommand - Stop the current playing video and clear the queue
async def StopCommand(interaction: discord.Interaction):
    logs.info(f"Stop command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Stopping and Clearing queue...")
    await Pl.stop()





#RestartCommand -  Restart the current video
async def RestartCommand(interaction: discord.Interaction, client):
    logs.info(f"Restart command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Restarting...")
    await Pl.restart(interaction, client)





#LeaveCommand -  leave the voice channel
async def LeaveCommand(interaction: discord.Interaction, client: discord.Client):
    logs.info(f"Leave command was called! by: {interaction.user}")
    if client.voice_clients == []:
        embed = discord.Embed(title="Something Went Wrong!", description= "I'm not in a voice channel!")
        await interaction.response.send_message(embed=embed)
    else:
        voiceclient = client.voice_clients[0]
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Nothing"))
        await voiceclient.disconnect()
        await interaction.response.send_message("Left!")




#JoinCommand -  Join the voice channel the user is currently in
async def JoinCommand(interaction: discord.Interaction):
    logs.info(f"Join command was called! by: {interaction.user}")
    if interaction.user.voice == None:
        embed = discord.Embed(title="Something Went Wrong!", description= "You're not in a voice channel")
        await interaction.response.send_message(embed=embed)
    else:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Joined!")




#NowPlayingCommand -  Show the currently playing song
async def NowPlayingCommand(interaction: discord.Interaction, client: discord.Client):
    logs.info(f"Now Playing command was called! by: {interaction.user}")
    await interaction.response.send_message("Thinking...")
    await interaction.delete_original_response()
    if Pl.playing:
        await Em.CreateEmbedPlaying(interaction, g.variables["nowplaying"], False)
    else:
        await interaction.channel.send("Nothing is playing!")

async def InfoCommand(interaction:discord.Interaction, index: int):
    logs.info(f"Info Command called by {interaction.user}")
    await interaction.response.send_message("Thinking...")
    await interaction.delete_original_response()
    if Pl.queue != []:
        if not len(Pl.queue) <= 1:
            await Em.CreateEmbedAdded(interaction, Pl.queue[index], False)






#PlayFileCommand -  Play a file provided by the user
async def PlayFileCommand(interaction: discord.Interaction, file: discord.Attachment, client):

    logs.info(f"Play File command was called! by: {interaction.user}, with Query: {file}")
    await interaction.response.send_message("Thinking...")
    if client.voice_clients == []:
         # connect to the channel the user is in
        channel = interaction.user.voice.channel
        await interaction.edit_original_response(content="Joining the voice channel..")
        await channel.connect(self_deaf=True)

    url = file
    await interaction.channel.send(str(file).split("//")[6].split("?")[0])
    file_name = f"{os.getcwd()}//Songs/{str(file).split('//')[6].split('?')[0]}"
    if not os.path.exists(file_name):
        res = requests.get(url, stream = True)
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            logs.info('Song sucessfully Downloaded: ',file_name, 'from: ', file)
        else:
            logs.info("Song Couldn't be retrieved")

        await interaction.edit_original_response(content = f"Successfully Downloaded: {file_name.split('/')[1]}")
    
    else:
        await interaction.edit_original_response(content = f"Song Already Downloaded: {file_name.split('/')[1]}")
    logs.info(f"Adding: {file_name} to the queue")
    filextension = os.path.splitext(os.path.basename(file_name))[1].split(".")[1]
    logs.info(f"Found: {filextension}")
    song = {
        "filename": file_name,
        "title": "",
        "url": str(url),
        "author" : "",
        "coverart": "",
        "user": None,
        "dur": 0.0,
        "id": len(Pl.queue),
        "userfile": True,
    }
    try:
        audio = mutagen.File(file_name, None, True)
        song["title"] = audio["title"][0]
        song["author"] = audio["artist"][0]
        song['user'] = interaction.user
        
        with audioread.audio_open(file_name) as f:
            song["dur"] = f.duration

    except Exception as e:
        logs.info(e)
        with audioread.audio_open(file_name) as f:
            song["dur"] = f.duration
        song["title"] = file_name
        song["author"] = "various artists"
        song["user"] = interaction.user
    if filextension == "flac":
        try:
            if not os.path.exists(f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"):
                subprocess.check_output(f'ffmpeg -i {file_name} -an "{os.getcwd()}//Songs//Images//{song["title"]} cover.jpg" ', shell=True)
            song["coverart"] = f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"
        except:
            song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"
    if filextension == "mp3":
        try:
            if not os.path.exists(f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"):
                subprocess.check_output(f'ffmpeg -i {file_name} -an "{os.getcwd()}//Songs//Images//{song["title"]} cover.jpg" ', shell=True)
            song["coverart"] = f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"
        except:
            song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"
    if filextension == "mp4":
        try:
            if not os.path.exists(f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"):
                subprocess.check_output(f'ffmpeg -i {file_name} -an "{os.getcwd()}//Songs//Images//{song["title"]} cover.jpg" ', shell=True)
            song["coverart"] = f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"
        except:
            song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"
    if filextension == "m4a":
        try:
            if not os.path.exists(f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"):
                subprocess.check_output(f'ffmpeg -i {file_name} -an "{os.getcwd()}//Songs//Images//{song["title"]} cover.jpg" ', shell=True)
            song["coverart"] = f"{os.getcwd()}//Songs//Images//{song['title']} cover.jpg"
        except:
            song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"
    else:
        song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"

    logs.info(song)
    Pl.queue.append(song)
    await Em.CreateEmbedAdded(interaction, song, True)
    await Pl.player(interaction, client)




#/Commands

#Miscellaneous Functions
async def get_info(url):
    from googleapiclient.discovery import build
    import googleapiclient.discovery
    token = open("key.txt", "r").readlines()[3]
    youtube = build('youtube', 'v3', developerKey=token)
    try:
        raise Exception("yo") 
        request = youtube.search().list(part="id", q=url, maxResults=1, type="video")
        response =  request.execute()

        print(response)
    except Exception as e:
        logs.warn(f"An Error Occured, most likely we have reached the quota limit \nError: {e}")
        response = await YTDLSource.from_url_without_download(url)
        return response
    

#/Miscellaneous Functions




