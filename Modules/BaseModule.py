#Module Base
import logs
import discord
import random
import os
import database
logs.info("Base Module Started Successfully!")
enabled = True
def running():
    return True

async def roll(interaction : discord.Interaction, minimum, maximum, amount):
    logs.info(f"roll command was called! by: {interaction.user}, with arguments: {minimum} | {maximum} | {amount}")
    if minimum > maximum:
          await interaction.response.send_message("The min can't be higher than the max")
    else:
        await interaction.response.send_message("Rolling...")
        for i in range(0, amount):
            await interaction.channel.send(f"{i+1} = {random.randint(minimum, maximum)}")

async def flip(interaction: discord.Interaction, amount: int):
    logs.info(f"roll command was called! by: {interaction.user}, with arguments: {amount}")
    await interaction.response.send_message("Flipping a coin...")
    for i in range(0, amount):
        if random.randint(0, 100) > 50:
            await interaction.channel.send(f"{i+1} = Heads")
        else:
            await interaction.channel.send("{i+1} = Tails")

async def register(interaction: discord.Interaction):
    logs.info(f"register command was called by: {interaction.user}")
    
