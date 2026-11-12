import model
from contextlib import contextmanager

@contextmanager   
def db_connection(db_pool):
    conn = db_pool.get_connection()
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()

class UserRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_user(self,user:model.Users):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO users (dc_id, username) VALUES (%s, %s)"
            cursor.execute(sql, (user.dc_id, user.username))
            new_id = cursor.lastrowid
            cursor.close()

        return new_id

    def update_user(self,user:model.Users):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE users SET username = %s WHERE dc_id = %s"
            cursor.execute(sql, (user.username, user.dc_id))
            res = cursor.rowcount > 0
            cursor.close()

        return res

    def get_user_by_dc_id(self, dc_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE dc_id = %s"
            cursor.execute(sql, (dc_id,))
            result = cursor.fetchone()
            cursor.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None


    def get_user_by_username(self, username):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            cursor.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None


class AvatarRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool


    def create_avatar(self,avatar:model.Avatars):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO avatars (user_id, avatar, job, cur_channel) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (avatar.user_id, avatar.avatar, avatar.job, avatar.cur_channel))
            new_id = cursor.lastrowid
            cursor.close()

        return new_id

    def update_avatar(self,avatar:model.Avatars):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE avatars SET avatar = %s, job = %s, cur_channel = %s WHERE user_id = %s"
            cursor.execute(sql, (avatar.avatar, avatar.job, avatar.cur_channel, avatar.user_id))
            conn.commit()
            cursor.close()

        return cursor.rowcount > 0

    def get_avatar_by_name(self, avatar):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT id, user_id, avatar, job, cur_channel FROM avatars WHERE avatar = %s"
            cursor.execute(sql, (avatar,))
            result = cursor.fetchone()
            cursor.close()

        return model.Avatars(id=result[0], user_id=result[1], avatar=result[2], job=result[3], cur_channel=result[4]) if result else None

    def get_user_by_dc_id(self, user_dc_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE dc_id = %s"
            cursor.execute(sql, (user_dc_id,))
            result = cursor.fetchone()
            cursor.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None

    def get_all_avatars(self):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT id, user_id, avatar, job, cur_channel FROM avatars"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

        return [model.Avatars(id=result[0], user_id=result[1], avatar=result[2], job=result[3], cur_channel=result[4]) for result in results]

class ItemRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_item(self,item:model.Items):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO items (item) VALUES (%s)"
            cursor.execute(sql, (item.item,))
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        return new_id

    def update_item(self,item:model.Items):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE items SET item = %s WHERE id = %s"
            cursor.execute(sql, (item.item, item.id))
            res = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res

    def get_item_by_name(self, item_name):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM items WHERE item = %s"
            cursor.execute(sql, (item_name,))
            result = cursor.fetchone()
            cursor.close()

        return model.Items(id=result[0], item=result[1]) if result else None

    def get_item_by_id(self, item_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM items WHERE id = %s"
            cursor.execute(sql, (item_id,))
            result = cursor.fetchone()
            cursor.close()

        return model.Items(id=result[0], item=result[1]) if result else None

    def get_all_items(self):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM items"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

        return [model.Items(id=result[0], item=result[1]) for result in results]

class BossRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_boss(self,boss:model.Bosses):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO bosses (boss, difficulty) VALUES (%s, %s)"
            cursor.execute(sql, (boss.boss, boss.difficulty))
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        return new_id

    def update_boss(self,boss:model.Bosses):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE bosses SET boss = %s, difficulty = %s WHERE id = %s"
            cursor.execute(sql, (boss.boss, boss.difficulty, boss.id))
            res = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res

    def get_boss_by_name(self, boss_name):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM bosses WHERE boss = %s"
            cursor.execute(sql, (boss_name,))
            result = cursor.fetchone()
            cursor.close()

        return model.Bosses(id=result[0], boss=result[1], difficulty=result[2]) if result else None

    def get_boss_by_id(self, boss_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM bosses WHERE id = %s"
            cursor.execute(sql, (boss_id,))
            result = cursor.fetchone()
            cursor.close()

        return model.Bosses(id=result[0], boss=result[1], difficulty=result[2]) if result else None

    def get_all_bosses(self):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM bosses"
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

        return [model.Bosses(id=result[0], boss=result[1], difficulty=result[2]) for result in results]

class DropRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_with_participants(self, drop: model.Drops, avatar_ids):
        # One connection and one commit: both records succeed or both roll back.
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO drops (boss_id, item_id, is_container, open_item_id, quantity, created_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (drop.boss_id, drop.item_id, drop.is_container,
                     drop.open_item_id, drop.quantity, drop.created_at),
                )
                drop_id = cursor.lastrowid
                cursor.executemany(
                    "INSERT INTO drop_participants (avatar_id, drop_id) VALUES (%s, %s)",
                    [(avatar_id, drop_id) for avatar_id in avatar_ids],
                )
            finally:
                cursor.close()
        return drop_id

    def create_drop(self,drop:model.Drops):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO drops (boss_id, item_id, is_container, open_item_id, quantity, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (drop.boss_id, drop.item_id, drop.is_container, drop.open_item_id, drop.quantity, drop.created_at))
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        return new_id

    def update_drop(self,drop:model.Drops):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE drops SET boss_id = %s, item_id = %s, is_container = %s, open_item_id = %s, quantity = %s WHERE id = %s"
            cursor.execute(sql, (drop.boss_id, drop.item_id, drop.is_container, drop.open_item_id, drop.quantity, drop.id))
            res  = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res

    def delete_drop(self, drop_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM drops WHERE id = %s"
            cursor.execute(sql, (drop_id,))
            res = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res

class Drop_participantRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_drop_participant(self, drop_participant:model.Drop_participants):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO drop_participants (avatar_id, drop_id) VALUES (%s, %s)"
            cursor.execute(sql, (drop_participant.avatar_id, drop_participant.drop_id))
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()

        return new_id

    def update_drop_participant(self, drop_participant:model.Drop_participants):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "UPDATE drop_participants SET avatar_id = %s, drop_id = %s WHERE id = %s"
            cursor.execute(sql, (drop_participant.avatar_id, drop_participant.drop_id, drop_participant.id))
            res = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res


    def delete_drop_participant(self, drop_participant_id):
        with db_connection(self.db_pool) as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM drop_participants WHERE id = %s"
            cursor.execute(sql, (drop_participant_id,))
            res = cursor.rowcount > 0
            conn.commit()
            cursor.close()

        return res


if __name__ == "__main__":
    from config import db

