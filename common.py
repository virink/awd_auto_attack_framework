#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import re
import requests
import logging
from logging import handlers

from config import LOG_FILE, LOG_LEVEL, \
    LOG_FMT, RSA_PRIVATE_KEY, RSA_AGENT, \
    FLAG_PATTERN

"""
Python RSA ?? PHP RSA

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

RSA_KEY = RSA.importKey(RSA_PRIVATE_KEY)
cipher = Cipher_pkcs1_v1_5.new(RSA_KEY)
sentinel = Random.new().read(15 + SHA.digest_size)

def _rsa_encrypt(data):
    data_chunk = re.findall(r'.{117}', data)
    ret = b''
    for chunk in data_chunk:
        ret += cipher.encrypt(bytes(chunk, 'utf-8'))
    return b64e(ret)


def _rsa_decrypt(data):
    data = b64d(data, 1)
    ret = []
    for p in range(0, len(data), 128):
        ret.append(str(cipher.decrypt(data[p:p + 128]), 'utf-8'))
    return str(b''.join(ret), 'utf-8')
"""


KEYWORDS = [
    'preg_replace', 'bcreate_function', 'passthru("cat /flag")',
    'shell_exec("cat /flag")', 'exec("cat /flag")', 'bbase64_decode',
    'bedoced_46esab', 'eval', 'system("cat /flag")',  'proc_open',
    'popen', 'curl_exec', 'curl_multi_exec', 'parse_ini_file',
    'show_source', 'file_get_contents("/flag")', 'fsockopen("/flag")',
    'cat /flag', 'whoami', 'exec', 'escapeshellcmd', 'assert'
]

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]


class Logger(object):

    _debug = False

    def __init__(self, filename, level, fmt):
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level)
        format_str = logging.Formatter(fmt)
        # Console
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        # File
        fh = logging.FileHandler(filename=filename, encoding='utf-8')
        fh.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        self.logger.toggleDebug = self.toggleDebug

    def toggleDebug(self):
        if self._debug:
            self.logger.setLevel(LOG_LEVEL)
        else:
            self.logger.setLevel(logging.DEBUG)


log = Logger(
    LOG_FILE,
    level=LOG_LEVEL,
    fmt=LOG_FMT
)
logger = log.logger


def md5(text):
    m = hashlib.md5(text.encode())
    return m.hexdigest()


def b64e(c):
    if not isinstance(c, bytes):
        c = bytes(c, 'utf-8')
    return str(base64.b64encode(c), 'utf-8')


def b64d(c, b=0):
    if not isinstance(c, bytes):
        c = bytes(c, 'utf-8')
    ret = base64.b64decode(c)
    return ret if b else str(ret, 'utf-8')


def _rsa_agent(data, query=""):
    res = requests.post(RSA_AGENT + query, data=data)
    return res.text


def rsa_encrypt(data):
    return _rsa_agent(data, "?encrypt=1")


def rsa_decrypt(data):
    return _rsa_agent(data)


def find_flag(data):
    flags = []
    for PATTERN in FLAG_PATTERN:
        m = PATTERN.findall(data)
        if m and m[0]:
            flags.append(m[0][-1])
    return flags


def callback_default(target, resp_text):
    logger.debug("[#] ====== Recv Data ======")
    logger.debug("[#] Target: %s" % target)
    logger.debug("[#] Text: %s" % resp_text)
    logger.debug("[#] ====== Recv Data ======")
    flags = find_flag(resp_text)
    for flag in flags:
        logger.info("[+] Recv Flag : %s -> [[%s]]" % (target, flag))
