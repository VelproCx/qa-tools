#!/bin/sh
# cd /app/data/auto_fix_client/initiator/load_test/cgw101
# sleep 5
# python3 /app/data/auto_fix_client/initiator/load_test/cgw101/rol_load_client.py /app/data/auto_fix_client/initiator/load_test/cgw101/rol_load_client.cfg


cd ./edp_fix_client/initiator/load_test/cgw101
sleep 5
python3 edp_load_client.py edp_load_client.cfg

