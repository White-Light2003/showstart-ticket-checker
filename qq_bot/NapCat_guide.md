# NapCat QQ 协议端部署指南

## 为什么推荐 NapCat？

- ✅ 基于 NTQQ 协议，比 go-cqhttp 更稳定
- ✅ 内存占用低（50-100MB）
- ✅ 支持 WebSocket 连接 NoneBot2
- ✅ Windows/Linux/MacOS 都支持

## 部署步骤

### 1. 下载 NapCat

访问 GitHub 下载最新版本：
https://github.com/NapNeko/NapCatQQ/releases

找到 Windows 版本下载（NapCat_windows_x64.zip 或类似文件名）

### 2. 解压并运行

1. 解压到任意目录
2. 双击运行 `NapCat.exe`
3. 首次运行会提示登录，用手机QQ扫码即可

### 3. 获取 WebSocket 连接信息

NapCat 默认会开启 WebSocket 服务，地址通常是：
- WebSocket: `ws://127.0.0.1:6099/onebot/v11/ws`

### 4. 修改 NoneBot2 配置

编辑 `qq_bot/.env` 文件：

```env
# Driver 配置
DRIVER=~httpx+~websockets

# NapCat 的 WebSocket 地址（默认端口 6099）
CQHTTP_WS_URL=ws://127.0.0.1:6099/onebot/v11/ws

# NapCat 如果设置了 access_token，在这里填入
# CQHTTP_ACCESS_TOKEN=你的token
```

### 5. 启动顺序

1. 先启动 NapCat（确保 QQ 已登录）
2. 再启动 NoneBot2

```bash
cd qq_bot
python bot.py
```

## 常见问题

### Q: NapCat 连接 NoneBot2 失败？
A: 检查以下几点：
1. NapCat 是否正常运行
2. 端口 6099 是否被占用
3. WebSocket URL 是否匹配（注意端口号）

### Q: 如何查看 NapCat 配置？
A: NapCat 会在首次运行后在目录生成配置文件

### Q: go-cqhttp 的配置还能用吗？
A: 不兼容，需要重新配置。NapCat 使用不同的配置文件格式。

## NapCat + NoneBot2 架构图

```
┌─────────────┐         WebSocket          ┌─────────────────┐
│   NapCat    │ ←─────────────────────────→│    NoneBot2     │
│  (协议端)   │      ws://127.0.0.1:6099   │   (应用框架)    │
│             │                             │                 │
│  登录 QQ    │                             │  秀动余票插件   │
└─────────────┘                             └─────────────────┘
```

有问题随时问！
