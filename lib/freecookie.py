from lib.log import *
import requests

def getNameFreeCookie():
    url = 'https://cookie.alexblock.org/api/v1/freecookie/get/name'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功获取随机名: {response_data["name"]}')
                    return response_data['name']
                else:
                    logger(RankType.ERROR, '未在响应内找到Name字段')
                    return False
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False
        else:
            logger(RankType.ERROR, f'请求失败 状态码:{response.status_code}')
            return False
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False