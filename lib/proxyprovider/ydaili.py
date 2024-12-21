from lib import config
from lib.log import logger, RankType
import requests

def yDailiGet():
    url = config.yDailiAPIUrl
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['status'] == 'success':
                    data = response_data["data"]
                    if data:
                        ip, port = data[0]["IP"].split(":")
                        logger(RankType.INFO, f'成功获取代理IP: {ip}:{port}')
                        return ip, port
                    else:
                        logger(RankType.INFO, '获取代理IP失败，data为空')
                        return False, 0
                else:
                    logger(RankType.ERROR, '获取代理IP失败')
                    return False, 0
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False, 0
        else:
            logger(RankType.ERROR, f'请求失败 状态码:{response.status_code}')
            return False, 0
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False, 0
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False, 0
