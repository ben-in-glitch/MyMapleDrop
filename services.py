class UserAlreadyExistedError(Exception): pass
class UserNameALreadyExistedError(Exception): pass
class UserNotRegisteredError(Exception): pass
class AvatarAlreadyExistsError(Exception): pass
class BossAlreadyExistsError(Exception): pass
class BossNotFoundError(Exception): pass
class ItemAlreadyExistsError(Exception): pass
class ItemNotFoundError(Exception): pass
import model

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, dc_id, username):
        if self.user_repo.get_user_by_dc_id(dc_id):
            raise UserAlreadyExistedError()
        if self.is_existing_username(username.strip()):
            raise UserNameALreadyExistedError()
        
        user = model.Users(dc_id=dc_id, username=username)
        self.user_repo.create_user(user)
        return user

    def update_username(self, dc_id, new_username):
        user = self.user_repo.get_user_by_dc_id(dc_id)
        new_username = new_username.strip()
        if not user:
            raise UserNotRegisteredError()
        if self.is_existing_username(new_username):
            raise UserNameALreadyExistedError()
        
        user.username = new_username
        self.user_repo.update_user(user)
        return user

    def is_existing_username(self, username):
        return self.user_repo.get_user_by_username(username.strip()) is not None

class AvatarService:
    def __init__(self, avatar_repo):
        self.avatar_repo = avatar_repo

    def create(self, user_dc_id, avatar, job, cur_channel):
        user = self.is_existing_user(user_dc_id)
        if not user:
            raise UserNotRegisteredError()

        if self.is_existing_avatar(avatar):
            raise AvatarAlreadyExistsError()
        
        avatar = model.Avatars(user_id=user.id,
                                avatar=avatar.strip(),
                                  job=job.strip(),
                                    cur_channel=cur_channel.strip())
        self.avatar_repo.create_avatar(avatar)
        return avatar

    def update(self, user_dc_id, new_avatar, new_job, new_channel):
        user = self.is_existing_user(user_dc_id)
        if not user:
            raise UserNotRegisteredError()

        new_avatar = new_avatar.strip() if new_avatar else None
        avatar = self.avatar_repo.get_avatar_by_name(new_avatar)
        if avatar:
            raise AvatarAlreadyExistsError()
        
        avatar = model.Avatars(user_id=user.id)
        avatar.avatar = new_avatar if new_avatar else avatar.avatar
        avatar.job = new_job.strip() if new_job else avatar.job
        avatar.cur_channel = new_channel.strip() if new_channel else avatar.cur_channel

        self.avatar_repo.update_avatar(avatar)
        return avatar

    def is_existing_avatar(self, avatar):
        return self.avatar_repo.get_avatar_by_name(avatar)

    def is_existing_user(self,user_dc_id):
        return self.avatar_repo.get_user_by_dc_id(user_dc_id)


class BossService:
    def __init__(self, boss_repo):
        self.boss_repo = boss_repo

    def create(self, boss_name, difficulty):
        if self.is_existing_boss(boss_name):
            raise BossAlreadyExistsError()

        boss = model.Bosses(boss=boss_name.strip(), difficulty=difficulty.strip())
        self.boss_repo.create_boss(boss)
        return boss

    def update(self, boss_id, new_boss_name, new_difficulty):
        boss = self.is_existing_boss(boss_id=boss_id)
        if not boss:
            raise BossNotFoundError()

        if self.is_existing_boss(new_boss_name):
            raise BossAlreadyExistsError()

        boss.boss = new_boss_name.strip() if new_boss_name else boss.boss
        boss.difficulty = new_difficulty.strip() if new_difficulty else boss.difficulty

        self.boss_repo.update_boss(boss)
        return boss

    def is_existing_boss(self, boss_name = None, boss_id = None):
        if boss_name is not None:
            return self.boss_repo.get_boss_by_name(boss_name)
        elif boss_id is not None:
            return self.boss_repo.get_boss_by_id(boss_id)
        return False

class ItemService:
    def __init__(self, item_repo):
        self.item_repo = item_repo

    def create(self, item_name):
        if self.is_existing_item(item_name):
            raise ItemAlreadyExistsError()

        item = model.Items(item=item_name.strip())
        self.item_repo.create_item(item)
        return item

    def update(self, item_id, new_item_name):
        item = self.is_existing_item(item_id=item_id)
        if not item:
            raise ItemNotFoundError()

        if self.is_existing_item(new_item_name):
            raise ItemAlreadyExistsError()

        item.item = new_item_name.strip() if new_item_name else item.item

        self.item_repo.update_item(item)
        return item

    def is_existing_item(self, item_name = None, item_id = None):
        if item_name is not None:
            return self.item_repo.get_item_by_name(item_name)
        elif item_id is not None:
            return self.item_repo.get_item_by_id(item_id)
        return False

class DropService:
    def __init__(self, drop_repo):
        self.drop_repo = drop_repo

    def create_with_participants(self, drop_data, avatar_ids):
        avatar_ids = sorted(set(avatar_ids))
        if not avatar_ids:
            raise ValueError("At least one participant is required")
        drop = model.Drops(**drop_data)
        if drop.open_item_id is not None and not drop.is_container:
            raise ValueError("Only containers can have an opened item")
        return self.drop_repo.create_with_participants(drop, avatar_ids)

    def create(self, boss_id, item_id, is_container=False, open_item_id=None, quantity=1):
        drop = model.Drops(boss_id=boss_id,
                           item_id=item_id,
                           is_container=is_container,
                           open_item_id=open_item_id,
                           quantity=quantity)
        self.drop_repo.create_drop(drop)
        return drop

if __name__ == "__main__":
    from config import db_pool
    from repositories import AvatarRepository
    avatar_service = AvatarService(AvatarRepository(db_pool))