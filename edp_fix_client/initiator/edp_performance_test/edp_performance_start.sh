#!/bin/sh
# cd /app/data/auto_fix_client/initiator/edp_performance_test
# sleep 5
# python3 /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.py /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.cfg


sleep 3
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_1 --Sender RUAT_EDP_1 --Target FSX_UAT_EDP --Host clientgateway101 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_2 --Sender RUAT_EDP_2 --Target FSX_UAT_EDP --Host clientgateway102 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_3 --Sender RUAT_EDP_3 --Target FSX_UAT_EDP --Host clientgateway103 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_4 --Sender RUAT_EDP_4 --Target FSX_UAT_EDP --Host clientgateway104 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_5 --Sender RUAT_EDP_5 --Target FSX_UAT_EDP --Host clientgateway105 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_6 --Sender RUAT_EDP_6 --Target FSX_UAT_EDP --Host clientgateway106 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_7 --Sender RUAT_EDP_7 --Target FSX_UAT_EDP --Host clientgateway107 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_8 --Sender RUAT_EDP_8 --Target FSX_UAT_EDP --Host clientgateway108 --Port 5001 &
sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RUAT_EDP_ACCOUNT_9 --Sender RUAT_EDP_9 --Target FSX_UAT_EDP --Host clientgateway109 --Port 5001 &
