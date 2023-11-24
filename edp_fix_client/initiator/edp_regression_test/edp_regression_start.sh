#!/bin/sh

sleep 5
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_4 -target FSX_UAT_EDP -host clientgateway104 -port 5001

