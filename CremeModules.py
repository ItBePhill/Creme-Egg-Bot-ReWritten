#Creme Modules Base
import os
import logs
import os
import subprocess
import discord
from Modules import *
from inspect import getmembers, isfunction
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
