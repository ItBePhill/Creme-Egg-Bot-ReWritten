#Creme Egg Bot ReWritten
#Imports------------------------------------------
import discord
from discord import app_commands
import yt_dlp as youtube_dl
import os
import logs
import platform
import CremeModules
import multiprocessing as mp
#-------------------------------------------------

#Initialisation-----------------------------------
#Function that starts the bot
#Discord Crap
botprocess: mp.Process = None
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
def runbot(process):
    global botprocess
    botprocess = process
    with open(f"{os.getcwd()}/key.txt", "r") as r:
      TOKEN = r.readlines()[0]
      r.close()
    logs.info("\n\nStarting The Bot")
    client.run(TOKEN)
    return botprocess
#-------------------------------------------------
@client.event
async def on_ready():
    CremeModules.MusicModule.init(client)
    await tree.sync(guild=discord.Object(id=1014812996226256927))
    if "Windows" in platform.platform(True, True):
      await client.get_channel(1105906381552369725).send(f"Connected!")
    else:
      await client.get_channel(1109167764981174343).send(f"Connected!")
    logs.info("Connected!")
    await client.change_presence(status = discord.Status.online, activity=discord.Activity(type = discord.ActivityType.listening, name = "Nothing"))
@tree.command(name = "module_info", description="get all the information for a specified module", guild = discord.Object(id=1014812996226256927))
@app_commands.describe(
    name='The name of the module',
)
async def module_info(interaction: discord.Interaction, name: str):
  await CremeModules.module_info(interaction, name)

@tree.command(name = "update_bot", description="Update the bot", guild = discord.Object(id=1014812996226256927))
async def update(interaction: discord.Interaction):
  await CremeModules.UpdateCommand(interaction) 

@tree.command(name = "restart-bot", description="Restart the bot", guild = discord.Object(id=1014812996226256927))
async def update(interaction: discord.Interaction):
  await interaction.response.defer()
  await CremeModules.Restart(interaction, botprocess) 


@tree.command(name = "test_command", description="Test Command Please Ignore", guild = discord.Object(id=1014812996226256927))
async def testcommand(interaction: discord.Interaction):
  await interaction.response.send_message("Test Command")
  data = await CremeModules.MusicModule.get_info_ytdlp("https://www.youtube.com/watch?v=mZD6xxq-eyI")
  print(data["thumbnail"])

if CremeModules.BaseModule.enabled == True:
  @tree.command(name="roll", description="Generate a random number from the min and max", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      minimum="The minimum value the number can be",
      maximum="The maximum value the number can be",
      amount="Amount of times to roll",
  )
  async def roll(interaction: discord.Interaction, minimum: int, maximum: int, amount : int):
      await CremeModules.BaseModule.roll(interaction, minimum, maximum, amount)

  @tree.command(name= "flip", description="Flip a coin", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      amount="Amount of times to flip",
  )
  async def flip(interaction: discord.Interaction, amount: int):
     await CremeModules.BaseModule.flip(interaction, amount)

if CremeModules.MovieModule.enabled == True:
  @tree.command(name = "shows", description="Edit / Add A Movie / Show", guild = discord.Object(id=1014812996226256927))
  async def ShowsCommand(interaction: discord.Interaction):
    await CremeModules.MovieModule.ShowsCommand(interaction)


if CremeModules.MusicModule.enabled == True:
  @tree.command(name = "play", description="Play a Song", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      query="The song you want to play",
  )
  async def PlayCommand(interaction: discord.Interaction, query: str):
    await CremeModules.MusicModule.PlayCommand(interaction, query, client)

  @tree.command(name = "queue", description="Show the Queue", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.QueueCommand(interaction)
  
  @tree.command(name = "shuffle", description="Shuffle the Queue", guild = discord.Object(id=1014812996226256927))
  async def ShuffleCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.ShuffleCommand(interaction)
  
  @tree.command(name = "remove", description="Remove a Song from the Queue", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      index="The position of the song you wan to remove",
  )
  async def RemoveCommand(interaction: discord.Interaction, index: int):
    await CremeModules.MusicModule.RemoveCommand(interaction, index)

  @tree.command(name = "pause", description="Pause the Current Song", guild = discord.Object(id=1014812996226256927))
  async def PauseCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.PauseCommand(interaction)
  
  @tree.command(name = "resume", description="Resume the Current Song", guild = discord.Object(id=1014812996226256927))
  async def ResumeCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.ResumeCommand(interaction)

  @tree.command(name = "skip", description="Skip the Current Song", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.SkipCommand(interaction, client)
  
  @tree.command(name = "stop", description="Stop the Current Song and Clear the Queue", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.StopCommand(interaction)
  
  @tree.command(name = "restart", description="Restart the Current Song", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.RestartCommand(interaction, client)

  @tree.command(name = "leave", description="Leave the Voice Channel", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.LeaveCommand(interaction, client)

  @tree.command(name = "join", description="Join the Voice Channel", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.JoinCommand(interaction)
  
  @tree.command(name = "nowplaying", description="Show Information on the Currently Playing Song", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.NowPlayingCommand(interaction, client)
  
  @tree.command(name = "info", description="Info from a song in the queue", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      index="The Position of the song you want the information for",
  )
  async def InfoCommand(interaction: discord.Interaction, index: int):
    await CremeModules.MusicModule.InfoCommand(interaction, index)

  @tree.command(name = "playfile", description="Play a file from your computer", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
     file = "The file to play",
  )
  async def PlayFileCommand(interaction: discord.Interaction, file: discord.Attachment):
    await CremeModules.MusicModule.PlayFileCommand(interaction, file,  client)

# if not "Linux" in platform.platform(True, True):
#   runbot()