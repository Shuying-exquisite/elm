#!/bin/sh
# 饿了么中央控制脚本
#node ./脚本名称.js
#python ./脚本名称.py





# 延时防黑
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay


