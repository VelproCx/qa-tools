#!/bin/sh
cd /app/data/auto_fix_client/initiator/trading_hours_test/cgw101
#本地调试路径：
#/initiator/trading_hours_test/cgw101
#uat调试路径：
#/app/data/auto_fix_client/initiator/trading_hours_test/cgw101
sleep 5
python3 /app/data/auto_fix_client/initiator/trading_hours_test/cgw101/rol_tradingHours_client.py /app/data/auto_fix_client/initiator/trading_hours_test/cgw101/rol_tradingHours_client.cfg
#本地调试路径：
#/initiator/trading_hours_test/cgw101/rol_tradingHours_client.py  /initiator/trading_hours_test/cgw101/rol_tradingHours_client.cfg
#uat调试路径：
#/app/data/auto_fix_client/initiator/trading_hours_test/cgw101/rol_tradingHours_client.py  /app/data/auto_fix_client/initiator/trading_hours_test/cgw101/rol_tradingHours_client.cfg