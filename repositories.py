import model

class UserRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_user(self,user:model.Users):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO users (dc_id, username) VALUES (%s, %s)"
        cursor.execute(sql, (user.dc_id, user.username))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_user(self,user:model.Users):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE users SET username = %s WHERE dc_id = %s"
        cursor.execute(sql, (user.username, user.dc_id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

    def get_user_by_dc_id(self, dc_id):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE dc_id = %s"
        cursor.execute(sql, (dc_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None

    def get_user_by_username(self, username):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None

class AvatorRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_avator(self,avator:model.Avators):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO avators (user_id, avator, job, cur_channel) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (avator.user_id, avator.avator, avator.job, avator.cur_channel))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_avator(self,avator:model.Avators):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE avators SET avator = %s, job = %s, cur_channel = %s WHERE user_id = %s"
        cursor.execute(sql, (avator.avator, avator.job, avator.cur_channel, avator.user_id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

    def get_avator_by_name(self, avator):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM avators WHERE avator = %s"
        cursor.execute(sql, (avator,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        return model.Avators(id=result[0], user_id=result[1], avator=result[2], job=result[3], cur_channel=result[4]) if result else None

    def get_user_by_dc_id(self, user_dc_id):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE dc_id = %s"
        cursor.execute(sql, (user_dc_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        return model.Users(id=result[0], dc_id=result[1], username=result[2]) if result else None

class ItemRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_item(self,item:model.Items):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO items (item) VALUES (%s)"
        cursor.execute(sql, (item.item,))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_item(self,item:model.Items):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE items SET item = %s WHERE id = %s"
        cursor.execute(sql, (item.item, item.id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

class BossRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_boss(self,boss:model.Bosses):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO bosses (boss, difficulty) VALUES (%s, %s)"
        cursor.execute(sql, (boss.boss, boss.difficulty))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_boss(self,boss:model.Bosses):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE bosses SET boss = %s, difficulty = %s WHERE id = %s"
        cursor.execute(sql, (boss.boss, boss.difficulty, boss.id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

class DropRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_drop(self,drop:model.Drops):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO drops (boss_id, item_id, is_container, open_item_id, quantity, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (drop.boss_id, drop.item_id, drop.is_container, drop.open_item_id, drop.quantity, drop.created_at))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_drop(self,drop:model.Drops):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE drops SET boss_id = %s, item_id = %s, is_container = %s, open_item_id = %s, quantity = %s WHERE id = %s"
        cursor.execute(sql, (drop.boss_id, drop.item_id, drop.is_container, drop.open_item_id, drop.quantity, drop.id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

    def delete_drop(self, drop_id):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM drops WHERE id = %s"
        cursor.execute(sql, (drop_id,))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

class Drop_participantRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def create_drop_participant(self, drop_participant:model.Drop_participants):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO drop_participants (avator_id, drop_id) VALUES (%s, %s)"
        cursor.execute(sql, (drop_participant.avator_id, drop_participant.drop_id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.lastrowid

    def update_drop_participant(self, drop_participant:model.Drop_participants):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "UPDATE drop_participants SET avator_id = %s, drop_id = %s WHERE id = %s"
        cursor.execute(sql, (drop_participant.avator_id, drop_participant.drop_id, drop_participant.id))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0

    def delete_drop_participant(self, drop_participant_id):
        db = self.db_pool.get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM drop_participants WHERE id = %s"
        cursor.execute(sql, (drop_participant_id,))
        db.commit()
        cursor.close()
        db.close()

        return cursor.rowcount > 0


if __name__ == "__main__":
    from config import db

