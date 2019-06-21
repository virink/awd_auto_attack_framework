<?php

class RSA
{
    private static $PUBLIC_KEY = <<<EOF
-----BEGIN PUBLIC KEY-----
xxx
-----END PUBLIC KEY-----
EOF;

    private static $PRIVATE_KEY = <<<EOF
-----BEGIN RSA PRIVATE KEY-----
xxx
-----END RSA PRIVATE KEY-----
EOF;

    private static function getPrivateKey()
    {
        return openssl_pkey_get_private(self::$PRIVATE_KEY);
    }
    private static function getPublicKey()
    {
        return openssl_pkey_get_public(self::$PUBLIC_KEY);
    }
    public static function privateEncrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split($data, 117) as $chunk) {
            openssl_private_encrypt($chunk, $encryptData, self::getPrivateKey());
            $res .= $encryptData;
        }
        return $res ? base64_encode($res) : null;
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

    public static function privateDecrypt($data = '')
    {
        if (!is_string($data)) {
            return null;
        }
        $res = '';
        foreach (str_split(base64_decode($data), 128) as $chunk) {
            openssl_private_decrypt($chunk, $decryptData, self::getPrivateKey());
            $res .= $decryptData;
        }
        return $res ? $res : null;
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
        return $res;
    }
}


$test = new RSA();

$encrypt = isset($_GET['encrypt']);
$data = file_get_contents("php://input");
if ($encrypt == 1) {
    $ret = $test->privateEncrypt($data);
} else {
    $ret = $test->privateDecrypt($data);
    if (!$ret) {
        $ret = $test->publicDecrypt($data);
    }
}
print_r($ret);
