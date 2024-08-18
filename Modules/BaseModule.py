#Module Base
import logs
import discord
import random
import os
import database
import database as db
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


# Not finished / might scrap
# async def register(interaction: discord.Interaction):
#     logs.info(f"register command was called by: {interaction.user}")
#     async def Edit(i, ii):
#         logs.info(f"{i.user} selected Edit")
#         async def selected(select: discord.ui.Select, i: discord.Interaction, ii: discord.Interaction):
#             async def button(i: discord.Interaction, ii: discord.Interaction):
#                     await i.response.send_modal(nameep())
#             await i.response.send_message("Thinking...", ephemeral=True)
#             await i.delete_original_response()
#             entry = dicts[int(select.values[0])]
#             class nameep(discord.ui.Modal, title = f"Editing: {entry['name']}"):
#                 name = discord.ui.TextInput(label = "Name", placeholder = entry["name"])
#                 dob = discord.ui.TextInput(label = "dob", placeholder =  entry["dob"])
#                 colour = discord.ui.TextInput(label =  "colour", placeholder = entry["colour"])
#                 async def on_submit(self, interaction: discord.Interaction):
#                     newentry = {}
#                     newentry["name"] = self.name.value
#                     newentry["dob"] = self.dob.value
#                     newentry["colour"] = self.colour.value

#                     db.ShowData.DB("u", newentry)
                    
#                     embed = discord.Embed(title = f"New Options for: {entry['name']}")
#                     embed.add_field(name = "Name", value = newentry["name"])
#                     embed.add_field(name = "dob", value = newentry["dob"])
#                     embed.add_field(name = "colour", value = newentry["colour"])
#                     await interaction.response.send_message(embed = embed)
                
#             logs.info(f"Picked: {entry}")
#             embed = discord.Embed(title = f"Editing: {entry['name']}")
#             embed.add_field(name = "Name", value = entry["name"])
#             embed.add_field(name = "dob", value = entry["dob"])
#             embed.add_field(name = "colour", value = entry["colour"])
#             view = discord.ui.View()
#             editbutton =  discord.ui.Button(label= "Edit")
#             editbutton.callback = lambda i: button(i, interaction)
#             view.add_item(editbutton)
#             await ii.edit_original_response(embed = embed, view = view)
#         await i.response.send_message("Thinking...", ephemeral=True)
#         await i.delete_original_response()
#         embed = discord.Embed(title = "Choose a User")
#         view = discord.ui.View()
#         selectionbox =  discord.ui.Select(min_values=1, max_values=1)
#         selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
#         dicts = []
#         dicts = db.ShowData.load()
#         logs.info(dicts)
#         x = 0
#         for i in dicts:
#             selectionbox.add_option(label = i["name"],  value = str(x))
#             x+=1
        
#         view.add_item(selectionbox)
#         await ii.edit_original_response(embed=embed, view=view)

    
#     async def New(i, ii):
#         logs.info(f"{i.user} selected New")
#         class nameep(discord.ui.Modal, title = f"Adding A New User:"):
#             name = discord.ui.TextInput(label = "Name", placeholder = "Enter Name Here...")
#             dob = discord.ui.TextInput(label = "Date of Birth", placeholder =  "Enter Your Date of Birth Here")

#             Colour = discord.ui.TextInput(label = "Colour", placeholder = "Enter Your Favourite Colour Here...") 
#             async def on_submit(self, interaction: discord.Interaction):
#                 newentry = {}
#                 newentry["name"] = self.name.value
#                 newentry["dob"] = self.dob.value
#                 newentry["colour"] = self.Colour.value
#                 logs.info(f"Creating {newentry['name']}")
                
#                 db.ShowData.DB("a", newentry)
                
#                 embed = discord.Embed(title = f"Adding: {newentry['name']}")
#                 embed.add_field(name = "Name", value = newentry["name"])
#                 embed.add_field(name = "dob", value = newentry["dob"])
#                 embed.add_field(name = "colour", value = newentry["colour"])
#                 await interaction.response.send_message(embed = embed)
#         await i.response.send_modal(nameep())
#     async def View(i, ii):
#         logs.info(f"{i.user} selected View")
#         async def selected(select, i: discord.Interaction, ii: discord.Interaction):
#             await i.response.send_message("Thinking...", ephemeral=True)
#             await i.delete_original_response()
#             entry = dicts[int(select.values[0])]
#             logs.info(f"Picked: {entry}")
#             embed = discord.Embed(title = f"Viewing: {entry['name']}")
#             embed.add_field(name = "Name", value = entry["name"])
#             embed.add_field(name = "dob", value = entry["dob"])
#             embed.add_field(name = "colour", value = entry["colour"])
#             await ii.edit_original_response(embed = embed, view = view)

#         await i.response.send_message("Thinking...", ephemeral=True)
#         await i.delete_original_response()
#         embed = discord.Embed(title = "Choose a User")
#         view = discord.ui.View()
#         selectionbox =  discord.ui.Select(min_values=1, max_values=1)
#         selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
#         dicts = []
#         dicts = db.ShowData.load()
#         logs.info(dicts)
#         x = 0
#         for i in dicts:
#             selectionbox.add_option(label = i["name"],  value = str(x))
#             x+=1
        
#         view.add_item(selectionbox)
#         await ii.edit_original_response(embed=embed, view=view)

#     async def Remove(i: discord.Interaction, ii: discord.Interaction):
#         logs.info(f"{i.user} selected Remove")
#         async def selected(select, i: discord.Interaction, ii: discord.Interaction):
#             await i.response.send_message("Thinking...", ephemeral=True)
#             await i.delete_original_response()
#             entry = dicts[int(select.values[0])]
#             logs.info(f"Picked: {entry}")
#             embed = discord.Embed(title = f"Removing: {entry['name']}")
#             embed.add_field(name = "Name", value = entry["name"])
#             embed.add_field(name = "dob", value = entry["dob"])
#             embed.add_field(name = "colour", value = entry["colour"])
#             await ii.edit_original_response(embed = embed, view = None)

#             message = await ii.channel.send(f"Removing... {entry['name']}")
#             db.ShowData.remove(entry["name"])
#             await message.edit(content = f"Removed... {entry['name']}", embed = None, view = None)

#         await i.response.send_message("Thinking...", ephemeral=True)
#         await i.delete_original_response()
#         embed = discord.Embed(title = "Choose a User")
#         view = discord.ui.View()
#         selectionbox =  discord.ui.Select(min_values=1, max_values=1)
#         selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
#         dicts = []
#         dicts = db.ShowData.load()
#         logs.info(dicts)
#         x = 0
#         for i in dicts:
#             selectionbox.add_option(label = i["name"],  value = str(x))
#             x+=1
        
#         view.add_item(selectionbox)
#         await ii.edit_original_response(embed=embed, view=view)
#     logs.info(f"Shows command was called! by: {interaction.user}")
#     try:
#         embed = discord.Embed(title = "Add / Edit a User")
#         embed.description = "Select a User to edit or create a new one"
#         newButton =  discord.ui.Button(label = "New")
#         editButton =  discord.ui.Button(label = "Edit")
#         viewbutton = discord.ui.Button(label = "View")
#         removebutton = discord.ui.Button(label = "Remove")
#         newButton.callback = lambda i: New(i, interaction) 
#         editButton.callback = lambda i: Edit(i, interaction)
#         viewbutton.callback = lambda i: View(i, interaction)
#         removebutton.callback = lambda i: Remove(i, interaction)
#         view = discord.ui.View()
#         view.add_item(newButton)
#         view.add_item(editButton)
#         view.add_item(viewbutton)
#         view.add_item(removebutton)
#         await interaction.response.send_message(embed=embed, view=view)
#     except Exception as e:
#         await interaction.channel.send(e)
