from dataclasses import dataclass


@dataclass
class UserInfo:
    user_id: int
    admin: bool


@dataclass
class OrderInfo:
    uid_order:str
    region: str
    type_com:str
    section:str
    rate:str
    billing:str
    pay:bool
    active:bool