#!/bin/sh
cd ./initiator
sleep 5
python3 rolx_regression_client.py rolx_client.cfg

sleep 5
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_regression_test/rolx_regression_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_4 -target FSX_UAT_EDP -host clientgateway104 -port 5001
