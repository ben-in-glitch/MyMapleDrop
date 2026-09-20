from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class Users:
    id: int = None
    dc_id: int = None
    username: str = None

@dataclass
class Avators:
    id: int = None
    user_id: int = None
    avator: str = None
    job: str = None
    cur_channel: str = None

@dataclass
class Items:
    id: int = None
    item: str = None

@dataclass
class Bosses:
    id: int = None
    boss: str = None
    difficulty: Literal["easy", "normal", "hard", "extreme"] = None

@dataclass
class Drops:
    id: int = None
    boss_id: int = None
    item_id: int = None
    is_container: bool = False
    open_item_id: int = None
    quantity: int = 1
    created_at: datetime = datetime.now().strftime("%Y-%m-%d")

@dataclass
class Drop_participants:
    id: int = None
    avator_id: int = None
    drop_id: int = None