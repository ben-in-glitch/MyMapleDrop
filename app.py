import discord
from discord import app_commands
from config import token, guild_id  
import db, model

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.Object(id=guild_id)

@tree.command(name="hello", description ="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

@tree.command(name="register", description ="Register a new user")
async def register(interaction: discord.Interaction, username: str):
    user = model.Users(dc_id=interaction.user.id, username=username)
    req = db.create_user(user)
    if req:
        message = f"User ({user.username}) registered successfully!"
    else:
        message = f"Failed to register user ({user.username})."

    await interaction.response.send_message(message)

@tree.command(name="update_username", description ="Update your username")
async def update_username(interaction: discord.Interaction, new_username: str):
    user = model.Users(username=new_username, dc_id=interaction.user.id)
    req = db.update_user(user)
    if req:
        message = f"Username updated to ({new_username}) successfully!"
    else:
        message = f"Failed to update username."

    await interaction.response.send_message(message)

@tree.command(name="create_avator", description ="Create a new avator")
async def create_avator(interaction: discord.Interaction, avator: str, job: str, cur_channel: str):
    user = db.get_user_by_dc_id(interaction.user.id)
    if not user:
        await interaction.response.send_message("You need to register first using /register command.")
        return

    avator_obj = model.Avators(user_id=user.id, avator=avator, job=job, cur_channel=cur_channel)
    req = db.create_avator(avator_obj)
    if req:
        message = f"Avator ({avator}) created successfully!"
    else:
        message = f"Failed to create avator ({avator})."

    await interaction.response.send_message(message)

@tree.command(name="update_avator", description ="Update your avator")
async def update_avator(interaction: discord.Interaction, avator: str, job: str, cur_channel: str):
    user = db.get_user_by_dc_id(interaction.user.id)
    if not user:
        await interaction.response.send_message("You need to register first using /register command.")
        return

    avator_obj = model.Avators(user_id=user.id, avator=avator, job=job, cur_channel=cur_channel)
    req = db.update_avator(avator_obj)
    if req:
        message = f"Avator updated to ({avator}) successfully!"
    else:
        message = f"Failed to update avator."

    await interaction.response.send_message(message)

@client.event
async def on_ready():
    tree.copy_global_to(guild=guild)
    synced = await tree.sync(guild=guild)
    print(f"{client.user} is logged in")
    print(f"synced {len(synced)} commands")




client.run(token)