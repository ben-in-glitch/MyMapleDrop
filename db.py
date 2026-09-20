import config, model

db = config.db

# ----------------------user----------------------
def create_user(user):
    cursor = db.cursor()
    sql = "INSERT INTO users (dc_id, username) VALUES (%s, %s)"
    cursor.execute(sql, (user.dc_id, user.username))
    db.commit()
    cursor.close()

    return cursor.lastrowid

def update_user(user):
    cursor = db.cursor()
    sql = "UPDATE users SET username = %s WHERE dc_id = %s"
    cursor.execute(sql, (user.username, user.dc_id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

def get_user_by_dc_id(dc_id):
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE dc_id = %s"
    cursor.execute(sql, (dc_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return model.Users(id=result[0], dc_id=result[1], username=result[2])
    else:
        return None

# ----------------------avator----------------------
def create_avator(avator):
    cursor = db.cursor()
    sql = "INSERT INTO avators (user_id, avator, job, cur_channel) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (avator.user_id, avator.avator, avator.job, avator.cur_channel))
    db.commit()
    cursor.close()

    return cursor.lastrowid

def update_avator(avator):
    cursor = db.cursor()
    sql = "UPDATE avators SET avator = %s, job = %s, cur_channel = %s WHERE user_id = %s"
    cursor.execute(sql, (avator.avator, avator.job, avator.cur_channel, avator.user_id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

# ----------------------item----------------------
def create_item(item):
    cursor = db.cursor()
    sql = "INSERT INTO items (item) VALUES (%s)"
    cursor.execute(sql, (item.item,))
    db.commit()
    cursor.close()

    return cursor.lastrowid

def update_item(item):
    cursor = db.cursor()
    sql = "UPDATE items SET item = %s WHERE id = %s"
    cursor.execute(sql, (item.item, item.id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

# ----------------------boss----------------------
def create_boss(boss):
    cursor = db.cursor()
    sql = "INSERT INTO bosses (boss, difficulty) VALUES (%s, %s)"
    cursor.execute(sql, (boss.boss, boss.difficulty))
    db.commit()
    cursor.close()

    return cursor.lastrowid

def update_boss(boss):
    cursor = db.cursor()
    sql = "UPDATE bosses SET boss = %s, difficulty = %s WHERE id = %s"
    cursor.execute(sql, (boss.boss, boss.difficulty, boss.id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

# ----------------------drop----------------------
def create_drop(drop):
    cursor = db.cursor()
    sql = "INSERT INTO drops (created_ate, boss_id, item_id, is_container, open_tiem_id, quantity) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (drop.created_ate, drop.boss_id, drop.item_id, drop.is_container, drop.open_tiem_id, drop.quantity))
    db.commit()
    cursor.close()

    return cursor.lastrowid

def update_drop(drop):
    cursor = db.cursor()
    sql = "UPDATE drops SET created_ate = %s, boss_id = %s, item_id = %s, is_container = %s, open_tiem_id = %s, quantity = %s WHERE id = %s"
    cursor.execute(sql, (drop.created_ate, drop.boss_id, drop.item_id, drop.is_container, drop.open_tiem_id, drop.quantity, drop.id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

def delete_drop(drop_id):
    cursor = db.cursor()
    sql = "DELETE FROM drops WHERE id = %s"
    cursor.execute(sql, (drop_id,))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

# ----------------------drop_participant---------------------
def create_drop_participant(drop_participant):
    cursor = db.cursor()
    sql = "INSERT INTO drop_participants (avator_id, drop_id) VALUES (%s, %s)"
    cursor.execute(sql, (drop_participant.avator_id, drop_participant.drop_id))
    db.commit()
    cursor.close()
    
    return cursor.lastrowid

def update_drop_participant(drop_participant):
    cursor = db.cursor()
    sql = "UPDATE drop_participants SET avator_id = %s, drop_id = %s WHERE id = %s"
    cursor.execute(sql, (drop_participant.avator_id, drop_participant.drop_id, drop_participant.id))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0

def delete_drop_participant(drop_participant_id):
    cursor = db.cursor()
    sql = "DELETE FROM drop_participants WHERE id = %s"
    cursor.execute(sql, (drop_participant_id,))
    db.commit()
    cursor.close()

    return cursor.rowcount > 0