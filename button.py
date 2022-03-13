import discord


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='Confirmed ✅', color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='Cancelled ❌', color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.value = False
        self.stop()


class Next(discord.ui.View):
    def __init__(self, func):
        super().__init__()
        self.func = func

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        val = await self.func()
        if isinstance(val, discord.Embed):
            await interaction.response.edit_message(embed=val)
        else:
            await interaction.response.edit_message(val)

    @discord.ui.button(label='Stop Interaction', style=discord.ButtonStyle.grey)
    async def stop_interaction_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Interaction halted.", ephemeral=True)
        self.stop()

#     async def on_timeout(self, interaction) -> None:
#         for child in self.children:
#             child.disabled = True
#         await interaction.response.edit_message(view=self)
#
#
# class ReRoll(discord.ui.View):
#     super().__init__()
#
#     @discord.ui.button(label='Reroll', style=discord.ButtonStyle.green)
