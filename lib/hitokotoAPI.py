import requests

from lib.log import RankType
from lib.log import logger


def get_hitokoto():
    try:
        url = "https://v1.hitokoto.cn/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['from'] is None:
                data['from'] = ""
            return data['hitokoto']
        else:
            return "Netw0rk Err0r"
    except Exception as e:
        logger(RankType.ERROR,f'获取一言出现错误: {e}')
        return '我喜欢你'
