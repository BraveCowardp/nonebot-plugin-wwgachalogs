import httpx

from nonebot.log import logger
from .model import GachaLogList, CardPoolTypes, UserInfo

GACHALOGS_URL = 'https://gmserver-api.aki-game2.com/gacha/record/query'

class GachaLogs:
    def __init__(self, user: UserInfo) -> None:
        self.user = user
        self.gacha_log_dict = {}

    def generate_request_data(self, cardPoolId: int, cardPoolType: int) -> dict:
        return {
                    "serverId": "76402e5b20be2c39f095a152090afddc",
                    "playerId": self.user.playerid,
                    "languageCode": "zh-Hans",
                    "recordId": self.user.recordid,
                    "cardPoolId": cardPoolId,
                    "cardPoolType": cardPoolType
                }

    async def check_user_info(self) -> bool:
        async with httpx.AsyncClient() as client:
            request_data = self.generate_request_data(cardPoolId=1, cardPoolType=1)
            respose = await client.post(url=GACHALOGS_URL, json=request_data, timeout=90)
        
        status = respose.json()['message']
        if status != 'success':
            return False
        return True
    
    async def get_gacha_info(self) -> dict[str, GachaLogList]|None:
        gacha_log_dict: dict[str, GachaLogList] = {}

        for pool_type in CardPoolTypes:
            async with httpx.AsyncClient() as client:
                request_data = self.generate_request_data(cardPoolId=pool_type.value, cardPoolType=pool_type.value)
                respose = await client.post(url=GACHALOGS_URL, json=request_data, timeout=90)
            
            status = respose.json()['message']
            if status != 'success':
                return None
            
            data = respose.json()['data']
            gacha_log_dict[pool_type.name] = GachaLogList(data=data)

        return gacha_log_dict