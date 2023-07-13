##!/bin/sh
#cd /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101
#sleep 5
#python3 /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101/edp_fullstock_client.py /app/data/auto_fix_client/initiator/rolx_full_stock_test/cgw101/edp_fullstock_client.cfg


#!/bin/sh
cd /Users/zhenghuaimao/Desktop/qa-tools/gRpc_py
python3 sit_client.py
sleep 10


cd /Users/zhenghuaimao/Desktop/qa-tools/edp_fix_client/initiator/edp_full_stock_test/cgw101
sleep 5
python3 edp_fullstock_client.py edp_fullstock_client.cfg


