import aiosqlite
import asyncio
from os.path import abspath, dirname
from nonebot.log import logger
from .model import User

class GachaDatabase:
    def __init__(self) -> None:
        self.db_name = dirname(abspath(__file__)) + "/gacha.db"
        asyncio.run(self.init_database())

    async def init_database(self) -> None:
        self.conn = await aiosqlite.connect(self.db_name)
        cur = await self.conn.cursor()
        logger.debug(f'初始化数据库')

        # 创建url表
        await cur.execute('''
            CREATE TABLE IF NOT EXISTS user_info
            (
                uid INT PRIMARY KEY NOT NULL,
                playerid VARCHAR(9) NOT NULL,
                recordid VARCHAR(32) NOT NULL
            )
            ''')
        
    async def get_user_info(self, uid: int) -> User|None:
        cur = await self.conn.cursor()

        # 查询用户
        await cur.execute("SELECT uid, playerid, recordid FROM user_info WHERE uid = ?", (str(uid),))

        result = await cur.fetchone()
        if result == None:
            return None

        user = User(uid=int(result[0]), playerid=result[1], recordid=result[2])
        return user
    
    async def update_user_info(self, user: User) -> bool:
        cur = await self.conn.cursor()

        try:
            await cur.execute("UPDATE user_info SET playerid = ?, recordid = ? WHERE uid = ?", (user.playerid, user.recordid, user.uid))
        except Exception as e:
            ##logger.debug(f'更新信息表时发生错误:\n{e}')
            raise e
        else:
            ##logger.info(f'更新信息表成功')
            await self.conn.commit()
            return True

    async def insert_user_info(self, user: User) -> bool:
        cur = await self.conn.cursor()

        try:
            await cur.execute("INSERT INTO user_info(uid, playerid, recordid) VALUES (?, ?, ?)", (user.uid, user.playerid, user.recordid))
        except Exception as e:
            logger.error(f'[]插入信息表时发生错误:\n{e}')
            await self.conn.rollback()
            await cur.close()
            return False
        else:
            await cur.close()
            await self.conn.commit()
            #logger.info(f'插入信息表成功')
            return True
        