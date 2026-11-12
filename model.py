from dataclasses import dataclass, field
from typing import Literal
from datetime import date


@dataclass
class Users:
    id: int = None
    dc_id: int = None
    username: str = None

@dataclass
class Avatars:
    id: int = None
    user_id: int = None
    avatar: str = None
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
    created_at: date = field(default_factory=date.today)

@dataclass
class Drop_participants:
    id: int = None
    avatar_id: int = None
    drop_id: int = None