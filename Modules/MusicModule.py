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
import database as db
#/Imports
#Startup
logs.info("Music Module Started Successfully!")
enabled = True
#Check if the module is running or not
def running():
    return True
first = True
genericthumburl = "https://raw.githubusercontent.com/ItBePhill/Creme-Egg-Bot-ReWritten/main/Songs/Images/generic-thumb.png"
thumbsmall = "https://i.ytimg.com/vi/{_ID_}/default.jpg"
#/Startup

#Em


class embeds():
    def __init__(self):
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
    async def callback(self, i: discord.Interaction, x: str):
        await i.response.send_message(content =  "Thinking...", ephemeral=True)
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
                    view.add_item(shuffleButton)
                    view.add_item(pausePlayButton)
                    view.add_item(restartButton)
                    view.add_item(skipButton)
                    view.add_item(stopButton)
                    view.add_item(volumeUpButton)
                    view.add_item(volumeDownButton)
                    await self.ogmessage.edit(embed=embed, view=view)
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
                    await self.ogmessage.edit(embed=embed, view=view)
            case "r":
                await Pl.restart(i, Pl.client)
            case "st":
                await Pl.stop()
            case "vu":
                await Pl.volume_up()
                embed = self.embed
                view = self.view
                embed.remove_field(len(embed._fields) - 1)
                self.embed.add_field(name= "Volume", value = self.volumelabels[Pl.volume], inline = False)
                await self.ogmessage.edit(embed=embed, view=view)
            case "vd":
                await Pl.volume_down()
                embed = self.embed
                view = self.view
                embed.remove_field(len(embed._fields) - 1)
                self.embed.add_field(name= "Volume", value = self.volumelabels[Pl.volume], inline = False)
                await self.ogmessage.edit(embed=embed, view=view)

    #Create the "Playing" Embed, has a variation for Now Playing and Started Playing
    async def CreateEmbedPlaying(self, interaction: discord.Interaction, song: dict, started: bool):
                    
        await interaction.channel.send(content = "Thinking...")
        if started:
            title = f"Started Playing"
        else:
            title = f"Now Playing"
        self.embed = discord.Embed(title = title, description = f"{song['title']}\n{song['author']}")
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
        if not started:
            self.embed.add_field(name = "Time Elapsed", value = datetime.timedelta(seconds=g.variables["timelapsed"]), inline = False)
            self.embed.add_field(name= "Time Left", value = datetime.timedelta(seconds=song["dur"] - g.variables["timelapsed"]))
        self.embed.add_field(name = "Duration", value = str(datetime.timedelta(seconds=song["dur"])))
        self.embed.add_field(name = "URL", value = song["url"])
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
        
        self.view.add_item(shuffleButton)
        self.view.add_item(pausePlayButton)
        self.view.add_item(restartButton)
        self.view.add_item(skipButton)
        self.view.add_item(stopButton)
        self.view.add_item(volumeUpButton)
        self.view.add_item(volumeDownButton)
        self.ogmessage = await interaction.channel.send(content = None, embed = self.embed, file = None, view=self.view)
        

    # Create Embed for Addition / Info about a song
    async def CreateEmbedAdded(self, interaction: discord.Interaction, song): 
        await interaction.channel.send("Thinking...")
        embed = discord.Embed(title = "Added A Song", description = f"{song['title']}\n{song['author']}")
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
Em = embeds()

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
    'extract-audio': True,
    'audio-format': "wav",
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
    'concurrent-fragments': 2,
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
#Reorder the queue after a song or other operation is made

#Set TimeElapsed Variable
g.variables["timelapsed"] = 0

#Player Class
class Player():
    #player - plays the music and cycles through the queue
    def __init__(self, client):
            self.client = client
            self.queue = []
            self.paused =  False
            self.playing = False
            self.volume = 3
    async def player(self, interaction: discord.Interaction, client: discord.Client):
        def play(client: discord.Client):
            self.voiceclient.play(discord.FFmpegPCMAudio(source=self.queue[0]["filename"]))
            self.voiceclient.source = discord.PCMVolumeTransformer(self.voiceclient.source, volume = self.volume / 10)
        self.voiceclient = client.voice_clients[0]
        if self.voiceclient.is_playing() and not self.paused:
            await Em.CreateEmbedAdded(interaction, self.queue[-1])
        else:
            self.paused = False
            self.playing = True
            g.variables["nowplaying"] = self.queue[0]
            g.variables["timelapsed"] = 0
            logs.info("Player Started!")
            await client.change_presence(status = discord.Status.online, activity=discord.Activity(type = discord.ActivityType.listening, name = self.queue[0]["title"], state = f"🎵{self.queue[0]['title']} || {self.queue[0]['author']}🎵", details = "I don't know how you've seen this lol"))
            await Em.CreateEmbedPlaying(interaction, self.queue[0], True)
            waitask = None
            waitask = asyncio.create_task(coro = self.waitforend(interaction, client), name = "Wait Task")
            self.thread = waitask
            playthread = threading.Thread(target=play, name="Play Thread", args=[client], daemon=True)
            playthread.start()
            await asyncio.wait([waitask])
            self.queue = waitask.result()
    #Reorder the queue
    async def queuereorder(self):
        if self.queue != None:
            for song in self.queue:
                song["id"] = self.queue.index(song)
        else:
            logs.warn("Queue is empty")
    #waitforend - Waits for the end of the current song and moves on to the next song, also handles pausing
    async def waitforend(self, interaction, client):
        logs.info(g.variables["timelapsed"])
        logs.info(self.queue[0]["dur"])
        while g.variables["timelapsed"] <= self.queue[0]["dur"]:
            print(f"Time Elapsed: {g.variables['timelapsed']} / {self.queue[0]['dur']} | {Pl.volume} | {self.queue[0]['title']}", end="\r")
            if not self.paused:
                g.variables["timelapsed"] += 1
            await asyncio.sleep(1.0)



        if self.queue[0]["userfile"]:
            os.remove(self.queue[0]["filename"])
            if self.queue[0]["coverart"] != f"{os.getcwd()}//Songs//Images//generic-thumb.png":
                os.remove(self.queue[0]["coverart"])
        self.queue.pop(0)
        
        if self.queue != []:
            logs.info("queue not empty moving on to next song")
            g.variables["timelapsed"] = 0
            await self.player(interaction, client)
            self.queuereorder
        else:
            await interaction.channel.send("Reached the end of the self.queue!\nuse /play to add more!")
            await self.voiceclient.disconnect()
            logs.info("self.queue empty exiting player")
            self.playing = False
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Nothing"))
    
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
        g.variables["timelapsed"] = 0
        await Player.player(interaction, client)
    #restart - stops the current song and starts player again from the same song
    async def restart(self, interaction, client):
        logs.info("Restarted")
        
        self.voiceclient.stop()
        self.thread.cancel()
        g.variables["timelapsed"] = 0
        await Player.player(interaction, client)
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
    
    async def volume_up(self):
        self.volume += 1
        self.voiceclient.source.volume = self.volume / 10
    async def volume_down(self):
        self.volume -= 1
        self.voiceclient.source.volume = self.volume / 10


#/Player and Related
#Commands

#PlayCommand - Takes a Query, and plays it on discord
async def PlayCommand(interaction: discord.Interaction, query: str, client: discord.Client):
    global Pl
    Pl = Player(client=client)
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
        # try:
        #     data = await get_info_youtube(query)
        # except:
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
            }
        await interaction.edit_original_response(content = "Adding the song to the queue...")
        Pl.queue.append(song)
        await Pl.player(interaction, client)

page = 0
#QueueCommand - Get and show the queue, in a nice format
async def QueueCommand(interaction: discord.Interaction):
    logs.info(f"Pl.queue command was called! by: {interaction.user}")
    global page
    async def callback(i, x, ii):
        global page
        # i = button interaction, ii = command interaction
        if page == len(temptemp)-1 and x == "r":
            await i.response.send_message("you can't go forward anymore!", ephemeral=True)
            return page
        if page == 0 and x == "l":
            await i.response.send_message("you can't go back anymore!", ephemeral=True)
            return page
        else:
            await i.response.send_message("Thinking...", ephemeral=True)
            await i.delete_original_response()
            if x == "r":
                page += 1
            else:
                page -= 1

            embed = discord.Embed(title=f"Page: {page+1} / {len(temptemp)}")
            for i in temptemp[page]:
                embed.add_field(name=i["id"], value = f"Title: {i['title']}/n/nChannel: {i['author']}/n/nURL: {i['url']}/n/nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
            totalp = 0
            totalq = 0
            for i in temptemp[page]:
                totalp += i["dur"]
            for i in Pl.queue:
                totalq += i["dur"]
            embed.colour = discord.Colour.red()
            embed.add_field(name=f"Total Page Length", value = datetime.timedelta(seconds =  totalp))
            embed.add_field(name=f"Total queue Length", value =  datetime.timedelta(seconds = totalq))
            view = discord.ui.View()
            leftbutton = discord.ui.Button(emoji="⬅️")
            rightbutton = discord.ui.Button(emoji="➡️")
            leftbutton.callback = lambda i: callback(i, "l", interaction)
            rightbutton.callback = lambda i: callback(i, "r", interaction)
            view.add_item(leftbutton)
            view.add_item(rightbutton)
            await ii.edit_original_response(embed=embed, view = view)
            return page

    if Pl.queue != []:
        await interaction.response.send_message("Thinking...", ephemeral=True)
        pages = len(Pl.queue) / 10  # Amount of Items Per Page
        if pages == 0:
            pages = 1
        elif pages % 1 != 0:
            pages = math.floor(pages) + 1
        logs.info(f"The amount of pages we need is: {pages}")
        temp = np.array_split(Pl.queue, pages)
        temptemp = []
        for i in temp:
            temptemp.append(i.tolist())
        logs.info(page)
        embed = discord.Embed(title=f"Page: {page+1} / {len(temptemp)}")
        for i in temptemp:
            logs.info(i)
        for i in temptemp[page]:
            embed.add_field(name=i["id"], value = f"Title: {i['title']}/n/nChannel: {i['author']}/n/nURL: {i['url']}/n/nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
        totalp = 0
        totalq = 0
        for i in temptemp[page]:
            totalp += i["dur"]
        for i in Pl.queue:
            totalq += i["dur"]
        embed.colour = discord.Colour.red()
        embed.add_field(name=f"Total Page Length", value = datetime.timedelta(seconds =  totalp))
        embed.add_field(name=f"Total queue Length", value =  datetime.timedelta(seconds = totalq))
        view = discord.ui.View()
        leftbutton = discord.ui.Button(emoji="⬅️")
        rightbutton = discord.ui.Button(emoji="➡️")
        leftbutton.callback = lambda i: callback(i, "l", interaction)
        rightbutton.callback = lambda i: callback(i, "r", interaction)
        view.add_item(leftbutton)
        view.add_item(rightbutton)
        await interaction.edit_original_response(embed=embed, view = view)
        return page
    else:
        await interaction.response.send_message("The queue is Empty!")
        return page
    

#ShuffleCommand - Shuffle the queue
async def ShuffleCommand(interaction: discord.Interaction):
    logs.info(f"Shuffle command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Thinking...")



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
    if Pl.playing:
        await Em.CreateEmbedPlaying(interaction, g.variables["nowplaying"], False)






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
    await Em.CreateEmbedAdded(interaction, song)
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




