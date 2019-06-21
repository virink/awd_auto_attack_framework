# AWD Auto Attack Framework

辣鸡 Py 毁我青春

## 用法

1. 本地搭建 PHP 及环境
   - PHP
   - openssl - rsa
   - 放入 rsa_agent.php
   - 修改 config.py 的配置
2. 安装 python 相关依赖
   - `pip install -r requirements.txt`
3. 添加自己的shell
4. 运行 main_tests.py 进行测试
## TODO

**auto.py**

- 导入 main.py 的函数
- 自动化运行
  - 定时任务
  - while and sleep ?

## 说明

**mix.py**

- NormalRequest 正常流量请求
- MixRequest    混淆流量请求

**config.py**

- LOG_FILE            日志路径
- LOG_LEVEL           logging.INFO
- LOG_FMT             '[*] [%(asctime)s] - %(levelname)s %(message)s'
- RSA_AGENT           Agent 地址 "http://127.0.0.1:8085/rsa_agent.php"
- RSA_PRIVATE_KEY     RSA 私钥
- FLAG_PATTERN        flag 匹配正则模型
