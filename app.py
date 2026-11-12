import asyncio
import logging
import discord
from discord import app_commands, ui
from config import token, guild_id, db_pool
import services
from repositories import UserRepository, AvatarRepository, ItemRepository, BossRepository, DropRepository, Drop_participantRepository


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.Object(id=guild_id)
user_repo = UserRepository(db_pool)
avatar_repo = AvatarRepository(db_pool)
item_repo = ItemRepository(db_pool)
boss_repo = BossRepository(db_pool)
drop_repo = DropRepository(db_pool)
drop_participants_repo = Drop_participantRepository(db_pool)

@tree.command(name="hello", description ="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

#-----------------------------------------------------users-----------------------------------------------------
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

#-----------------------------------------------------avatars-----------------------------------------------------
@tree.command(name="create_avatar", description ="Create a new avatar")
async def create_avatar(interaction: discord.Interaction, avatar: str, job: str, cur_channel: str):
    try:
        avatar_obj = services.AvatarService(avatar_repo).create(interaction.user.id,
                                                                avatar.strip(),
                                                                job.strip(),
                                                                cur_channel.strip())
        message = f"Avatar ({avatar_obj.avatar}) created successfully!"
    except (services.AvatarAlreadyExistsError, services.UserNotRegisteredError):
        message = f"Failed to create avatar."

    await interaction.response.send_message(message)

@tree.command(name="update_avatar", description ="Update your avatar")
async def update_avatar(interaction: discord.Interaction, new_avatar:str = None, new_job:str = None, new_channel:str = None):
    try:
        avatar_obj = services.AvatarService(avatar_repo).update(interaction.user.id,
                                                                new_avatar.strip() if new_avatar else None,
                                                                new_job.strip() if new_job else None,
                                                                new_channel.strip() if new_channel else None)
        message = f"Avatar ({avatar_obj.avatar}) updated successfully!"
    except (services.AvatarAlreadyExistsError, services.UserNotRegisteredError):
        message = f"Failed to update avatar."
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
        message = f"Boss ({boss.boss} ({boss.difficulty})) created successfully!"
    except (services.BossAlreadyExistsError, services.BossNotFoundError):
        message = "Failed to create boss."
    await interaction.response.send_message(message)

async def boss_autocomplete(interaction: discord.Interaction, current: str):
    bosses = boss_repo.get_all_bosses()
    return [
        app_commands.Choice(name=f"{boss.boss} ({boss.difficulty})", value=str(boss.id))
        for boss in bosses if current.lower() in boss.boss.lower()
    ][:25]

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
        message = f"Boss ({boss.boss} ({boss.difficulty})) updated successfully!"
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
    ][:25]

@tree.command(name="update_item", description ="Update an item")
@app_commands.autocomplete(item_id=item_autocomplete)
async def update_item(interaction: discord.Interaction, item_id: int, new_item_name: str):
    try:
        item_obj = services.ItemService(item_repo).update(int(item_id), new_item_name.strip())
        message = f"Item ({item_obj.item}) updated successfully!"
    except (services.ItemAlreadyExistsError, services.ItemNotFoundError):
        message = "Failed to update item."
    await interaction.response.send_message(message)

#-----------------------------------------------------drops_models-----------------------------------------------------

class AvatarSelect(ui.Select):
    def __init__(self, drop_view, avatars):
        self.drop_view = drop_view
        self.visible_ids = {avatar.id for avatar in avatars}
        super().__init__(
            placeholder="Select participants on this page",
            min_values=0,
            max_values=len(avatars),
            row=0,
            options=[discord.SelectOption(
                label=avatar.avatar[:100],
                description=(avatar.job or "Unknown job")[:100],
                value=str(avatar.id),
                default=avatar.id in drop_view.selected_avatar_ids,
            ) for avatar in avatars],
        )

    async def callback(self, interaction):
        # Replace only this page's selection; keep selections on other pages.
        self.drop_view.selected_avatar_ids.difference_update(self.visible_ids)
        self.drop_view.selected_avatar_ids.update(int(value) for value in self.values)
        self.drop_view.update_controls()
        await interaction.response.edit_message(
            content=self.drop_view.render(), view=self.drop_view
        )


class DropView(ui.View):
    def __init__(self, owner_id, drop_data, item_name, boss_name,
                 avatars, drop_service, open_item_name=None):
        super().__init__(timeout=600)
        self.owner_id = owner_id
        self.drop_data = drop_data
        self.item_name = item_name
        self.boss_name = boss_name
        self.open_item_name = open_item_name
        self.avatars = sorted(avatars, key=lambda avatar: (avatar.avatar.casefold(), avatar.id))
        self.selected_avatar_ids = set()
        self.page = 0
        self.page_count = max(1, (len(self.avatars) + 24) // 25)
        self.drop_service = drop_service
        self.message = None
        self.finished = False
        self.saving = False
        self.status = "Select participants below, then confirm."
        self.update_controls()

    def update_controls(self):
        for child in list(self.children):
            if isinstance(child, AvatarSelect):
                self.remove_item(child)
        page_avatars = self.avatars[self.page * 25:(self.page + 1) * 25]
        if page_avatars:
            self.add_item(AvatarSelect(self, page_avatars))
        self.previous_page.disabled = self.page == 0
        self.next_page.disabled = self.page == self.page_count - 1
        if self.finished or self.saving:
            for child in self.children:
                child.disabled = True

    def render(self):
        names = [discord.utils.escape_markdown(avatar.avatar)
                 for avatar in self.avatars if avatar.id in self.selected_avatar_ids]
        participants = "\n".join(f"? {name}" for name in names) or "No participants selected."
        if len(participants) > 1000:
            participants = participants[:1000] + "\n..."
        return (
            "**Create Drop**\n\n"
            f"**Item:** {discord.utils.escape_markdown(self.item_name)}\n"
            f"**Boss:** {discord.utils.escape_markdown(self.boss_name)}\n"
            f"**Container:** {'Yes' if self.drop_data['is_container'] else 'No'}\n"
            f"**Opened item:** {discord.utils.escape_markdown(self.open_item_name or 'Not specified')}\n"
            f"**Participants ({len(names)})**\n{participants}\n\n"
            f"Page {self.page + 1}/{self.page_count} ? Selections are kept across pages.\n"
            f"{self.status}"
        )

    async def refresh_message(self):
        if self.message:
            await self.message.edit(content=self.render(), view=self)

    async def interaction_check(self, interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("This is not your drop.", ephemeral=True)
            return False
        if self.finished or self.saving:
            await interaction.response.send_message(
                "This drop is already closed or being saved.", ephemeral=True
            )
            return False
        return True

    @ui.button(label="Previous", style=discord.ButtonStyle.secondary, row=1)
    async def previous_page(self, interaction, button):
        self.page = max(0, self.page - 1)
        self.update_controls()
        await interaction.response.edit_message(content=self.render(), view=self)

    @ui.button(label="Next", style=discord.ButtonStyle.secondary, row=1)
    async def next_page(self, interaction, button):
        self.page = min(self.page_count - 1, self.page + 1)
        self.update_controls()
        await interaction.response.edit_message(content=self.render(), view=self)

    @ui.button(label="Confirm", style=discord.ButtonStyle.success, row=1)
    async def confirm(self, interaction, button):
        if not self.selected_avatar_ids:
            await interaction.response.send_message("Please select at least one avatar.", ephemeral=True)
            return
        self.saving = True
        await interaction.response.defer(ephemeral=True)
        self.update_controls()
        try:
            await self.refresh_message()
            drop_id = await asyncio.to_thread(
                self.drop_service.create_with_participants,
                self.drop_data, sorted(self.selected_avatar_ids),
            )
        except Exception:
            logging.exception("Failed to save drop with participants")
            self.saving = False
            self.update_controls()
            await self.refresh_message()
            await interaction.followup.send("Failed to save the drop. Please try again.", ephemeral=True)
            return
        self.finished = True
        self.status = f"Drop #{drop_id} saved successfully!"
        self.update_controls()
        self.stop()
        await self.refresh_message()
        await interaction.followup.send(self.status, ephemeral=True)

    @ui.button(label="Cancel", style=discord.ButtonStyle.danger, row=1)
    async def cancel(self, interaction, button):
        self.finished = True
        self.status = "Drop creation cancelled."
        self.update_controls()
        await interaction.response.edit_message(content=self.render(), view=self)
        self.stop()

    async def on_timeout(self):
        # A save that has started must be allowed to finish.
        if self.saving:
            return
        self.finished = True
        self.status = "Drop creation expired. Run /create_drop to start again."
        self.update_controls()
        try:
            await self.refresh_message()
        except discord.HTTPException:
            pass


#-----------------------------------------------------drops-----------------------------------------------------
@tree.command(name="create_drop", description="Create a new drop")
@app_commands.autocomplete(item=item_autocomplete, boss=boss_autocomplete, open_item=item_autocomplete)
async def create_drop(interaction: discord.Interaction, item: str, boss: str,
                      is_container: bool = False, open_item: str = None):
    await interaction.response.defer(ephemeral=True)
    try:
        item_id = int(item)
        boss_id = int(boss)
        open_item_id = int(open_item) if open_item is not None else None
    except ValueError:
        await interaction.followup.send("Invalid item or boss selection.", ephemeral=True)
        return
    if open_item_id is not None and not is_container:
        await interaction.followup.send("Set is_container to True when specifying open_item.", ephemeral=True)
        return

    def load_options():
        return (
            item_repo.get_item_by_id(item_id),
            boss_repo.get_boss_by_id(boss_id),
            item_repo.get_item_by_id(open_item_id) if open_item_id is not None else None,
            avatar_repo.get_all_avatars(),
        )

    try:
        item_obj, boss_obj, open_item_obj, avatars = await asyncio.to_thread(load_options)
    except Exception:
        logging.exception("Failed to load drop options")
        await interaction.followup.send("Failed to load drop options. Please try again.", ephemeral=True)
        return
    if item_obj is None or boss_obj is None or (open_item_id is not None and open_item_obj is None):
        await interaction.followup.send("Item or boss not found.", ephemeral=True)
        return
    if not avatars:
        await interaction.followup.send("No avatars registered. Use /create_avatar first.", ephemeral=True)
        return
    view = DropView(
        owner_id=interaction.user.id,
        drop_data={"item_id": item_id, "boss_id": boss_id,
                   "is_container": is_container, "open_item_id": open_item_id},
        item_name=item_obj.item,
        boss_name=f"{boss_obj.boss} ({boss_obj.difficulty})",
        avatars=avatars,
        drop_service=services.DropService(drop_repo),
        open_item_name=open_item_obj.item if open_item_obj else None,
    )
    view.message = await interaction.followup.send(
        view.render(), view=view, ephemeral=True, wait=True,
        allowed_mentions=discord.AllowedMentions.none(),
    )


#-----------------------------------------------------on_ready-----------------------------------------------------
@client.event
async def on_ready():
    tree.copy_global_to(guild=guild)
    synced = await tree.sync(guild=guild)
    print(f"{client.user} is logged in")
    print(f"synced {len(synced)} commands")




client.run(token)