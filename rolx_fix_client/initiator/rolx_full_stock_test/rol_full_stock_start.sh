#!/bin/sh
#cd /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101
#sleep 5
#python3 /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101/edp_fullstock_client.py /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101/edp_fullstock_client.cfg

sleep 5
#python3 rolx_full_stock_client.py rolx_full_stock_client.cfg

#python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_full_stock_test/cgw101/rolx_full_stock_application.py -account RSIT_ACCOUNT_1 -sender RSIT_ROLX_1 -target FSX_SIT_ROLX -host 35.74.32.240 -port 5001

python3 /Users/zhenghuaimao/Desktop/qa-tools/rolx_fix_client/initiator/rolx_full_stock_test/cgw101/rol_full_stock_application.py --account RSIT_ACCOUNT_7 --Sender RSIT_ROLX_7 --Target FSX_SIT_ROLX --Host 35.74.32.240 --Port 5001

