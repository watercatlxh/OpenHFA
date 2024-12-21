import shutil
from lib.myth.myth import *
from lib.file import *
from lib.mineflayer.mineflayer import *
from lib.freecookie import getNameFreeCookie
from lib.LocalRandomName import random_name
from lib.proxyprovider.ydaili import yDailiGet
import os
from datetime import datetime
import csv
import argparse
from lib.hitokotoAPI import get_hitokoto

# info
project_version = '241002'

def main():
    # arg start
    parser = argparse.ArgumentParser(description="What Can I Say")
    # 创建互斥组
    group = parser.add_mutually_exclusive_group()
    # 添加 --recheck 和 --newcheck 参数到互斥组
    group.add_argument('--recheck', action='store_true', help='签到老账号')
    group.add_argument('--newcheck', action='store_true', help='签到新账号')
    # check arg
    args = parser.parse_args()

    globals.start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    globals.log_file_path = os.path.join('logs', f'log_{globals.start_time}.txt')
    print('')
    print('''    ██╗  ██╗███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗
    ██║  ██║██╔════╝╚██╗ ██╔╝██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║
    ███████║█████╗   ╚████╔╝ ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║
    ██╔══██║██╔══╝    ╚██╔╝  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║
    ██║  ██║███████╗   ██║   ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║
    ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝''')
    logger(RankType.SUCCESS, 'HeypixelCheckIn made by CheatFox & AlexBlock')
    logger(RankType.SUCCESS, "version: " + project_version)
    logger(RankType.SUCCESS, f'❀ {get_hitokoto()}')
    logger(RankType.INFO, '正在初始化...')
    loadConfigs()
    checkFolders()
    logger(RankType.INFO, '云Cookie: ' + str(config.yunCookie))
    logger(RankType.INFO, '是否使用代理: ' + str(config.useProxy))
    logger(RankType.INFO, '代理切换时间: ' + str(config.changeProxyTime))
    logger(RankType.INFO, '易代理API: ' + config.yDailiAPIUrl)
    logger(RankType.WARNING, '请确保你已经打开Myth并且打开过Myth网页控制台登录')
    logger(RankType.INFO, '正在尝试连接Myth本地服务器...')
    pingStatus = pingMyth()
    if not pingStatus:
        exit(-1)
    if config.yunCookie:
        # 使用亚历山大方块的 获取曲奇
        pass
    else:
        if args.recheck:
            logger(RankType.INFO, '您正在使用--recheck参数启动')
            user_input = '2'
        elif args.newcheck:
            logger(RankType.INFO, '您正在使用--newcheck参数启动')
            user_input = '1'
        else:
            logger(RankType.WARNING, '请选择你想要进行的操作~')
            logger(RankType.INFO, '[1]签到新账号(input文件夹中的)')
            logger(RankType.INFO, '[2]签到老账号(cache.csv中的)')
            logger(RankType.INFO, '请输入你的选择并回车:')
            user_input = input()
        if user_input == "1":
            globals.successCount = 0
            globals.failedCount = 0

            # 获取当前路径
            current_dir = os.getcwd()
            start_time = time.time()

            # 获取文件夹路径
            input_folder_path = os.path.join(current_dir, 'accounts/input')
            checked_folder_path = os.path.join(current_dir, 'accounts/checked')
            checkpoint_file = 'checkpoint_newcheck.txt'

            # 确保 checked 文件夹存在
            if not os.path.exists(checked_folder_path):
                os.makedirs(checked_folder_path)

            # 读取断点续测的记录
            checkpoint = {}
            if os.path.exists(checkpoint_file):
                logger(RankType.WARNING, '检测到断点续测文件 即将继续上次的进度')
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)

            # 遍历文件
            for filename in os.listdir(input_folder_path):
                # 获取文件路径
                file_path = os.path.join(input_folder_path, filename)

                # 确保只读取文件，忽略文件夹
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        logger(RankType.INFO, f'正在读取文件: {filename}')

                        # 从断点续测记录中获取当前文件的行号
                        current_line = checkpoint.get(filename, 0)

                        # 跳过已经处理过的行
                        for _ in range(current_line):
                            next(file)

                        for line in file:
                            current_line += 1
                            logger(RankType.INFO, f'正在读取第{str(current_line)}行')

                            # 分割账号密码曲奇
                            line = line.strip()
                            parts = line.split('----')
                            username, password, cookie = parts
                            start_time = time.time()
                            shareMainCode(username, password, cookie)

                            # 记录当前处理的文件和行号
                            checkpoint[filename] = current_line
                            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                                json.dump(checkpoint, f)

                        # 处理完当前文件后，删除记录
                        del checkpoint[filename]
                        with open(checkpoint_file, 'w', encoding='utf-8') as f:
                            json.dump(checkpoint, f)

                        # 将文件移动到 checked 文件夹
                        shutil.move(file_path, os.path.join(checked_folder_path, filename))
                        logger(RankType.INFO, f'文件 {filename} 已移动到 checked 文件夹')

            # 计时
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger(RankType.SUCCESS, f'全部任务完成 耗时 {elapsed_time} s')
            logger(RankType.ERROR, f'Failed: {globals.failedCount}')
            logger(RankType.SUCCESS, f'Success: {globals.successCount}')

            # 删除断点续测记录文件
            if os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)

            exit(0)

        elif user_input == "2":
            globals.successCount = 0
            globals.failedCount = 0
            rows = []
            start_time = time.time()
            BREAKPOINT_FILE = 'checkpoint_recheck.txt'

            # 读取断点
            try:
                with open(BREAKPOINT_FILE, 'r') as file:
                    breakpoint = int(file.read().strip())
            except FileNotFoundError:
                breakpoint = 0

            with open('accounts/cache.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # 逐行读取数据
                for row in reader:
                    rows.append(row)

            lines = 0
            # 处理断点之前的行
            for row in rows[breakpoint:]:
                username, password, cookie, name, accountEntityID, characterEntityID, EXP, heypixelCoins, currentDate, *_ = row
                if currentDate == get_current_date():
                    lines += 1
                    logger(RankType.INFO, f'{username} 今天已经签过到了 跳过')
                else:
                    lines += 1
                    logger(RankType.INFO, f'正在读取第{str(lines + breakpoint)}行')
                    shareMainCode(username, password, cookie, name, characterEntityID, EXP, heypixelCoins)

                # 更新断点
                with open(BREAKPOINT_FILE, 'w') as file:
                    file.write(str(lines + breakpoint))

            # 如果已经处理完所有行，重置断点
            if lines + breakpoint >= len(rows):
                with open(BREAKPOINT_FILE, 'w') as file:
                    file.write('0')
                breakpoint = 0

            # 从第0行开始继续处理剩余的行
            for row in rows[breakpoint:]:
                username, password, cookie, name, accountEntityID, characterEntityID, EXP, heypixelCoins, currentDate, *_ = row
                if currentDate == get_current_date():
                    lines += 1
                    logger(RankType.INFO, f'{username} 今天已经签过到了 跳过')
                else:
                    lines += 1
                    logger(RankType.INFO, f'正在读取第{str(lines + breakpoint)}行')
                    shareMainCode(username, password, cookie, name, characterEntityID, EXP, heypixelCoins)

                # 更新断点
                with open(BREAKPOINT_FILE, 'w') as file:
                    file.write(str(lines + breakpoint))

            end_time = time.time()
            elapsed_time = end_time - start_time
            logger(RankType.SUCCESS, f'全部任务完成 耗时 {elapsed_time} s')
            logger(RankType.ERROR, f'Failed: {globals.failedCount}')
            logger(RankType.SUCCESS, f'Success: {globals.successCount}')
            exit(0)
        else:
            logger(RankType.ERROR, '请输入正确的选择!')
            exit(0)


# 把可共用的代码放在这里
def shareMainCode(username, password, cookie, name=None, characterEntityID=None, EXP=0, heypixelCoins=0):
    # 登录
    accountEntityID = loginCookie(cookie)
    if isinstance(accountEntityID, bool):
        if accountEntityID == False:
            logger(RankType.ERROR, f'登录失败 跳过操作')
            globals.failedCount += 1
            logoutMyth(accountEntityID, cookie)
            return

    # 检测角色是否上限
    CharacterNum = getCharacterNumMyth(accountEntityID)
    if isinstance(CharacterNum, bool):
        if CharacterNum == False:
            logger(RankType.ERROR, f'获取角色列表失败 跳过操作')
            globals.failedCount += 1
            logoutMyth(accountEntityID, cookie)
            return
    if CharacterNum == 3 and name is None:
        logger(RankType.ERROR, f'角色数量超出上限 跳过操作')
        globals.failedCount += 1
        logoutMyth(accountEntityID, cookie)
        return

    # 随机名
    if name is None:
        # 你好啊喜欢免费饼干的Alex菠萝客
        # name = getNameFreeCookie()
        name = random_name()
        if isinstance(name, bool):
            if name == False:
                logger(RankType.ERROR, f'获取随机名失败 跳过操作')
                globals.failedCount += 1
                logoutMyth(accountEntityID, cookie)
                return

    # 创建角色
    if characterEntityID is None:
        characterEntityID = createGameName(accountEntityID, name)
        if isinstance(characterEntityID, bool):
            if not characterEntityID:
                logger(RankType.ERROR, f'创建角色失败 跳过操作')
                globals.failedCount += 1
                logoutMyth(accountEntityID, cookie)
                return
        setRandomSkinMyth(accountEntityID)

    # 获取服务器列表
    # getServerListMyth(accountEntityID)

    # 获取服务器地址
    # getNetGameAddressMyth(accountEntityID)

    # 开启代理
    ip, port = startProxyMyth(characterEntityID, accountEntityID, name)
    if isinstance(ip, bool):
        if not ip:
            logger(RankType.ERROR, f'启动代理失败 跳过操作')
            globals.failedCount += 1
            logoutMyth(accountEntityID, cookie)
            return

    # 设置socks5
    def getSocks5Main():
        socks5ip, socks5port = yDailiGet()
        if isinstance(dailyStatus, bool):
            if not socks5ip:
                logger(RankType.ERROR, '获取代理失败 跳过操作')
                stopProxyMyth(characterEntityID, accountEntityID)
            else:
                globals.socks5ip, globals.socks5port = socks5ip, socks5port
                globals.proxyUsedTime = time.time()
        else:
            globals.socks5ip, globals.socks5port = socks5ip, socks5port
            globals.proxyUsedTime = time.time()

    if config.useProxy:
        if globals.proxyUsedTime == 0:
            logger(RankType.INFO, '未设置代理 正在尝试设置代理')
            socks5ip, socks5port = yDailiGet()
            if isinstance(socks5ip, bool):
                if not socks5ip:
                    logger(RankType.ERROR, '获取代理失败 跳过操作')
                    stopProxyMyth(characterEntityID, accountEntityID)
                    return
                else:
                    globals.socks5ip, globals.socks5port = socks5ip, socks5port
                    globals.proxyUsedTime = time.time()
            else:
                globals.socks5ip, globals.socks5port = socks5ip, socks5port
                globals.proxyUsedTime = time.time()
        elif time.time() - globals.proxyUsedTime >= config.changeProxyTime:
            logger(RankType.WARNING, '代理已过期 正在尝试更换代理')
            socks5ip, socks5port = yDailiGet()
            if isinstance(socks5ip, bool):
                if not socks5ip:
                    logger(RankType.ERROR, '获取代理失败 跳过操作')
                    stopProxyMyth(characterEntityID, accountEntityID)
                    return
                else:
                    globals.socks5ip, globals.socks5port = socks5ip, socks5port
                    globals.proxyUsedTime = time.time()
            else:
                globals.socks5ip, globals.socks5port = socks5ip, socks5port
                globals.proxyUsedTime = time.time()
        setSocks5ProxyMyth(globals.socks5ip, globals.socks5port, characterEntityID)

    logger(RankType.INFO, f'正在尝试签到: {accountEntityID}')
    logger(RankType.INFO, f'{name} 现有数据EXP:{EXP} COIN:{heypixelCoins}')
    # 签到
    dailyStatus = autoDaily(ip, port)
    if isinstance(dailyStatus, bool):
        if not dailyStatus:
            for i in range(3):
                stopProxyMyth(characterEntityID, accountEntityID)
                logger(RankType.WARNING, f"第 {i + 1} 次重试")
                logger(RankType.WARNING, '正在尝试更换代理')
                globals.proxyUsedTime = time.time()
                globals.socks5ip, globals.socks5port = yDailiGet()
                setSocks5ProxyMyth(globals.socks5ip, globals.socks5port,characterEntityID)
                ip, port = startProxyMyth(characterEntityID, accountEntityID, name)
                if isinstance(ip, bool):
                    if not ip:
                        logger(RankType.ERROR, f'启动代理失败 跳过操作')
                        globals.failedCount += 1
                        logoutMyth(accountEntityID, cookie)
                        return
                dailyStatus = autoDaily(ip, port)
                if not isinstance(dailyStatus, bool):
                    break
    # 别他妈炸了我求你了myth
    setSocks5ProxyMyth('', 0, characterEntityID)
    # 关闭代理
    stopProxyMyth(characterEntityID, accountEntityID)
    # 退出Myth
    logoutMyth(accountEntityID, cookie)
    if dailyStatus == 'EXP188':
        int_EXP = int(EXP)
        int_EXP += 188
        EXP = str(int_EXP)
    elif dailyStatus == 'COIN100':
        int_heypixelCoins = int(heypixelCoins)
        int_heypixelCoins += 100
        heypixelCoins = str(int_heypixelCoins)
    if int(heypixelCoins) >= 200:
        existing_data = []
        if os.path.exists('accounts/cache.csv'):
            with open('accounts/cache.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

        # 过滤掉要删除的账号
        updated_data = [row for row in existing_data if row[4] != accountEntityID]

        # 写回缓存 CSV
        writeOutCache('accounts/cache.csv', updated_data)
        logger(RankType.INFO, f'账号已从缓存中删除: {accountEntityID}')

        # 写出文件
        AccountStr = f'[4399][{get_current_time()}][{name}:{characterEntityID}][EXP:{EXP},COIN:{heypixelCoins}]{username}:{password}:{cookie}'
        writeOutfile(f'accounts/output/{get_current_date()}.txt', AccountStr)
        logger(RankType.SUCCESS, '写出文件到OUTPUT成功')
        return
    accountData = [
        [username, password, cookie, name, accountEntityID, characterEntityID, EXP, heypixelCoins, get_current_date()]]
    # 读取现有数据
    existing_data = []
    if os.path.exists('accounts/cache.csv'):
        with open('accounts/cache.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_data = list(reader)

    # 检查是否存在相同的 accountEntityID
    updated = False
    for i, row in enumerate(existing_data):
        if row[4] == accountEntityID:
            existing_data[i] = accountData[0]  # 更新 existing_data 中的行
            updated = True
            logger(RankType.INFO, f'账号缓存已更新: {accountEntityID}')
            break

    # 如果不存在相同的 accountEntityID，则添加新行
    if not updated:
        existing_data.append(accountData[0])

    writeOutCache('accounts/cache.csv', existing_data)  # 传递 existing_data 而不是 accountData
    globals.successCount += 1
    logger(RankType.SUCCESS, '写出文件到CSV缓存成功')
    return


if __name__ == "__main__":
    main()
