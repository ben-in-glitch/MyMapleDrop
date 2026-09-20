import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.environ.get("host"),
    user=os.environ.get("user"),
    password=os.environ.get("password"),
    port=os.environ.get("port"),
    database=os.environ.get("database")
)

token = os.environ.get("DISCORD_TOKEN")

guild_id = os.environ.get("guild_id")