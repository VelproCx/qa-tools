#!/bin/sh
#cd ./initiator
#sleep 5
#python3 rolx_regression_client.py rolx_client.cfg

sleep 5
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_regression_test/rol_regression_application.py -account RSIT_ACCOUNT_1 -sender RSIT_1 -target FSX_SIT_CGW_1 -host 10.4.65.1 -port 5001
