import httpx

from nonebot.log import logger
from .model import GachaLogList, CardPoolTypes, UserInfo

GACHALOGS_URL = 'https://gmserver-api.aki-game2.com/gacha/record/query'

def __prefill_request_data__(user: UserInfo):
    cache = {
        "serverId": "76402e5b20be2c39f095a152090afddc",
        playerId": user.playerid,
        "languageCode": "zh-Hans",
        "recordId": user.recordid,
        "cardPoolId": -1,
        "cardPoolType": -1
    }
    def request_data(cardPoolId: int, cardPoolType: int):
        cache["cardPoolId"] = cardPoolId
        cache["cardPoolType"] = cardPoolType
        return cache
    return request_data

def __gen_request_data__(user: UserInfo):
    unfinished = __prefill_request_data__(user)
    for pool_type in CardPoolTypes:
        finished = unfinished(pool_type.value, pool_type.value)
        yield finished

async def check(user):
    request_datas = __gen_request_data__(user)
    request_data = next(request_datas)
    return check_user_info(request_data)
        
async def do(user) -> dict[str, GachaLogList]|None:
    gacha_log_dict: dict[str, GachaLogList] = {}
    request_datas = __gen_request_data__(user)
        
    for request_data in request_datas:
        gacha_list = get_gacha_info(request_data)
        gacha_log_dict[pool_type.name] = gacha_list
     return gacha_log_dict



def __check_user_info__(request_data) -> bool:
    with httpx.AsyncClient() as client:
        request_data = self.generate_request_data(cardPoolId=1, cardPoolType=1)
        respose = client.post(url=GACHALOGS_URL, json=request_data, timeout=90)
        
    status = respose.json()['message']
    if status != 'success':
        return False
    return True
    
def __get_gacha_info__(request_data):
    with httpx.AsyncClient() as client:
        respose = client.post(url=GACHALOGS_URL, json=request_data, timeout=90)
            
    status = respose.json()['message']
    if status != 'success':
        return None
            
    data = respose.json()['data']
    return GachaLogList(data=data)
    

