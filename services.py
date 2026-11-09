class UserAlreadyExistedError(Exception): pass
class UserNameALreadyExistedError(Exception): pass
class UserNotRegisteredError(Exception): pass
class AvatorAlreadyExistsError(Exception): pass
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

class AvatorService:
    def __init__(self, avator_repo):
        self.avator_repo = avator_repo

    def create(self, user_dc_id, avator, job, cur_channel):
        user = self.is_existing_user(user_dc_id)
        if not user:
            raise UserNotRegisteredError()

        if self.is_existing_avator(avator):
            raise AvatorAlreadyExistsError()
        
        avator = model.Avators(user_id=user.id,
                                avator=avator.strip(),
                                  job=job.strip(),
                                    cur_channel=cur_channel.strip())
        self.avator_repo.create_avator(avator)
        return avator

    def update(self, user_dc_id, new_avator, new_job, new_channel):
        user = self.is_existing_user(user_dc_id)
        if not user:
            raise UserNotRegisteredError()

        new_avator = new_avator.strip() if new_avator else None
        avator = self.avator_repo.get_avator_by_name(new_avator)
        if avator:
            raise AvatorAlreadyExistsError()
        
        avator = model.Avators(user_id=user.id)
        avator.avator = new_avator if new_avator else avator.avator
        avator.job = new_job.strip() if new_job else avator.job
        avator.cur_channel = new_channel.strip() if new_channel else avator.cur_channel

        self.avator_repo.update_avator(avator)
        return avator

    def is_existing_avator(self, avator):
        return self.avator_repo.get_avator_by_name(avator)

    def is_existing_user(self,user_dc_id):
        return self.avator_repo.get_user_by_dc_id(user_dc_id)


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

if __name__ == "__main__":
    from config import db_pool
    from repositories import AvatorRepository
    avator_service = AvatorService(AvatorRepository(db_pool))