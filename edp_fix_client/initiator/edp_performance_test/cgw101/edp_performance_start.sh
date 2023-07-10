#!/bin/sh
# cd /app/data/auto_fix_client/initiator/edp_performance_test/cgw101
# sleep 5
# python3 /app/data/auto_fix_client/initiator/edp_performance_test/cgw101/rol_load_client.py /app/data/auto_fix_client/initiator/edp_performance_test/cgw101/rol_load_client.cfg


cd ./edp_fix_client/initiator/edp_performance_test/cgw101
sleep 5
python3 edp_performance_client.py edp_performance_client.cfg

