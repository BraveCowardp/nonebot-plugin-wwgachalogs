from enum import Enum
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from nonebot_plugin_orm import Model


class UserInfo(Model):
    userid: Mapped[int] = mapped_column(primary_key=True)
    playerid: Mapped[str]
    recordid: Mapped[str]

    def eq(self, other) -> bool:
        if not isinstance(other, UserInfo):
            return False
        return (self.userid == other.userid and self.playerid == other.playerid and self.recordid == other.recordid)

class CardPoolTypes(Enum):
    角色UP池 = 1
    武器UP池 = 2
    角色普池 = 3
    武器普池 = 4

class OneGachaLog:
    def __init__(self, name: str, qualityLevel: int) -> None:
        self.name = name
        self.qualityLevel = qualityLevel

class GachaLogList(list):
    def __init__(self, data: List) -> None:
        self.gachalist: List[OneGachaLog] = []
        data.reverse()
        for raw_info in data:
            self.gachalist.append(OneGachaLog(name=raw_info['name'], qualityLevel=raw_info['qualityLevel']))

    def get_gold_info_list(self) -> List[dict[str, str]]:
        gold_info_list = []
        i = 0
        for row in self.gachalist:
            i = i+1
            if row.qualityLevel == 5:
                gold_info_list.append({"name":row.name,  "gacha_num":i})
                i = 0

        gold_info_list.append({"name": "上次出金后已抽", "gacha_num":i})
        return gold_info_list
