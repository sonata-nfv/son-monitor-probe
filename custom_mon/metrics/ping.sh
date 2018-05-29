#!/usr/bin/env bash
ip=$1

timestamp() {
  date +"%s"
}

#echo $(date '+%Y-%m-%d %H:%M:%S')
resp=$(ping -W3 -c1 $ip | grep ttl)
echo $resp
if [[ $resp ]]
    then
        echo $(timestamp)
    else
        echo "Failed"
fi

