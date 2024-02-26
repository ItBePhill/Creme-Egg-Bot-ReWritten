#Music Module

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
from database import *
logs.info("Music Module Started Successfully!")
enabled = True
def running():
    return True
first = True
class embeds():
    @classmethod
    async def CreateEmbedPlaying(self, interaction: discord.Interaction, song: list, started: bool):
        message: discord.Message = await interaction.channel.send(content = "Thinking...")

        if started:
            title = f"Started Playing: {song['title']}"
        else:
            title = f"Now Playing: {song['title']}"
        embed = discord.Embed(title = title)
        embed.colour = discord.Colour.red()
        embed.add_field(name = "Title", value = song["title"])
        embed.add_field(name = "Author", value = song["author"])
        embed.add_field(name = "Duration", value = str(datetime.timedelta(seconds=song["dur"])))
        embed.add_field(name = "URL", value = song["url"])
        if not started:
            embed.add_field(name = "Time Elapsed", value = g.variables["timelapsed"])
        file = discord.File(song["coverart"])
        last_message: discord.Message = await message.edit(content = None, attachments = [file], embed = None)
        embed.set_image(url = last_message.attachments[0])
        embed.set_footer(text = f"Requested By: {song['user']}")
        embed.timestamp = datetime.datetime.now()
        await last_message.delete()
        await interaction.channel.send(content = None, embed = embed, file = None)
    @classmethod
    async def CreateEmbedAdded(self, interaction: discord.Interaction, song): 
        message = await interaction.channel.send("Thinking...")
        embed = discord.Embed(title = song["title"])
        embed.colour = discord.Colour.red()
        embed.add_field(name = "Position", value = str(song["id"]))
        embed.add_field(name = "Title", value = song["title"])
        embed.add_field(name = "Author", value = song["author"])
        embed.add_field(name = "Duration", value = str(datetime.timedelta(seconds=song["dur"])))
        embed.add_field(name = "URL", value = song["url"])
        total = 0
        x = 0
        for i in queue:
            if x != len(queue)-1:
                total += int(i["dur"])
            x += 1
        timel = total - int(g.variables["timelapsed"])
        logs.info(timel)
        totaltime = datetime.timedelta(seconds=timel)
        embed.add_field(name="Time until played", value = totaltime)
        file = discord.File(song["coverart"])
        last_message: discord.Message = await message.edit(content = None, attachments = [file], embed = None)
        # (message_id = message.id, content = "Thinking...", attachments = [file])
        embed.set_image(url = last_message.attachments[0])
        embed.set_footer(text = f"Requested By: {song['user']}")
        embed.timestamp = datetime.datetime.now()
        await last_message.delete()
        await interaction.channel.send(content = None, embed = embed, file = None)

# Youtube DL Stuff / queue
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
    'writethumbnail': True,
    'embedthumbnail': True,
    'concurrent-fragments': 2,
    'paths': {'home': f"{os.getcwd()}//Songs", 'thumbnail': 'Images/Videos'}
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
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
ytdl_no_down = youtube_dl.YoutubeDL(ytdl_format_options_no_down)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
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
        return data
# End Of Youtube DL Stuff


async def queuereorder():
    global queue
    for song in queue:
        song["id"] = queue.index(song)
    return queue
    


queue = []
nowplaying = {}
g.variables["timelapsed"] = 0
paused = False

class Player():
    @classmethod
    async def player(self, interaction: discord.Interaction, client: discord.Client):
        global queue, first
        self.paused = False
        g.variables["nowplaying"] = queue[0]
        logs.info("Player Started!")
        timelapsed = 0
        stopped = False
        filename = queue[0]["filename"]
        dur = queue[0]["dur"]
        title = queue[0]["title"]
        author = queue[0]["author"]
        url = queue[0]["url"]
        voiceclient: discord.VoiceClient = client.voice_clients[0]
        self.voiceclient = voiceclient
        if voiceclient.is_playing():
            return queue
        await client.change_presence(status = discord.Status.online, activity=discord.Activity(type = discord.ActivityType.listening, name = queue[0]["title"], state = f"🎵{queue[0]['title']} || {queue[0]['author']}🎵", details = "I don't know how you've seen this lol"))
        await embeds.CreateEmbedPlaying(interaction, queue[0], True)
        voiceclient.play(discord.FFmpegPCMAudio(source=filename))
        voiceclient.source = discord.PCMVolumeTransformer(voiceclient.source, volume = 0.3)
        logs.info("Creating task and waiting")
        waitask = None
        waitask = asyncio.create_task(coro = self.waitforend(interaction, queue), name = "Wait Task")
        self.thread = waitask
        await asyncio.wait([waitask])
        queue = waitask.result()
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Nothing"))
        if queue != []:
            logs.info("Queue not empty moving on to next song")
            g.variables["timelapsed"] = 0
            await queuereorder()
            await Player.player(interaction, client)
            return queue, first
        else:
            await interaction.channel.send("Reached the end of the Queue!")
            voiceclient.voice_disconnect()
            logs.info("Queue empty exiting player")
            return queue, first
    @classmethod
    async def waitforend(self, interaction, queue):
        # checktask = None
        # checktask = asyncio.create_task(coro = checkforcommands(interaction, thread1, checktask))
        while not g.variables["timelapsed"] >= queue[0]["dur"]:
            if not self.paused:
                g.variables["timelapsed"] += 1
            await asyncio.sleep(1.0)
        if queue[0]["userfile"]:
            os.remove(queue[0]["filename"])
            if queue[0]["coverart"] != f"{os.getcwd()}//Songs//Images//generic-thumb.png":
                os.remove(queue[0]["coverart"])
            else:
                os.remove(queue[0]["coverart"])
        # await checkforcommands.kill(checktask)
        queue.pop(0)
        return queue
    @classmethod
    async def stop(self):
        global queue
        logs.info("Stopped")
        self.voiceclient.stop()
        queue = []
        self.thread.cancel()
        return queue
    @classmethod
    async def skip(self, interaction, client):
        logs.info("Skipped")
        global queue
        self.voiceclient.stop()
        queue.pop(0)
        self.thread.cancel()
        g.variables["timelapsed"] = 0
        await Player.player(interaction, client)
        return queue
    @classmethod
    async def restart(self, interaction, client):
        logs.info("Restarted")
        global queue
        self.voiceclient.stop()
        self.thread.cancel()
        g.variables["timelapsed"] = 0
        await Player.player(interaction, client)
        return queue
    @classmethod
    async def pause(self):
        logs.info("Paused")
        self.paused = True
        self.voiceclient.pause()
    @classmethod
    async def resume(self):
        logs.info("Resuming")
        self.paused = False
        self.voiceclient.resume()
    

async def PlayCommand(interaction: discord.Interaction, query: str, client: discord.Client):
    """
    TODO:
    
    """
    async def DownPrep(interaction: discord.Interaction, queries: list):
        #This function will find out how many threads are needed for a playlist
        pass
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


    async def youtube(interaction: discord.Interaction, query: str):
        if "playlist" in query:
            logs.info("Found A Playlist")
        songs = await Down(interaction, [query], 0)
        return songs
    async def spotify(interaction: discord.Interaction, query: str):
        return None
    

    logs.info(f"Play command was called! by: {interaction.user}, with Query: {query}")
    await interaction.response.send_message(f"Thinking...")
    if client.voice_clients == []:
         # connect to the channel the user is in
        channel = interaction.user.voice.channel
        await interaction.edit_original_response(content="Joining the voice channel..")
        await channel.connect(self_deaf=True)
    data = await YTDLSource.from_url_without_download(query)
    logs.info(data)
    result = db.DB(db, data["title"])
    if result == None:
        await interaction.edit_original_response(content =  "Didn't find song, Downloading the song...")
        if "spotify" in query:
            files = await spotify(interaction, query)
            file = files[0]
        else:
            files = await youtube(interaction, query)
            file = files[0]
        song = {
            "filename": file,
            "title": data["title"],
            "url": f'https://www.youtube.com/watch?v={data["id"]}',
            "author" : data['channel'],
            "coverart": "",
            "user": interaction.user,
            "dur": data['duration'],
            "id": len(queue),
            "userfile": False,
        }
        if os.path.exists(f"{os.getcwd()}//Songs//Images//Videos//{os.path.splitext(os.path.basename(song['filename']))[0]}.webp"):
            song["coverart"] = f"{os.getcwd()}//Songs//Images//Videos//{os.path.splitext(os.path.basename(song['filename']))[0]}.webp"
        else:
            
             song["coverart"] = f"{os.getcwd()}//Songs//Images//generic-thumb.png"
        db.add(db, song)
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
            "id": len(queue),
            "userfile": False,
        }
    await interaction.edit_original_response(content = "Adding to the queue...")
    queue.append(song)
    await embeds.CreateEmbedAdded(interaction, song)
    await Player.player(interaction, client)

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
        "id": len(queue),
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
    queue.append(song)
    await embeds.CreateEmbedAdded(interaction, song)
    await Player.player(interaction, client)

page = 0
async def QueueCommand(interaction: discord.Interaction):
    logs.info(f"Queue command was called! by: {interaction.user}")
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

            embed = discord.Embed(title=f"Queue Page: {page+1} / {len(temptemp)}")
            for i in temptemp[page]:
                embed.add_field(name=i["id"], value = f"Title: {i['title']}/n/nAuthor: {i['author']}/n/nURL: {i['url']}/n/nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
            totalp = 0
            totalq = 0
            for i in temptemp[page]:
                totalp += i["dur"]
            for i in queue:
                totalq += i["dur"]
            embed.colour = discord.Colour.red()
            embed.add_field(name=f"Total Page Length", value = datetime.timedelta(seconds =  totalp))
            embed.add_field(name=f"Total Queue Length", value =  datetime.timedelta(seconds = totalq))
            view = discord.ui.View()
            leftbutton = discord.ui.Button(emoji="⬅️")
            rightbutton = discord.ui.Button(emoji="➡️")
            leftbutton.callback = lambda i: callback(i, "l", interaction)
            rightbutton.callback = lambda i: callback(i, "r", interaction)
            view.add_item(leftbutton)
            view.add_item(rightbutton)
            await ii.edit_original_response(embed=embed, view = view)
            return page

    if queue != []:
        await interaction.response.send_message("Thinking...", ephemeral=True)
        pages = len(queue) / 10  # Amount of Items Per Page
        if pages == 0:
            pages = 1
        elif pages % 1 != 0:
            pages = math.floor(pages) + 1
        logs.info(f"The amount of pages we need is: {pages}")
        temp = np.array_split(queue, pages)
        temptemp = []
        for i in temp:
            temptemp.append(i.tolist())
        logs.info(page)
        embed = discord.Embed(title=f"Queue Page: {page+1} / {len(temptemp)}")
        for i in temptemp:
            logs.info(i)
        for i in temptemp[page]:
            embed.add_field(name=i["id"], value = f"Title: {i['title']}/n/nAuthor: {i['author']}/n/nURL: {i['url']}/n/nDuration: {datetime.timedelta(seconds = i['dur'])}", inline = True)
        totalp = 0
        totalq = 0
        for i in temptemp[page]:
            totalp += i["dur"]
        for i in queue:
            totalq += i["dur"]
        embed.colour = discord.Colour.red()
        embed.add_field(name=f"Total Page Length", value = datetime.timedelta(seconds =  totalp))
        embed.add_field(name=f"Total Queue Length", value =  datetime.timedelta(seconds = totalq))
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
        await interaction.response.send_message("The Queue is Empty!")
        return page

async def ShuffleCommand(interaction: discord.Interaction):
    logs.info(f"Shuffle command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Shuffle command was called! by: {interaction.user}")

async def RemoveCommand(interaction: discord.Interaction, index):
    logs.info(f"Remove command was called! by: {interaction.user}")
    global queue
    name = queue[index]
    if queue != []:
        if index != 0:
            try:
                await interaction.response.send_message(f"Removing: {name} from {index}")
                queue.pop(index)
            except Exception as e:
                await interaction.edit_original_response(content=e)
            else:
                await interaction.edit_original_response(content=f"Removed: {name} from {index}")
                x = 0
                for i in queue:
                    i["id"] = x
                    x += 1

        else:
            await interaction.response.send_message(content=f"Can't remove the song you are listening to!, use /skip instead")
    else:
        await interaction.response.send_message(content=f"There is nothing to remove!")
    return queue

async def PauseCommand(interaction: discord.Interaction):
    logs.info(f"Pause command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Pausing!")
    await Player.pause()

async def ResumeCommand(interaction: discord.Interaction):
    logs.info(f"Resume command was called by: {interaction.user}")
    await interaction.response.send_message(f"Resuming...")
    await Player.resume()

async def SkipCommand(interaction: discord.Interaction, client):
    logs.info(f"Skip command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Skipping...")
    voiceclient = client.voice_clients[0]
    if not voiceclient.is_playing():
        await interaction.followup.send("Nothing is playing!")
    else:
        await Player.skip(interaction, client)


async def StopCommand(interaction: discord.Interaction):
    logs.info(f"Stop command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Stopping and Clearing Queue...")
    await Player.stop()

async def RestartCommand(interaction: discord.Interaction, client):
    logs.info(f"Restart command was called! by: {interaction.user}")
    await interaction.response.send_message(f"Restarting...")
    await Player.restart(interaction, client)

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

async def JoinCommand(interaction: discord.Interaction):
    logs.info(f"Join command was called! by: {interaction.user}")
    if interaction.user.voice == None:
        embed = discord.Embed(title="Something Went Wrong!", description= "You're not in a voice channel")
        await interaction.response.send_message(embed=embed)
    else:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Joined!")

async def NowPlayingCommand(interaction: discord.Interaction, client):
    logs.info(f"Now Playing command was called! by: {interaction.user}")
    await interaction.response.send_message("Thinking...")
    voiceclient: discord.VoiceClient = client.voice_clients[0]
    if not voiceclient.is_playing():
        await embeds.CreateEmbedPlaying(interaction, g.variables["nowplaying"], False)
    else:
        await interaction.followup.send("we aren't playing anything!")
