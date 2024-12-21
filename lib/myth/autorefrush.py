from DrissionPage import WebPage
from lib.log import logger, RankType

web = WebPage()
logger(RankType.INFO, '开启网页')
web.get('http://127.0.0.1:14250/auth/jwt/login?returnTo=%2Fdashboard')

# 尝试查找元素并执行操作
# try:
#     # 查找登录页面元素
#     login_page_element = web.ele('#:r0:')
#     if login_page_element:
#         logger('INFO', '检测到登录页面')
#         username_element = web.ele('#:r1:')
#         if username_element:
#             username_element.input('AlexBlock')
#             logger('INFO', '输入账号')
#         else:
#             logger('WARNING', '未找到账号输入框，跳过输入账号')
#         password_element = web.ele('#:r2:')
#         if password_element:
#             password_element.input('2nwMI92Ubi0yXtJ')
#             logger('INFO', '输入密码')
#         else:
#             logger('WARNING', '未找到密码输入框，跳过输入密码')
#         login_button_element = web.ele('#:r3:')
#         if login_button_element:
#             login_button_element.click()
#             logger('INFO', '点击登录')
#         else:
#             logger('WARNING', '未找到登录按钮，跳过点击登录')
#     else:
#         logger('WARNING', '未检测到登录页面，跳过登录操作')
# except Exception as e:
#     logger('ERROR', f'元素查找失败: {e}')

web.get('http://127.0.0.1:14250/dashboard/minecraft/netease/account')
logger(RankType.INFO, '进入账号管理页面')
web.get('http://127.0.0.1:14250/dashboard/minecraft/netease/server/net')
logger(RankType.INFO, '进入服务器列表页面')
