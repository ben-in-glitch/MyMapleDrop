import os
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host=os.environ.get("host"),
    user=os.environ.get("user"),
    password=os.environ.get("password"),
    port=os.environ.get("port"),
    database=os.environ.get("database")
)

token = os.environ.get("DISCORD_TOKEN")

guild_id = os.environ.get("guild_id")