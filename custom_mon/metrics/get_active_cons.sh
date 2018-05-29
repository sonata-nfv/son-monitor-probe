#!/usr/bin/env bash

resp=$(curl -s http://10.100.16.42/nginx_status)

if [[ $resp == "Active connections:"* ]];
    then
        words=($resp)
        echo ${words[2]}
    else
        echo "Failed"
fi

