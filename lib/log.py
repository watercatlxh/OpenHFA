import colorama
from datetime import datetime
import os
from lib import globals
from enum import Enum

# 初始化
colorama.init()


# 日志输出
def logger_(rank, reason):
    colors = {
        'INFO': '\033[94m',  # 蓝色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',  # 红色
        'UNKNOWN': '\033[90m',  # 灰色
        'SUCCESS': '\033[92m',  # 绿色
    }
    reset = '\033[0m'
    color = colors.get(rank, colors['UNKNOWN'])
    log_message = f'[{rank}] {reason}'
    log_to_file(log_message)
    print(f'{color}[{rank}] {reason}{reset}')


def log_to_file(message):
    # 创建 logs 文件夹（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 写入日志文件
    with open(globals.log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f'{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} {message}\n')


# 定义 RankType 枚举类型
class RankType(Enum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    UNKNOWN = 'UNKNOWN'
    SUCCESS = 'SUCCESS'


# 获取格式化时间的函数
def get_time():
    now = datetime.now()
    return now.strftime("[%y-%m-%y %H:%M:%S]")


# 日志记录函数
def logger(rank: RankType, reason: str):
    colors = {
        RankType.INFO: '\033[94m',  # 蓝色
        RankType.WARNING: '\033[93m',  # 黄色
        RankType.ERROR: '\033[91m',  # 红色
        RankType.UNKNOWN: '\033[90m',  # 灰色
        RankType.SUCCESS: '\033[92m',  # 绿色
    }
    reset = '\033[0m'
    color = colors.get(rank, colors[RankType.UNKNOWN])
    log_message = f'[{rank.value}] {reason}'
    log_to_file(log_message)
    # print(f'{color}[{rank.value}]{get_time()} {reason}{reset}')
    print(f'{color}[{rank.value}] {reason}{reset}')
