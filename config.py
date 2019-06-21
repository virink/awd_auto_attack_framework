#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging

# === RSA ===
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
xxx
-----END RSA PRIVATE KEY-----""".strip()
RSA_AGENT = "http://127.0.0.1:8085/agent.php"
# === RSA ===

# === LOG ===
LOG_FILE = './logs/attack.log'
LOG_LEVEL = logging.INFO
LOG_FMT = '[%(asctime)s] - %(levelname)8s %(message)s'
# === LOG ===

# === FLAG ===
FLAG_PATTERN = [
    # ICQ AWD (uuid)
    re.compile(r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', re.I | re.M),
    # Normal
    re.compile(r'((flag)?({(.*?)}))', re.I | re.M)
]
# === FLAG ===
