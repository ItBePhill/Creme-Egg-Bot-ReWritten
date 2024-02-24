#Movie Module
import logs
import discord
import os
import json
logs.info("Movie Module Started Successfully!")
enabled = True
def running():
    return True


async def ShowsCommand(interaction: discord.Interaction):
    async def Edit(i, ii):
        logs.info(f"{i.user} selected Edit")
        async def selected(select: discord.ui.Select, i: discord.Interaction, ii: discord.Interaction):
            async def button(i: discord.Interaction, ii: discord.Interaction):
                    await i.response.send_modal(nameep())
            await i.response.send_message("Thinking...", ephemeral=True)
            await i.delete_original_response()
            entry = dicts[int(select.values[0])]
            class nameep(discord.ui.Modal, title = f"Editing: {entry['name']}"):
                name = discord.ui.TextInput(label = "Name", placeholder = entry["name"])
                episode = discord.ui.TextInput(label = "Episode", placeholder =  entry["episode"])

                hours = discord.ui.TextInput(label = "Hours", placeholder = entry["time"].split(":")[0])
                minutes = discord.ui.TextInput(label = "Minutes", placeholder =  entry["time"].split(":")[1])
                seconds = discord.ui.TextInput(label = "Seconds", placeholder = entry["time"].split(":")[2])    
                async def on_submit(self, interaction: discord.Interaction):
                    newentry = {}
                    newentry["name"] = self.name.value
                    newentry["episode"] = self.episode.value
                    newentry["time"] = f"{self.hours.value}:{self.minutes.value}:{self.seconds.value}"

                    logs.info(f"Deleting {entry['name']}.json")
                    os.remove(f"Json/{entry['name']}.json")
                    logs.info(f"Creating {newentry['name']}.json")
                    with open(f"Json/{newentry['name']}.json", "w") as f:
                        json.dump(newentry, f)
                        f.close()
                        

                    embed = discord.Embed(title = f"New Options for: {entry['name']}")
                    embed.add_field(name = "Name", value = newentry["name"])
                    embed.add_field(name = "Episode", value = newentry["episode"])
                    embed.add_field(name = "Time", value = newentry["time"])
                    await interaction.response.send_message(embed = embed)
                
            logs.info(f"Picked: {entry}")
            embed = discord.Embed(title = f"Editing: {entry['name']}")
            embed.add_field(name = "Name", value = entry["name"])
            embed.add_field(name = "Episode", value = entry["episode"])
            embed.add_field(name = "Time", value = entry["time"])
            view = discord.ui.View()
            editbutton =  discord.ui.Button(label= "Edit")
            editbutton.callback = lambda i: button(i, interaction)
            view.add_item(editbutton)
            await ii.edit_original_response(embed = embed, view = view)
        await i.response.send_message("Thinking...", ephemeral=True)
        await i.delete_original_response()
        embed = discord.Embed(title = "Choose a show or movie")
        view = discord.ui.View()
        selectionbox =  discord.ui.Select(min_values=1, max_values=1)
        selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
        dicts = []
        x = 0
        for i in os.listdir("Json"):
            with open(os.path.join("Json", i), "r") as f:
                data = json.load(f)
                dicts.append(data)
            x+=1
            
        
        x = 0
        for i in dicts:
            selectionbox.add_option(label = i["name"],  value = str(x))
            x+=1
        
        view.add_item(selectionbox)
        await ii.edit_original_response(embed=embed, view=view)

    
    async def New(i, ii):
        logs.info(f"{i.user} selected New")
        class nameep(discord.ui.Modal, title = f"Adding A New Show/Movie:"):
            name = discord.ui.TextInput(label = "Name", placeholder = "Enter Name Here...")
            episode = discord.ui.TextInput(label = "Episode", placeholder =  "Enter Episode Here")

            hours = discord.ui.TextInput(label = "Hours", placeholder = "Enter Hours Here...")
            minutes = discord.ui.TextInput(label = "Minutes", placeholder =  "Enter Minutes Here...")
            seconds = discord.ui.TextInput(label = "Seconds", placeholder = "Enter Seconds Here...")    
            async def on_submit(self, interaction: discord.Interaction):
                newentry = {}
                newentry["name"] = self.name.value
                newentry["episode"] = self.episode.value
                newentry["time"] = f"{self.hours.value}:{self.minutes.value}:{self.seconds.value}"
                logs.info(f"Creating {newentry['name']}.json")
                with open(f"Json/{newentry['name']}.json", "w") as f:
                    json.dump(newentry, f)
                    f.close()
                    

                embed = discord.Embed(title = f"Adding: {newentry['name']}")
                embed.add_field(name = "Name", value = newentry["name"])
                embed.add_field(name = "Episode", value = newentry["episode"])
                embed.add_field(name = "Time", value = newentry["time"])
                await interaction.response.send_message(embed = embed)
        await i.response.send_modal(nameep())
    async def View(i, ii):
        logs.info(f"{i.user} selected View")
        async def selected(select, i: discord.Interaction, ii: discord.Interaction):
            await i.response.send_message("Thinking...", ephemeral=True)
            await i.delete_original_response()
            entry = dicts[int(select.values[0])]
            logs.info(f"Picked: {entry}")
            embed = discord.Embed(title = f"Viewing: {entry['name']}")
            embed.add_field(name = "Name", value = entry["name"])
            embed.add_field(name = "Episode", value = entry["episode"])
            embed.add_field(name = "Time", value = entry["time"])
            await ii.edit_original_response(embed = embed, view = view)

        await i.response.send_message("Thinking...", ephemeral=True)
        await i.delete_original_response()
        embed = discord.Embed(title = "Choose a show or movie")
        view = discord.ui.View()
        selectionbox =  discord.ui.Select(min_values=1, max_values=1)
        selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
        dicts = []
        x = 0
        for i in os.listdir("Json"):
            with open(os.path.join("Json", i), "r") as f:
                data = json.load(f)
                dicts.append(data)
            x+=1
        
        x = 0
        for i in dicts:
            selectionbox.add_option(label = i["name"],  value = str(x))
            x+=1
        
        view.add_item(selectionbox)
        await ii.edit_original_response(embed=embed, view=view)

    async def Remove(i: discord.Interaction, ii: discord.Interaction):
        logs.info(f"{i.user} selected Remove")
        async def selected(select, i: discord.Interaction, ii: discord.Interaction):
            await i.response.send_message("Thinking...", ephemeral=True)
            await i.delete_original_response()
            entry = dicts[int(select.values[0])]
            logs.info(f"Picked: {entry}")
            embed = discord.Embed(title = f"Removing: {entry['name']}")
            embed.add_field(name = "Name", value = entry["name"])
            embed.add_field(name = "Episode", value = entry["episode"])
            embed.add_field(name = "Time", value = entry["time"])
            await ii.edit_original_response(embed = embed, view = None)

            message = await ii.channel.send(f"Removing... {entry['name']}")
            logs.info(f"Removing {entry['name']}.json")
            os.remove(f"Json/{entry['name']}.json")
            await message.edit(content = f"Removed... {entry['name']}", embed = None, view = None)

        await i.response.send_message("Thinking...", ephemeral=True)
        await i.delete_original_response()
        embed = discord.Embed(title = "Choose a show or movie")
        view = discord.ui.View()
        selectionbox =  discord.ui.Select(min_values=1, max_values=1)
        selectionbox.callback = lambda i: selected(selectionbox, i, interaction)
        dicts = []
        x = 0
        for i in os.listdir("Json"):
            with open(os.path.join("Json", i), "r") as f:
                data = json.load(f)
                dicts.append(data)
            x+=1
        
        x = 0
        for i in dicts:
            selectionbox.add_option(label = i["name"],  value = str(x))
            x+=1
        
        view.add_item(selectionbox)
        await ii.edit_original_response(embed=embed, view=view)
    logs.info(f"Shows command was called! by: {interaction.user}")
    try:
        embed = discord.Embed(title = "Add / Edit a Movie / Show")
        embed.description = "Select a show / movie to edit or create a new one"
        newButton =  discord.ui.Button(label = "New")
        editButton =  discord.ui.Button(label = "Edit")
        viewbutton = discord.ui.Button(label = "View")
        removebutton = discord.ui.Button(label = "Remove")
        newButton.callback = lambda i: New(i, interaction) 
        editButton.callback = lambda i: Edit(i, interaction)
        viewbutton.callback = lambda i: View(i, interaction)
        removebutton.callback = lambda i: Remove(i, interaction)
        view = discord.ui.View()
        view.add_item(newButton)
        view.add_item(editButton)
        view.add_item(viewbutton)
        view.add_item(removebutton)
        await interaction.response.send_message(embed=embed, view=view)
    except Exception as e:
        await interaction.channel.send(e)




