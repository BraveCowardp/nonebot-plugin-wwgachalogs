from nonebot.plugin import PluginMetadata
from nonebot import require, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.log import logger

require("nonebot_plugin_orm")

from nonebot_plugin_orm import async_scoped_session
from .config import Config
from .db import GachaDatabase
from .model import CardPoolTypes, UserInfo
from .gacha import GachaLogs


__plugin_meta__ = PluginMetadata(
    name="鸣潮抽卡记录分析",
    description="鸣潮抽卡记录分析",
    usage="{插件用法}",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/BraveCowardp/nonebot-plugin-wwgachalogs",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

wwgacha_bind_info = on_command("鸣潮抽卡信息绑定")
wwgacha_get_gachalogs = on_command("抽卡记录", aliases={"抽卡记录查询"})
wwgacha_help = on_command("抽卡记录帮助")

@wwgacha_bind_info.handle()
async def handle_wwgacha_bind_info(event: GroupMessageEvent, state: T_State, session: async_scoped_session, args: Message = CommandArg()):
    info_list = args.extract_plain_text().split()
    if len(info_list) != 2:
        await wwgacha_bind_info.finish("参数个数有误，应为playerid和recordid")

    playerid = ""
    recordid = ""
    for info in info_list:
        if len(info) == 9:
            playerid = info
        if len(info) == 32:
            recordid = info
    
    if playerid == "" or recordid == "":
        await wwgacha_bind_info.finish("playerid应为9位，recordid应为32位，请检查")

    uncheck_user = UserInfo(userid=event.user_id, playerid=playerid, recordid=recordid)
    # 检查用户信息是否有效
    gachalogs = GachaLogs(user=uncheck_user)
    if not await gachalogs.check_user_info():
        await wwgacha_bind_info.finish("用户信息检查不通过，无法查询到抽卡信息")
    new_user = uncheck_user

    gachadatabase = GachaDatabase(session=session)
    user = await gachadatabase.get_user_info(userid=new_user.userid)

    if user == None:
        state["if_new_user"] = True

    if user == None or new_user.eq(user):
        state["if_cover"] = "是"

    state["wwgacha_user"] = new_user


@wwgacha_bind_info.got("if_cover", prompt="已设置过抽卡信息，输入\"是\"覆盖已有信息，输入其他内容取消")
async def _(state: T_State, session: async_scoped_session):
    user = state.get("wwgacha_user")
    if not isinstance(user, UserInfo):
        await wwgacha_bind_info.finish(f"user类型错误:{type(user)}")

    gachadatabase = GachaDatabase(session=session)
    if str(state.get("if_cover", "否")).strip() == "是":
        if state.get("if_new_user", False):
            await gachadatabase.insert_user_info(external_user=user)
        else:
            await gachadatabase.update_user_info(external_user=user)
        await gachadatabase.commit()
        await wwgacha_bind_info.finish(f"抽卡信息绑定成功，使用命令\"抽卡记录\"查看抽卡记录")
    else:
        await wwgacha_bind_info.finish(f"取消覆盖")



@wwgacha_get_gachalogs.handle()
async def handle_wwgacha_get_gachalogs(event: GroupMessageEvent, session: async_scoped_session):
    userid = event.user_id

    gachadatabase = GachaDatabase(session=session)
    user = await gachadatabase.get_user_info(userid=userid)
    if user == None:
        await wwgacha_get_gachalogs.finish("尚未绑定抽卡信息，请使用\"鸣潮抽卡信息绑定\"命令绑定")

    gachalogs = GachaLogs(user=user)
    gacha_log_dict = await gachalogs.get_gacha_info()
    if gacha_log_dict == None:
        await wwgacha_get_gachalogs.finish("抽卡记录获取有误，请重试")

    msg = ""
    for gacha_type in CardPoolTypes:
        gold_info_list = gacha_log_dict[gacha_type.name].get_gold_info_list()
        logger.debug(gold_info_list)
        info = f"{gacha_type.name}:"
        for gold_info in gold_info_list:
            name = gold_info['name']
            gacha_num = gold_info['gacha_num']
            info += f"{name}:[{gacha_num}] "

        msg += info + "\n"


    await wwgacha_get_gachalogs.finish(msg)


@wwgacha_help.handle()
async def handle_wwgacha_help():
    await wwgacha_help.finish("""PC端方法
        1.进入游戏，打开唤取界面，点击唤取记录
        2.右键鸣潮图标，选择打开文件所在位置
        3.依次打开目录 Wuthering Waves Game\\Client\\Saved Logs 找到 Client.log 文件
        4.使用文本编辑器打开，ctrl + F搜索 https://aki-gm-resources.aki-game.com/aki/gacha/index.html 找到位置
        5.找到链接携带的player_id和record_id参数
        6.发送 "鸣潮抽卡信息绑定 player_id record_id" 即可绑定抽卡信息，可长期使用
        例如：鸣潮抽卡信息绑定 100123456 b3545192e2d8ac6a6b0d069e6f54e83f
""")
