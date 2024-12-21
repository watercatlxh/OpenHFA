import json
from lib.log import logger, RankType
from lib import config
import requests
from datetime import datetime
import csv
import os
import yaml


# 获取cookie(FreeCookieAPI)
def getCookie():
    logger(RankType.INFO, '尝试获取Cookie')
    url = 'https://cookie.alexblock.org/api/v1/freecookie/get/cookie'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        cookie = response.json()
    except json.decoder.JSONDecodeError as e:
        logger(RankType.ERROR, '获取Cookie失败: ' + str(e))
    try:
        if cookie['code'] == 0:
            logger(RankType.INFO, '获取Cookie成功')
            logger(RankType.INFO, 'Cookie:' + str(cookie))
    except KeyError:
        logger(RankType.ERROR, '获取Cookie失败: ' + str(cookie))
    return cookie


# 检测文件夹是否存在
def checkFolders():
    folders = [
        'accounts',
        'accounts/input',
        'accounts/output',
        'accounts/checked',
        'logs',
    ]
    current_dir = os.getcwd()
    for folder in folders:
        folder_path = os.path.join(current_dir, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            pass
        else:
            os.makedirs(folder_path)
            logger(RankType.SUCCESS, '已自动创建文件夹' + folder)
    logger(RankType.INFO, '文件夹已检查完毕')


def countFileLines(folder_path):
    total_files = 0
    total_lines = 0
    current_dir = os.getcwd()
    full_folder_path = os.path.join(current_dir, folder_path)

    # 遍历文件夹中的所有文件
    for root, _, files in os.walk(full_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 计算文件的行数
                    lines = f.readlines()
                    line_count = len(lines)
                    logger(RankType.INFO, f'检查文件: {file_path}')
                    logger(RankType.INFO, f'行数: {line_count}')

                    # 累计文件数和总行数
                    total_files += 1
                    total_lines += line_count
            except Exception as e:
                logger(RankType.ERROR, f"无法读取: {file_path},错误: {e}")


def writeOutfile(output_path, text):
    # 检查文件是否存在
    if not os.path.exists(output_path):
        # 如果文件不存在，创建文件
        with open(output_path, 'w'):
            pass  # 创建空文件

    # 打开文件并将text写到最后一行
    with open(output_path, 'a', encoding="utf-8") as file:
        file.write(text + '\n')  # 写入文本并添加换行符


def writeOutCache(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_current_time():
    # 获取当前时间
    now = datetime.now()
    # 格式化时间为 y-m-d-h-m-s
    formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    return formatted_time


def get_current_date():
    # 获取当前时间
    now = datetime.now()
    # 格式化时间为 y-m-d
    formatted_time = now.strftime("%Y-%m-%d")
    return formatted_time


def loadConfigs():
    # 定义默认配置
    default_configs = {
        'yunCookie': False,
        'useProxy': False,
        'changeProxyTime': 70,
        'yDailiAPIUrl': '',
        'multiThread': False,
        'multiThreadNum': 10,
        'managerType': 'official',
        'MCSM_API_URL': '',
        'MCSM_API_KEY': '',
        'instance_id': '',
        'daemon_id': '',
    }

    # 检查文件是否存在，如果不存在则创建默认配置文件
    if not os.path.exists('config.yaml'):
        with open('config.yaml', 'w') as file:
            yaml.dump(default_configs, file)
        logger(RankType.INFO, '已创建配置文件 请修改后运行')
        exit(0)

    # 读取 YAML 文件
    try:
        with open('config.yaml', 'r') as file:
            configs = yaml.safe_load(file)
    except Exception as e:
        logger(RankType.ERROR, f'无法读取配置文件: {e}')
        exit(1)

    # 动态设置配置项到 config 对象
    for key, value in configs.items():
        setattr(config, key, value)

    return config


def checkpoint_plus():
    with open('checkpoint_recheck.txt', 'a') as f:
        count = f.readlines()
    f.close()
    try:
        count = int(count[0]) + 1
        with open('checkpoint_recheck.txt', 'w') as f:
            f.write(str(count))
    finally:
        return
