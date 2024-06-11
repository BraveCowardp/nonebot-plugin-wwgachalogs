from nonebot.log import logger
from .model import UserInfo
from nonebot_plugin_orm import async_scoped_session

class GachaDatabase:
    def __init__(self, session: async_scoped_session) -> None:
        self.session = session
        
    async def get_user_info(self, userid: int) -> UserInfo|None:
        # 查询用户
        if not (user := await self.session.get(UserInfo, userid)):
            return None
        return user
    
    async def update_user_info(self, external_user: UserInfo) -> bool:
        try:
            await self.session.merge(external_user)
        except Exception as e:
            ##logger.debug(f'更新信息表时发生错误:\n{e}')
            raise e
        else:
            ##logger.info(f'更新信息表成功')
            return True

    async def insert_user_info(self, external_user: UserInfo) -> bool:
        try:
            self.session.add(external_user)
        except Exception as e:
            logger.error(f'插入信息表时发生错误:\n{e}')
            await self.session.rollback()
            return False
        else:
            #logger.info(f'插入信息表成功')
            return True

    async def commit(self) -> None:
        await self.session.commit()
