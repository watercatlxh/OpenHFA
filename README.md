# HeypixelCheckIn

## 纯协议的布吉岛服务器自动签到脚本

这个项目是一个用于自动签到布吉岛服务器的 Python 脚本。它通过模拟登录、创建角色、启动代理服务器等操作，实现自动签到功能。

## 功能概述

- **登录功能**：支持通过用户名密码或 Cookie 登录。
- **角色管理**：创建角色并获取角色 ID。
- **代理服务器管理**：启动和停止代理服务器。
- **签到功能**：通过 Mineflayer 连接到服务器并自动签到。
- **日志记录**：使用自定义日志记录功能，方便调试和监控。

## 依赖库

- `DrissionPage`
- `requests`
- `mineflayer`
- `mineflayer-pathfinder`
- `javascript`
- `lib.log`
