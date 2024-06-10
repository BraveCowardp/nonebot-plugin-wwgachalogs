from enum import Enum
from typing import List

class User:
    def __init__(self, uid: int, playerid: str, recordid: str) -> None:
        self.uid: int = uid
        self.playerid: str = playerid
        self.recordid: str = recordid

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, User):
            return False
        if self.uid == value.uid and self.playerid == value.playerid and self.recordid == value.recordid:
            return True
        else:
            return False
        
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
