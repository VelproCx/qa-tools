#!/bin/sh
# cd /app/data/auto_fix_client/initiator/edp_performance_test
# sleep 5
# python3 /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.py /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.cfg


sleep 3
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_1 --Target FSX_SIT_EDP --Host clientgateway101 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_2 --Target FSX_SIT_EDP --Host clientgateway102 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_3 --Target FSX_SIT_EDP --Host clientgateway103 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_4 --Target FSX_SIT_EDP --Host clientgateway104 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_5 --Target FSX_SIT_EDP --Host clientgateway105 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_6 --Target FSX_SIT_EDP --Host clientgateway106 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_7 --Target FSX_SIT_EDP --Host clientgateway107 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_8 --Target FSX_SIT_EDP --Host clientgateway108 --Port 5001 &
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py --account RSIT_EDP_ACCOUNT_1 --Sender RSIT_EDP_9 --Target FSX_SIT_EDP --Host clientgateway109 --Port 5001 &
