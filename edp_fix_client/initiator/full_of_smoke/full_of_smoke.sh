#!/bin/sh
sleep 3
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_1 -target FSX_UAT_EDP -sender RUAT_EDP_1 -host clientgateway101 -port 5001 -tor 30 &
sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_2 -target FSX_UAT_EDP -sender RUAT_EDP_2 -host clientgateway102 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_3 -target FSX_UAT_EDP -sender RUAT_EDP_3 -host clientgateway103 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_4 -target FSX_UAT_EDP -sender RUAT_EDP_4 -host clientgateway104 -port 5001 -tor 30
#sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_5 -target FSX_UAT_EDP -sender RUAT_EDP_5 -host clientgateway105 -port 5001 -tor 30 &
sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_6 -target FSX_UAT_EDP -sender RUAT_EDP_6 -host clientgateway106 -port 5001 -tor 30 &
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_7 -target FSX_UAT_EDP -sender RUAT_EDP_7 -host clientgateway107 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_8 -target FSX_UAT_EDP -sender RUAT_EDP_8 -host clientgateway108 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_9 -target FSX_UAT_EDP -sender RUAT_EDP_9 -host clientgateway109 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_10 -target FSX_UAT_EDP -sender RUAT_EDP_10 -host clientgateway110 -port 5001 -tor 30
#sleep 2
#python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/full_of_smoke.py -account RUAT_EDP_ACCOUNT_99 -target FSX_UAT_EDP -sender RUAT_EDP_99 -host clientgateway99 -port 5001 -tor 30
#sleep 2



