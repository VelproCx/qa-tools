#!/bin/sh
#cd ./initiator
#sleep 5
#python3 rolx_regression_client.py rolx_client.cfg

sleep 5
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_regression_test/rolx_regression_application.py -account RSIT_ACCOUNT_1 -sender RSIT_ROLX_1 -target FSX_SIT_ROLX -host clientgateway101 -port 5001
