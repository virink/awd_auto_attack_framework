<?php

error_reporting(0);

define("WEBROOT", $_SERVER['DOCUMENT_ROOT']);
define("LOGDIR", "_logs");

class FlowLog
{
    public function __construct()
    {
        $this->flow = array();
        $this->log_path = WEBROOT . '/' . LOGDIR . '/';
        mkdir($this->log_path, 0777, 1);
        $this->Flow();
    }

    private function Save($keyword="vk")
    {
        $data = $this->flow;
        file_put_contents(
            $this->log_path . date("d-h") . ".log",
            "=====================================\r\n" .
            "Keyword : " . implode(", ", $keyword) . "\r\n" .
            print_r($data, true) . "\r\n",
            FILE_APPEND
        );
    }

    private function Flow()
    {
        foreach ($_SERVER as $key => $value) {
            if (stripos("HTTP_", $key)) {
                $this->flow['header'][ucwords(strtolower($key))] = $_SERVER["HTTP_" . $key];
            }
        }
        $this->flow['method'] = $_SERVER['REQUEST_METHOD'];
        $this->flow['protocol'] = $_SERVER['SERVER_PROTOCOL'];
        $this->flow['time'] = date('Y-m-d H:i:s', $_SERVER['REQUEST_TIME']);
        isset($_SERVER['CONTENT_TYPE']) && $this->flow['ctype'] = @$_SERVER['CONTENT_TYPE'];
        $this->flow['ip'] = array(
            'REMOTE_ADDR' => @$_SERVER['REMOTE_ADDR'],
            'CLIENT-IP' => @$_SERVER['HTTP_CLIENT_IP'],
            'X-FORWARDED-FOR' => @$_SERVER['HTTP_X_FORWARDED_FOR'],
        );

        /* GetData */
        $this->flow['uri'] = $_SERVER['REQUEST_URI'];
        $this->flow['get'] = print_r(parse_url($_SERVER['REQUEST_URI']), 1);

        /* PostData */
        if (strtolower($_SERVER['CONTENT_TYPE']) != 'multipart/form-data') {
            $this->flow['post'] = file_get_contents('php://input');
        } elseif (isset($_POST) or strtolower($this->flow['method']) == 'post') {
            $this->flow['post'] = print_r($_POST, 1);
        }
        // Save
        $this->Save();
    }
}

header("X-Waf-Defense: Virink");

new FlowLog();
