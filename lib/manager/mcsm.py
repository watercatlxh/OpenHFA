
from lib.file import *
from lib.mineflayer.mineflayer import *

# boom
def getInstancesListMCSM():
    url = f'{config.MCSM_API_URL}/api/service/remote_service_instances'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "page": 0,  # 转换为整数
        "page_size": 20,  # 转换为整数
        "status": "200",  # 转换为字符串
        "instance_name": "[Auto]HeypixelCheckIn-Recheck"  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        logger(RankType.INFO, "成功获取实例列表")
        return instances
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"获取实例列表失败: {e}")
        return None


# {'instanceUuid': 'e5fa103bb0084c0f9b4876d07e0c8b00', 'started': 1499, 'status': 0, 'config': {'nickname': '[Auto]HeypixelCheckIn-Recheck', 'startCommand': 'python3 main.py --recheck', 'stopCommand': '^c', 'cwd': '/root/Heypixel/HeypixelCheckIn', 'ie': 'utf8', 'oe': 'utf8', 'createDatetime': 1726988360431, 'lastDatetime': 1728036195849, 'type': 'universal', 'tag': [], 'endTime': 0, 'fileCode': 'utf8', 'processType': 'general', 'updateCommand': '', 'crlf': 1, 'enableRcon': False, 'rconPassword': '', 'rconPort': 0, 'rconIp': '', 'actionCommandList': [], 'terminalOption': {'haveColor': False, 'pty': True, 'ptyWindowCol': 164, 'ptyWindowRow': 40}, 'eventTask': {'autoStart': True, 'autoRestart': True, 'ignore': True}, 'docker': {'containerName': '', 'image': '', 'ports': [], 'extraVolumes': [], 'memory': 0, 'networkMode': 'bridge', 'networkAliases': [], 'cpusetCpus': '', 'cpuUsage': 0, 'maxSpace': 0, 'io': 0, 'network': 0, 'workingDir': '/workspace/', 'env': []}, 'pingConfig': {'ip': '', 'port': 25565, 'type': 1}, 'extraServiceConfig': {'openFrpTunnelId': '', 'openFrpToken': ''}}, 'info': {'currentPlayers': -1, 'maxPlayers': -1, 'version': '', 'fileLock': 0, 'playersChart': [], 'openFrpStatus': False}, 'space': 0, 'processInfo': {'cpu': 0, 'memory': 0, 'ppid': 0, 'pid': 0, 'ctime': 0, 'elapsed': 0, 'timestamp': 0}}
def getInstanceInfoMCSM():
    url = f'{config.MCSM_API_URL}/api/instance'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "uuid": config.instance_id  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        if instances['status'] == 200:
            logger(RankType.INFO, f"成功获取实例信息{instances['data']}")
            return instances
        else:
            logger(RankType.ERROR, f'获取实例列表失败: {instances}')
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"获取实例列表失败: {e}")
        return None

def startInstanceMCSM():
    url = f'{config.MCSM_API_URL}/api/protected_instance/open'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "uuid": config.instance_id  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        if instances['status'] == 200:
            logger(RankType.INFO, f"成功启动实例")
            return instances
        else:
            logger(RankType.ERROR, f'启动失败: {instances}')
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"启动失败: {e}")
        return None

def stopInstanceMCSM():
    url = f'{config.MCSM_API_URL}/api/protected_instance/stop'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "uuid": config.instance_id  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        if instances['status'] == 200:
            logger(RankType.INFO, f"成功停止实例")
            return instances
        else:
            logger(RankType.ERROR, f'停止失败: {instances}')
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"停止失败: {e}")
        return None

def restartInstanceMCSM():
    url = f'{config.MCSM_API_URL}/api/protected_instance/restart'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "uuid": config.instance_id  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        if instances['status'] == 200:
            logger(RankType.INFO, f"成功重启实例")
            return instances
        else:
            logger(RankType.ERROR, f'重启失败: {instances}')
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"重启失败: {e}")
        return None

def killInstanceMCSM():
    url = f'{config.MCSM_API_URL}/api/protected_instance/kill'
    params = {
        "apikey": config.MCSM_API_KEY,
        "daemonId": config.daemon_id,
        "uuid": config.instance_id  # 修正参数名
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        instances = response.json()
        if instances['status'] == 200:
            logger(RankType.INFO, f"成功强制停止实例")
            return instances
        else:
            logger(RankType.ERROR, f'强制停止失败: {instances}')
    except requests.exceptions.RequestException as e:
        logger(RankType.ERROR, f"强制停止失败: {e}")
        return None

