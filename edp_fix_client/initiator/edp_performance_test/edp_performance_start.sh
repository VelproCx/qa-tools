#!/bin/sh
# cd /app/data/auto_fix_client/initiator/edp_performance_test
# sleep 5
# python3 /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.py /app/data/auto_fix_client/initiator/edp_performance_test/rolx_full_stock_client.cfg


sleep 3
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_1 -target FSX_UAT_EDP -host clientgateway101 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_2 -target FSX_UAT_EDP -host clientgateway102 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_3 -target FSX_UAT_EDP -host clientgateway103 -port 5001 &
#sleep 1
python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_4 -target FSX_UAT_EDP -host clientgateway104 -port 5001 -m 30000 -s 5
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_5 -target FSX_UAT_EDP -host clientgateway105 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_6 -target FSX_UAT_EDP -host clientgateway106 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_7 -target FSX_UAT_EDP -host clientgateway107 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_8 -target FSX_UAT_EDP -host clientgateway108 -port 5001 &
#sleep 1
#python3 /app/data/qa-tools/edp_fix_client/initiator/edp_performance_test/edp_performance_application.py -account RUAT_EDP_ACCOUNT_1 -sender RUAT_EDP_9 -target FSX_UAT_EDP -host clientgateway109 -port 5001 &
