import discord
from discord import app_commands
from config import token, guild_id, db_pool
import services
from repositories import UserRepository, AvatorRepository, ItemRepository, BossRepository, DropRepository, Drop_participantRepository

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.Object(id=guild_id)
user_repo = UserRepository(db_pool)
avator_repo = AvatorRepository(db_pool)
item_repo = ItemRepository(db_pool)
boss_repo = BossRepository(db_pool)
drop_repo = DropRepository(db_pool)
drop_participants_repo = Drop_participantRepository(db_pool)

@tree.command(name="hello", description ="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

@tree.command(name="register", description ="Register a new user")
async def register(interaction: discord.Interaction, username: str):
    try:
        user = services.UserService(user_repo).register(interaction.user.id, username.strip())
        message = f"User ({user.username}) registered successfully!"

    except (services.UserAlreadyExistedError, services.UserNameALreadyExistedError):
        message = "Failed to register user."

    await interaction.response.send_message(message)

@tree.command(name="update_username", description ="Update your username")
async def update_username(interaction: discord.Interaction, new_username: str):
    try:
        user = services.UserService(user_repo).update_username(interaction.user.id, new_username.strip())
        message = f"Username updated to ({user.username}) successfully!"
    except (services.UserNotRegisteredError, services.UserNameALreadyExistedError):
        message = "Failed to update username."

    await interaction.response.send_message(message)

@tree.command(name="create_avator", description ="Create a new avator")
async def create_avator(interaction: discord.Interaction, avator: str, job: str, cur_channel: str):
    try:
        avator_obj = services.AvatorService(avator_repo).create(interaction.user.id,
                                                                avator.strip(),
                                                                job.strip(),
                                                                cur_channel.strip())
        message = f"Avator ({avator_obj.avator}) created successfully!"
    except (services.AvatorAlreadyExistsError, services.UserNotRegisteredError):
        message = f"Failed to create avator."

    await interaction.response.send_message(message)

@tree.command(name="update_avator", description ="Update your avator")
async def update_avator(interaction: discord.Interaction, new_avator:str = None, new_job:str = None, new_channel:str = None):
    try:
        avator_obj = services.AvatorService(avator_repo).update(interaction.user.id,
                                                                new_avator.strip() if new_avator else None,
                                                                new_job.strip() if new_job else None,
                                                                new_channel.strip() if new_channel else None)
        message = f"Avator ({avator_obj.avator}) updated successfully!"
    except (services.AvatorAlreadyExistsError, services.UserNotRegisteredError):
        message = f"Failed to update avator."
    await interaction.response.send_message(message)

@client.event
async def on_ready():
    tree.copy_global_to(guild=guild)
    synced = await tree.sync(guild=guild)
    print(f"{client.user} is logged in")
    print(f"synced {len(synced)} commands")




client.run(token)