#Creme Modules Base
import os
import logs
import os
import subprocess
import discord
from Modules import *
from inspect import getmembers, isfunction
import asyncio
import sys
import platform
logs.info("Creme Modules Base has started!")



async def module_info(interaction: discord.Interaction, name):
    await interaction.response.defer()
    logs.info(f"module_info was called! by: {interaction.user} module: {name}")
    embed = discord.Embed(title=f"{name} info")
    embed.add_field(name = "Module Name",  value = name)
    embed.add_field(name = "Available Functions", value = getmembers(eval(name), isfunction))
    embed.add_field(name = "Enabled", value =  eval(name).enabled)
    running = None
    try:
        eval(name).running()
    except Exception as e:
        running = False
    else:
        running = True
    embed.add_field(name = "Running", value = running)
    await interaction.followup.send(embed=embed)

async def UpdateCommand(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        output = subprocess.check_output("git pull", shell = True)
    except Exception as e:
        await interaction.followup.send(str(e))
    await interaction.followup.send(output)
    await Restart(interaction)

async def Restart(interaction):
        await interaction.followup.send(content = "Restarting... in")
        await interaction.channel.send("3")
        await asyncio.sleep(1)
        await interaction.channel.send("2")
        await asyncio.sleep(1)
        await interaction.channel.send("1")
        await asyncio.sleep(1)
        await interaction.channel.send("Restarting (It may take a while for the bot to start up again\n(It will message connected when it has started up)")
        if platform.platform() == "Linux":
            os.execl("/usr/bin/python3", 'python', "Creme Egg Bot ReWritten.py", *sys.argv[1:])
        else:
            os.execl(sys.executable, 'python', "Creme Egg Bot ReWritten.py", *sys.argv[1:])
