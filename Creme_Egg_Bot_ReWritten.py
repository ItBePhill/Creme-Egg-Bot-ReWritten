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
MY_GUILD = discord.Object(id=1014812996226256927)
botprocess: mp.Process = None
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type = discord.ActivityType.listening, name = "Nothing", state="by: Noone", assets = {"large_image":"creme_egg", "small_image":"play"})
        self.status = discord.Status.online

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        logs.info("Connected!")
        
intents = discord.Intents.all()
client = MyClient(intents=intents)

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
@client.tree.command(name = "module_info", description="get all the information for a specified module", guild = discord.Object(id=1014812996226256927))
@app_commands.describe(
    name='The name of the module',
)
async def module_info(interaction: discord.Interaction, name: str):
  await CremeModules.module_info(interaction, name)

@client.tree.command(name = "update_bot", description="Update the bot", guild = discord.Object(id=1014812996226256927))
async def update(interaction: discord.Interaction):
  await CremeModules.UpdateCommand(interaction) 

@client.tree.command(name = "restart-bot", description="Restart the bot", guild = discord.Object(id=1014812996226256927))
async def update(interaction: discord.Interaction):
  await interaction.response.defer()
  await CremeModules.Restart(interaction, botprocess) 


@client.tree.command(name = "test_command", description="Test Command Please Ignore", guild = discord.Object(id=1014812996226256927))
async def testcommand(interaction: discord.Interaction):
  await interaction.response.send_message("Test Command")
  data = await CremeModules.MusicModule.get_info_ytdlp("https://www.youtube.com/watch?v=mZD6xxq-eyI")
  print(data["thumbnail"])

if CremeModules.BaseModule.enabled == True:
  @client.tree.command(name="roll", description="Generate a random number from the min and max", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      minimum="The minimum value the number can be",
      maximum="The maximum value the number can be",
      amount="Amount of times to roll",
  )
  async def roll(interaction: discord.Interaction, minimum: int, maximum: int, amount : int):
      await CremeModules.BaseModule.roll(interaction, minimum, maximum, amount)

  @client.tree.command(name= "flip", description="Flip a coin", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      amount="Amount of times to flip",
  )
  async def flip(interaction: discord.Interaction, amount: int):
     await CremeModules.BaseModule.flip(interaction, amount)

  # @client.tree.command(name= "register", description="register your date of birth with the bot!", guild = discord.Object(id=1014812996226256927))
  # async def register(interaction: discord.Interaction):
  #    await CremeModules.BaseModule.register(interaction)

if CremeModules.MovieModule.enabled == True:
  @client.tree.command(name = "shows", description="Edit / Add A Movie / Show", guild = discord.Object(id=1014812996226256927))
  async def ShowsCommand(interaction: discord.Interaction):
    await CremeModules.MovieModule.ShowsCommand(interaction)


if CremeModules.MusicModule.enabled == True:
  @client.tree.command(name = "play", description="Play a video", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      query = "The video you want to play",
      starttime = "The time to start the video at in seconds P.S. (by default will be set to 0)",
  )
  async def PlayCommand(interaction: discord.Interaction, query: str, starttime: float|None):
    if starttime == None:
      starttime = 0
    await CremeModules.MusicModule.PlayCommand(interaction, query, starttime, client)

  @client.tree.command(name = "queue", description="Show the Queue", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.QueueCommand(interaction)
  
  @client.tree.command(name = "creme_egg_wrapper", description="Show a list of the most listened to videos", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.WrappedCommand(interaction)
  



  # --------------------------------------------- Not finished -----------------------------------------------------------
  # @client.tree.command(name = "change_queue", description="Change to another queue", guild = discord.Object(id=1014812996226256927))
  # @app_commands.describe(
  #     index = "Index of queue to change to",
  #     continue_ = "Whether the bot will continue playing where you left off on the queue (True by default)",
  # )
  # async def ChangeQueueCommand(interaction: discord.Interaction, index: int, continue_: bool|None):
  #   if continue_ == None:
  #     continue_ = True
  #   await CremeModules.MusicModule.ChangeQueueCommand(interaction, index, continue_)
  # @app_commands.describe(
  #     change = "Whether to change to the new queue after it is created (True by default)",
  # )
  # @client.tree.command(name = "create_queue", description="Create a new Queue", guild = discord.Object(id=1014812996226256927))
  # async def CreateQueueCommand(interaction: discord.Interaction, change: bool|None):
  #   if change == None:
  #     change = True
  #   await CremeModules.MusicModule.CreateQueueCommand(interaction, client, change)
  # ----------------------------------------------------------------------------------------------------------------------
  
  @client.tree.command(name = "list_queues", description="list queues", guild = discord.Object(id=1014812996226256927))
  async def CreateQueueCommand(interaction: discord.Interaction, change: bool|None):
    if change == None:
      change = True
    await CremeModules.MusicModule.CreateQueueCommand(interaction, client, change)
  
  
  @client.tree.command(name = "shuffle", description="Shuffle the Queue", guild = discord.Object(id=1014812996226256927))
  async def ShuffleCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.ShuffleCommand(interaction)
  
  @client.tree.command(name = "remove", description="Remove a video from the Queue", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      index="The position of the video you wan to remove",
  )
  async def RemoveCommand(interaction: discord.Interaction, index: int):
    await CremeModules.MusicModule.RemoveCommand(interaction, index)

  @client.tree.command(name = "pause", description="Pause the Current video", guild = discord.Object(id=1014812996226256927))
  async def PauseCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.PauseCommand(interaction)
  
  @client.tree.command(name = "resume", description="Resume the Current video", guild = discord.Object(id=1014812996226256927))
  async def ResumeCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.ResumeCommand(interaction)

  @client.tree.command(name = "skip", description="Skip the Current video", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.SkipCommand(interaction, client)
  
  @client.tree.command(name = "stop", description="Stop the Current video and Clear the Queue", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.StopCommand(interaction)
  
  @client.tree.command(name = "restart", description="Restart the Current video", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.RestartCommand(interaction, client)

  @client.tree.command(name = "leave", description="Leave the Voice Channel", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.LeaveCommand(interaction, client)

  @client.tree.command(name = "join", description="Join the Voice Channel", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.JoinCommand(interaction)
  
  @client.tree.command(name = "now_playing", description="Show Information on the Currently Playing video", guild = discord.Object(id=1014812996226256927))
  async def QueueCommand(interaction: discord.Interaction):
    await CremeModules.MusicModule.NowPlayingCommand(interaction, client)
  
  @client.tree.command(name = "info", description="Info from a video in the queue", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
      index="The Position of the video you want the information for",
  )
  async def InfoCommand(interaction: discord.Interaction, index: int):
    await CremeModules.MusicModule.InfoCommand(interaction, index)

  @client.tree.command(name = "playfile", description="Play a file from your computer", guild = discord.Object(id=1014812996226256927))
  @app_commands.describe(
     file = "The file to play",
  )
  async def PlayFileCommand(interaction: discord.Interaction, file: discord.Attachment):
    await CremeModules.MusicModule.PlayFileCommand(interaction, file,  client)

# if not "Linux" in platform.platform(True, True):
#   runbot()