#!/bin/sh
export elmck=$1
# 调用乐园币脚本
node ./ele_lyb.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay

# 调用2048脚本
node ./ele_2048.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay

# 调用成语闯关脚本
node ./ele_cycg.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay

# 调用美食摊脚本
node ./ele_mst.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay

# 调用合成甜蜜蜜脚本
node ./ele_hctmm.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay

# 调用饿了么资产推送脚本
node ./饿了么资产推送.js

# 延时
delay=$(( ($RANDOM % 6) + 5 ))
echo "延时 $delay 秒以防止黑号..."
sleep $delay
