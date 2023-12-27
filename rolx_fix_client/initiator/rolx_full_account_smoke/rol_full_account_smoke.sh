#!/bin/sh
sleep 3
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_1 -target FSX_UAT_ROLX -sender RUAT_ROLX_1 -host clientgateway101 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_2 -target FSX_UAT_ROLX -sender RUAT_ROLX_2 -host clientgateway102 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_3 -target FSX_UAT_ROLX -sender RUAT_ROLX_3 -host clientgateway103 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_4 -target FSX_UAT_ROLX -sender RUAT_ROLX_4 -host clientgateway104 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_5 -target FSX_UAT_ROLX -sender RUAT_ROLX_5 -host clientgateway105 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_6 -target FSX_UAT_ROLX -sender RUAT_ROLX_6 -host clientgateway106 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_7 -target FSX_UAT_ROLX -sender RUAT_ROLX_7 -host clientgateway107 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_8 -target FSX_UAT_ROLX -sender RUAT_ROLX_8 -host clientgateway108 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_9 -target FSX_UAT_ROLX -sender RUAT_ROLX_9 -host clientgateway109 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_10 -target FSX_UAT_ROLX -sender RUAT_ROLX_10 -host clientgateway110 -port 5001 &
sleep 2
python3 /app/data/qa-tools/edp_fix_client/initiator/full_of_smoke/rol_full_of_smoke.py -account RUAT_ACCOUNT_99 -target FSX_UAT_ROLX -sender RUAT_ROLX_99 -host clientgateway99 -port 5001 &
sleep 2
