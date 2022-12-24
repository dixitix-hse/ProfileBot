import sqlite3 as sql


async def db_connect():
    global db, cursor
    db = sql.connect('profiles_data.db')
    cursor = db.cursor()
    query = "CREATE TABLE IF NOT EXISTS profiles(user_id TEXT PRIMARY KEY, name TEXT, gender TEXT, age INTEGER)"
    cursor.execute(query)
    db.commit()


async def create_profile(state, user_id):
    user = cursor.execute(
        "SELECT user_id FROM profiles WHERE user_id == '{key}'".format(
            key=user_id)).fetchone()
    if not user:
        async with state.proxy() as data:
            cursor.execute(
                "INSERT INTO profiles (user_id, name, gender, age) VALUES(?,?,?,?)",
                (user_id, data['name'], data["gender"], data["age"]))
            db.commit()
    else:
        await update_profile(state, user_id)


async def update_profile(state, user_id):
    async with state.proxy() as data:
        update_query = "UPDATE profiles  SET name ='{}', gender ='{}', age ='{}' WHERE user_id=='{}'".format(
            data['name'], data["gender"], data["age"], user_id)
        cursor.execute(update_query)
        db.commit()


async def get_profile(user_id):
    user = cursor.execute(
        "SELECT * FROM profiles WHERE user_id == '{key}'".format(
            key=user_id)).fetchone()
    return user
