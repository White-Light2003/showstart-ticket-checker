# go-cqhttp 配置指南

## 1. 下载 go-cqhttp

访问 https://github.com/Mrs4s/go-cqhttp/releases 下载最新版本

- Windows 64位: `go-cqhttp_v1.2.0_windows_amd64.zip`
- Windows 32位: `go-cqhttp_v1.2.0_windows_386.zip`

## 2. 解压并初始化

解压后将可执行文件放在项目根目录，进入文件夹后双击运行，它会提示：

```
[WARNING]: 当前版本 v1.2.0 运行正常
请选择你要使用的通信方案:
> 0: HTTP POST
  1: HTTP API
  2: 正向 WebSocket
  3: 反向 WebSocket
```

选择 `3` (反向 WebSocket)，然后会生成 `config.yml` 配置文件。

## 3. 修改 config.yml

将以下配置替换进去（注意修改 QQ账号密码）：

```yaml
account:
  uin: 你的QQ号
  password: "你的QQ密码"
  encrypt_password: false
  password_encrypted: ""
  enable_db: true
  access_token: ""
  relogin:
    enabled: true
    relogin_delay: 3
    max_relogin_times: 0
  _rate_limit:
    enabled: true
    frequency: 30
    bucket_size: 1
  ignore_invalid_cqcode: false
  force_fragmented: false
  fix_url: false
  use_ssoAddress: true
  debug: false

servers:
  - ws:
      reverse: true
      universal: ws://127.0.0.1:8080/onebot/v11/ws
      access_token: ""
      reconnection: true
      reconnect_interval: 3000
```

## 4. 启动 go-cqhttp

双击运行 go-cqhttp.exe，如果是首次运行，需要扫码登录。

## 5. 验证运行状态

运行后看到类似以下日志表示成功：
```
[INFO] CQ WebSocket 服务已启动: ws://127.0.0.1:8080/onebot/v11/ws
```
