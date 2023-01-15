from dataclasses import dataclass
from uuid6 import uuid8

@dataclass
class UserInfo:
    user_id: int
    admin: bool


@dataclass
class OrderInfo:
    uid_order:str=str(uuid8())
    user_id:int = None
    region: str=None
    type_com:str=None
    section:str=None
    rate:str=None
    billing:str=None
    pay:bool=None
    active:bool=None
    tx_hash:str=None
    user_url:str=None