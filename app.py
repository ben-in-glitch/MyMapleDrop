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

#-----------------------------------------------------bosses-----------------------------------------------------
@tree.command(name="create_boss", description ="Create a new boss")
@app_commands.choices(
    difficulty=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Normal", value="normal"),
        app_commands.Choice(name="Hard", value="hard"),
        app_commands.Choice(name="Extreme", value="extreme")
    ]
    )
async def create_boss(interaction: discord.Interaction, boss_name: str, difficulty: app_commands.Choice[str]):
    try:
        boss = services.BossService(boss_repo).create(boss_name.strip(), difficulty.value)
        message = f"Boss ({boss.boss}) created successfully!"
    except (services.BossAlreadyExistsError, services.BossNotFoundError):
        message = "Failed to create boss."
    await interaction.response.send_message(message)

async def boss_autocomplete(interaction: discord.Interaction, current: str):
    bosses = boss_repo.get_all_bosses()
    return [
        app_commands.Choice(name=f"{boss.boss} ({boss.difficulty})", value=str(boss.id))
        for boss in bosses if current.lower() in boss.boss.lower()
    ]

@tree.command(name="update_boss", description ="Update a boss")
@app_commands.autocomplete(boss=boss_autocomplete)
@app_commands.choices(
    new_difficulty=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Normal", value="normal"),
        app_commands.Choice(name="Hard", value="hard"),
        app_commands.Choice(name="Extreme", value="extreme")
    ]
    )
async def update_boss(interaction: discord.Interaction, boss: str, new_boss_name: str = None, new_difficulty: app_commands.Choice[str] = None):
    try:
        boss = services.BossService(boss_repo).update(int(boss),
                                                      new_boss_name.strip() if new_boss_name else None,
                                                      new_difficulty.value if new_difficulty else None)
        message = f"Boss ({boss.boss}) updated successfully!"
    except (services.BossAlreadyExistsError, services.BossNotFoundError):
        message = "Failed to update boss."
    await interaction.response.send_message(message)

#-----------------------------------------------------items-----------------------------------------------------
@tree.command(name="create_item", description ="Create a new item")
async def create_item(interaction: discord.Interaction, item: str):
    try:
        item_obj = services.ItemService(item_repo).create(item.strip())
        message = f"Item ({item_obj.item}) created successfully!"
    except (services.ItemAlreadyExistsError, services.ItemNotFoundError):
        message = "Failed to create item."
    await interaction.response.send_message(message)

async def item_autocomplete(interaction: discord.Interaction, current: str):
    items = item_repo.get_all_items()
    return [
        app_commands.Choice(name=f"{item.item}", value=str(item.id))
        for item in items if current.lower() in item.item.lower()
    ]

@tree.command(name="update_item", description ="Update an item")
@app_commands.autocomplete(item_id=item_autocomplete)
async def update_item(interaction: discord.Interaction, item_id: int, new_item_name: str):
    try:
        item_obj = services.ItemService(item_repo).update(int(item_id), new_item_name.strip())
        message = f"Item ({item_obj.item}) updated successfully!"
    except (services.ItemAlreadyExistsError, services.ItemNotFoundError):
        message = "Failed to update item."
    await interaction.response.send_message(message)


#-----------------------------------------------------on_ready-----------------------------------------------------
@client.event
async def on_ready():
    tree.copy_global_to(guild=guild)
    synced = await tree.sync(guild=guild)
    print(f"{client.user} is logged in")
    print(f"synced {len(synced)} commands")




client.run(token)