import random
import threading
import time
from time import sleep

import javascript

from lib import globals
from colorama import init, deinit, Fore, Back, Style
from javascript import require, On  # type: ignore

from lib.file import checkpoint_plus
from lib.log import logger, log_to_file, RankType
from lib.manager.mcsm import restartInstanceMCSM

# 引入mineflayer
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')


# 用于解析布吉岛脑残言论的班级
class ChatMessage:
    def __init__(self, json_data, warn, text, extra, bold, italic, underlined, strikethrough, obfuscated, color):
        self.json = json_data
        self.warn = warn
        self.text = text
        self.extra = extra
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated
        self.color = color


# 用于解析布吉岛脑残言论的函数
def extract_text(chat_message):
    texts = []

    # 提取当前节点的文本
    if chat_message.text:
        texts.append(chat_message.text)

    # 递归提取子节点的文本
    if chat_message.extra:
        for sub_message in chat_message.extra:
            texts.extend(extract_text(sub_message))

    return texts


# 颜色代码映射
color_map = {
    '§0': Fore.BLACK,
    '§1': Fore.BLUE,
    '§2': Fore.GREEN,
    '§3': Fore.CYAN,
    '§4': Fore.RED,
    '§5': Fore.MAGENTA,
    '§6': Fore.YELLOW,
    '§7': Fore.WHITE,
    '§8': Fore.LIGHTBLACK_EX,
    '§9': Fore.LIGHTBLUE_EX,
    '§a': Fore.LIGHTGREEN_EX,
    '§b': Fore.LIGHTCYAN_EX,
    '§c': Fore.LIGHTRED_EX,
    '§d': Fore.LIGHTMAGENTA_EX,
    '§e': Fore.LIGHTYELLOW_EX,
    '§f': Fore.LIGHTWHITE_EX,
    '§r': Style.RESET_ALL,
    '§l': Style.DIM,
}


# 合并文本并转换颜色代码
def merge_and_colorize(texts, removeColor=False):
    if not removeColor:
        merged_text = ''.join(texts)
        for code, color in color_map.items():
            merged_text = merged_text.replace(code, color)
        return merged_text + Style.RESET_ALL  # 添加重置颜色代码
    else:
        merged_text = ''.join(texts)
        for code, color in color_map.items():
            merged_text = merged_text.replace(code, '')
        return merged_text


# 在每句前面加上灰色的 '[MESSAGE]'
def add_server_chat_prefix(texts):
    server_chat_prefix = f"{Fore.LIGHTBLACK_EX}[MESSAGE]{Style.RESET_ALL} "
    merged_text = merge_and_colorize(texts)
    return server_chat_prefix + merged_text


# 使用Mineflayer签到
def autoDaily(ip, port):
    try:
        # 是否生成
        botSpawned = False
        # 是否发送指令
        commandSent = False
        # 是否发送签到点击事件
        clickEventSent = False
        # 是否监听到成功事件
        successEvent = False
        # 是否退出服务器（主动）
        botDisconnect = False
        # 是否被踢
        botKicked = False
        # 签到奖励
        DailyRewards = ''

        logger(RankType.INFO, '正在尝试连接服务器')

        bot = mineflayer.createBot({
            "host": ip,
            "port": port,
            "username": "BMW",
            "version": "1.18.1",
            # try to fix bug
            "brand": "fml,forge",
            "checkTimeoutInterval": 30000,
            "noPongTimeout": 5000,
            "closeTimeout": 3000,
            # less network using
            "viewDistance": "tiny"
        })

        # 加入世界
        @On(bot, "spawn")
        def BotSpawn(this, *args):
            nonlocal botSpawned
            botSpawned = True
            logger(RankType.SUCCESS, '成功加入世界')
            countdown_thread = threading.Thread(target=countdown_and_execute)
            countdown_thread.start()

        # 定时签到
        def countdown_and_execute():
            nonlocal botSpawned
            nonlocal commandSent
            nonlocal botDisconnect
            time.sleep(2.5)
            if botSpawned:
                # 恶俗啊
                # logger('WARNING', '发送辱骂消息')
                # bot.chat("朱仲登#510525200202087898")
                commandSent = True
                logger(RankType.INFO, '尝试发送签到指令')
                bot.chat("/qd")

        # 弃用
        # 定时断连
        def countdown_and_exit():
            nonlocal botDisconnect
            time.sleep(0.5)
            bot.quit()
            botDisconnect = True

        # 自动修改变量
        def botQuit():
            nonlocal botDisconnect
            nonlocal botSpawned
            bot.quit()
            botSpawned = False
            botDisconnect = True

        # 箱子小偷 但是自动签到
        @On(bot, "windowOpen")
        def handle_window_open(this, window, *args):
            nonlocal clickEventSent
            nonlocal successEvent
            nonlocal DailyRewards
            logger(RankType.INFO, f'签到窗口已打开: {window.title}')
            if window.type == "minecraft:generic_9x3":
                if window.title == r'{"text":"每日签到   /已签到"}':
                    DailyRewards = ''
                    successEvent = True
                    countdown_thread_exit = threading.Thread(target=countdown_and_exit)
                    countdown_thread_exit.start()
                    logger(RankType.INFO, '签到成功')
                else:
                    slots = list(range(1, 16))
                    random.shuffle(slots)
                    for slot in slots:
                        item = window.slots[slot]
                        if item:
                            bot.clickWindow(slot, 0, 0)
                            clickEventSent = True
                            countdown_thread_daily_check = threading.Thread(target=countdown_and_execute)
                            countdown_thread_daily_check.start()
                            logger(RankType.INFO, '已点击签到 等待进行校验')
                            break
            else:
                logger(RankType.WARNING, f'未知的箱子类型: {window.type}')

        # 监测断连
        @On(bot, "end")
        def handle_end(this, *args):
            nonlocal botDisconnect
            nonlocal botSpawned
            nonlocal botKicked
            if botDisconnect == True:
                logger(RankType.SUCCESS, '成功退出服务器')
                botSpawned = False
            else:
                logger(RankType.ERROR, '异常退出服务器')
                botKicked = True

        # 监听被踢
        @On(bot, "kicked")
        def handle_kick(this, reason, *args):
            nonlocal botDisconnect
            nonlocal botKicked
            botDisconnect = False
            botKicked = True
            logger(RankType.ERROR, f'异常断开连接: {reason}')

        # 我觉得我是天才
        @On(bot, "message")
        def handle_message(this, message, *args):
            nonlocal successEvent
            nonlocal DailyRewards
            if extract_text(message) == ['    ', '签到成功,获得经验+', '188', '.']:
                DailyRewards = 'EXP188'
                logger(RankType.INFO, f'已识别到签到奖励: 经验+188')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '点券+', '100', '.']:
                DailyRewards = 'COIN100'
                logger(RankType.INFO, f'已识别到签到奖励: 点卷+100')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '脚底足迹+', '3天', '.']:
                DailyRewards = ''
                logger(RankType.INFO, f'已识别到签到奖励: 脚底足迹3d')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '起床硬币+', '200', '.']:
                DailyRewards = ''
                logger(RankType.INFO, f'已识别到签到奖励: 起床硬币+300')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '只因宠物时装[3天]', '.']:
                DailyRewards = ''
                logger(RankType.INFO, f'已识别到签到奖励: 时装3d')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '深紫·末影龙翅膀[3天]', '.']:
                DailyRewards = ''
                logger(RankType.INFO, f'已识别到签到奖励: 时装3d')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            elif extract_text(message) == ['    ', '签到成功,获得', '全服喇叭+', '2', '.']:
                DailyRewards = ''
                logger(RankType.INFO, f'已识别到签到奖励: 喇叭+2')
                botQuit()
                logger(RankType.INFO, '签到成功')
                successEvent = True
            log_to_file(extract_text(message))
            log_to_file('[MESSAGE] ' + merge_and_colorize(extract_text(message), removeColor=True))
            print(add_server_chat_prefix(merge_and_colorize(extract_text(message))))

        @On(bot,"error")
        def handle_error(this,error,*args):
            logger(RankType.ERROR,error)

        dailyTime = 0
        while True:
            if botKicked == True and successEvent == False:
                return False
            if dailyTime >= 60:
                botQuit()
                return False
            if successEvent:
                return DailyRewards
            sleep(0.1)
            dailyTime += 0.1
    except Exception as e:
        logger(RankType.ERROR, f'Mineflayer已被害死 准备重试:{e}')
        try:
            # javascript.terminate()
            # javascript.init()
            # logger(RankType.WARNING, '尝试重启Nodejs进程 此部分可能有部分账号失败 但是不用担心')
            logger(RankType.WARNING, '急眼了 正在尝试重启mineflayer')
            restartInstanceMCSM()
            checkpoint_plus()
            return False
        except Exception as e:
            logger(RankType.ERROR, f'重启失败: {e}')
            logger(RankType.WARNING, '我他妈紫砂')
            exit()

