import json

from DrissionPage import WebPage
import requests
from lib.log import logger, RankType
from lib import globals
import random


# 我看看怎么事
# AccountEntityID = UserID 账号id eg.
# CharacterID 角色id eg.

def pingMyth():
    url = 'http://127.0.0.1:14250/base/Ping'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功连接Myth本地服务')
                    return True
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False
    except requests.RequestException as e:
        logger(RankType.ERROR, f'Myth请求失败: {e}')
        return False


def loginMyth(username, password):
    try:
        web = WebPage()
        web.get('http://127.0.0.1:14250/auth/jwt/login?returnTo=%2Fdashboard')
        web.ele('#:r1:').input(username)
        web.ele('#:r2:').input(password)
        web.ele('#:r3:').click()
    except Exception as e:
        logger(RankType.ERROR, f'登录Myth失败: {e}')
        return False


def loginCookie(cookie):
    url = 'http://localhost:14250/netass/authlogin'
    try:
        sauth_json = json.loads(cookie)
        realcookie = sauth_json['sauth_json']
        data = {
            "username": realcookie,
            "passwordHash": "",
            "IsSauth": True,
            "attributes": {
                "VERIFY_CODE": None,
            },
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if 'msg' in response_data:
                    logger(RankType.ERROR, response_data['msg'])
                    return False
                elif 'data' in response_data and 'EntityID' in response_data['data']:
                    checkStatusURL = f'http://127.0.0.1:14250/netass/IsAccountOnline/ID/{response_data["data"]["EntityID"]}'
                    response = requests.get(checkStatusURL)
                    response.raise_for_status()  # 检查请求是否成功
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            if response_data["code"] == 0:
                                logger(RankType.INFO, f'成功加载 AccountEntityID: {response_data["data"]["EntityID"]}')
                                #globals.IsLoginSuccess = True
                                return response_data['data']['EntityID']
                            else:
                                logger(RankType.WARNING, f'登录失败 正在重试: {response_data["msg"]}')
                                return False
                        except ValueError:
                            logger(RankType.ERROR, 'Value Error')
                            return False
                else:
                    logger(RankType.ERROR, '返回的参数中没有 EntityID')
                    return False
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False


def createGameName(accountEntityID, name):
    url = 'http://127.0.0.1:14250/launcher/AddCharacter'
    try:
        data = {
            "UserID": f'{accountEntityID}',
            "GameID": "4661334467366178884",
            "GameType": 2,
            "Name": f'{name}'
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功创建角色: {response_data["data"]["Name"]}')
                    logger(RankType.INFO, f'CharacterEntityID: {response_data["data"]["EntityID"]}')
                    globals.IsCreateCharacterSuccess = True
                    return response_data['data']['EntityID']
                else:
                    logger(RankType.ERROR, '未知错误')
                    return False
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False
        else:
            logger(RankType.ERROR, f'请求失败 状态码:{response.status_code}')
            try:
                response_data = response.json()
                logger(RankType.ERROR, f'请求失败: {response_data["msg"]}')
                return False
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False


def startProxyMyth(characterEntityID, accountEntityID, name):
    url = f'http://127.0.0.1:14250/launcher/StartGameAuthServer/{accountEntityID}'
    try:
        data = {
            "IsNotDownloadClient": True,
            "IsProxyServer": True,
            "IsRental": False,
            "Role": {
                "EntityID": characterEntityID,
                "GameID": "4661334467366178884",
                "GameType": 2,
                "Name": name,
                "UserId": accountEntityID
            }
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    ip = {response_data['data']['ProxyServerIP']}
                    port = {response_data['data']['ProxyServerPort']}
                    ip = list(ip)[0] if isinstance(ip, set) else ip
                    port = list(port)[0] if isinstance(port, set) else port
                    logger(RankType.SUCCESS, f'成功启动代理服务器: {ip}:{str(port)}')
                    globals.IsStartProxySuccess = True
                    return ip, port
                else:
                    logger(RankType.ERROR, '未知错误')
                    return False,0
            except ValueError:
                logger(RankType.ERROR, 'Value Error')
                return False,0
        else:
            logger(RankType.ERROR, f'请求失败 状态码:{response.status_code}')
            return False,0
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False,0
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False,0


def stopProxyMyth(characterEntityID, accountEntityID):
    url = f'http://127.0.0.1:14250/yggdrasil/StopProxyServer/{accountEntityID}/{characterEntityID}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功关闭代理服务器')
                    return True
                else:
                    logger(RankType.ERROR, '未知错误')
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


def logoutMyth(accountEntityID, cookie):
    url = 'http://127.0.0.1:14250/netass/ClearAccount'
    try:
        data = {
            "EntityID": f'{accountEntityID}',
            "UserName": f'{cookie}',
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功删除账号: {accountEntityID}')
                    return True
                else:
                    logger(RankType.ERROR, '未知错误')
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

def getServerListMyth(accountEntityID):
    url = f'http://127.0.0.1:14250/launcher/GetNetGameList/{accountEntityID}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.SUCCESS, f'成功获取服务器列表 服务器数: {response_data["count"]}')
                    return True
                else:
                    logger(RankType.ERROR, '获取服务器列表失败')
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


def getNetGameAddressMyth(accountEntityID):
    url = f'http://127.0.0.1:14250/launcher/GetNetGameAddress/{accountEntityID}/4661334467366178884'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.INFO, f'成功获取服务器IP: {response_data["data"]["IP"]}')
                    return True
                else:
                    logger(RankType.ERROR, '获取服务器信息失败')
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


def getCharacterNumMyth(accountEntityID):
    url = 'http://127.0.0.1:14250/launcher/QueryCharacterList'
    try:
        data = {
            "GameID": '4661334467366178884',
            "GameType": 2,
            "UserID": accountEntityID,
        }
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.ERROR, f'账号角色数: {response_data["count"]}')
                    return response_data['count']
                else:
                    logger(RankType.ERROR, '未知错误')
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


def setRandomSkinMyth(accountEntityID):
    skinIndex = ['4622719213331109643', '4643725081589755560', '4624314571974668765', '4644239300407481330',
                 '4628439246879359586', '4626946281787191700', '4621895361534351625', '4625061431256632416',
                 '4643586537044611823', '4624308908070700905', '4624330490437611577', '4624328734560728978',
                 '4622744875689819625', '4630453462487981159', '4629269573534524410', '4631919375301710491',
                 '4621809262144673289', '4621936098769159446', '4629155122685916337', '4645321013820735152',
                 '4621723937143378573', '4637884058389204765', '4629664091370388563', '4626725529540284969',
                 '4627931762979915680', '4628740839214606927', '4623097325545012372', '4625236424267758351',
                 '4625304907757850365', '4631964861609884429', '4636099142744386977', '4638086061143164436',
                 '4621936352098917508', '4638174627175992823', '4629441585276850397', '4622609510960208723',
                 '4627651514626184307', '4631805151530524152', '4630124675777835843', '4621936430219404769',
                 '4626411800070627625', '4636070656413319686', '4631646687677683670', '4621834913477988929',
                 '4630742682548765428', '4637842318891056780', '4621810636341866640', '4629468115246140100',
                 '4641855432473069407', '4625588201958383822', '4630986116845094984', '4625899780375138603',
                 '4629729759450953769', '4630742814119626385', '4624328454976766289', '4632641200347294956',
                 '4621809483273324800', '4632761833855790548', '4643288170845694037', '4654539227825831370',
                 '4649566712145807751', '4635827372097789344', '4628816706865870274', '4622118385964411282',
                 '4633384101662086133', '4630596390570717531', '4629441684440972654', '4641368613609444632',
                 '4632492478891846010', '4638174728245446648', '4635980745947360742', '4624328283197100157',
                 '4627763999204836776', '4631321246940057369', '4635553535259885883', '4633272968252626166',
                 '4625257774115075354', '4626411897824451759', '4628218186436853646', '4624293559161339220',
                 '4632693474757198209', '4660557793517601009', '4638044408750035376', '4624293430820096054',
                 '4633576483496583028', '4640829579487585523', '4627764081254308188', '4641788310040339166',
                 '4633159038402974649', '4627647318839483603', '4627958646567592493', '4644567503829100713',
                 '4629326956013331045', '4635341906541929313', '4659438591722280769', '4637490667278500367',
                 '4649432027170688968', '4631503183427313897', '4636291537264316433', '4644035770469965163']
    random_entity_id = random.choice(skinIndex)
    url = f'http://127.0.0.1:14250/launcher/SetPlayerSkinList/{accountEntityID}/{random_entity_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_data = response.json()
                if response_data['code'] == 0:
                    logger(RankType.SUCCESS, f'成功修改皮肤: {random_entity_id}')
                    return True
                else:
                    logger(RankType.ERROR, '修改皮肤失败')
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


def setSocks5ProxyMyth(ip, port, characterEntityID,username='', password=''):
    url = 'http://127.0.0.1:14250/app/SetSetting/post'
    try:
        yunip = {
            "Key": 'RIPAppConfig.Socks5',
            "Value": '',
        }
        response = requests.post(url, json=yunip)
        response.raise_for_status()  # 检查请求是否成功
        host = {
            "Key": f'RIPAppConfig.Socks5Host.{characterEntityID}',
            "Value": ip,
        }
        response = requests.post(url, json=host)
        response.raise_for_status()  # 检查请求是否成功
        port = {
            "Key": f'RIPAppConfig.Socks5Port.{characterEntityID}',
            "Value": port,
        }
        response = requests.post(url, json=port)
        response.raise_for_status()  # 检查请求是否成功
        user = {
            "Key": f'RIPAppConfig.Socks5User.{characterEntityID}',
            "Value": username,
        }
        response = requests.post(url, json=user)
        response.raise_for_status()  # 检查请求是否成功
        password = {
            "Key": f'RIPAppConfig.Socks5Pass.{characterEntityID}',
            "Value": password,
        }
        response = requests.post(url, json=password)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        logger(RankType.ERROR, f'请求失败: {e}')
        return False
    except Exception as e:
        logger(RankType.ERROR, f'未知错误: {e}')
        return False
