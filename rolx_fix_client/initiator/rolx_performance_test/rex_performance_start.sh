#!/bin/sh
# cd /app/data/auto_fix_client/initiator/rolx_performance_test
# sleep 5
# python3 /app/data/auto_fix_client/initiator/rolx_performance_test/rolx_full_stock_client.py /app/data/auto_fix_client/initiator/rolx_performance_test/rolx_full_stock_client.cfg


sleep 3
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_1 --Sender RSIT_ROLX_1 --Target FSX_SIT_ROLX --Host clientgateway101 --Port 5001 -m 15000 -s 5
&
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_2 --Sender RSIT_ROLX_2 --Target FSX_SIT_ROLX --Host clientgateway102 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_3 --Sender RSIT_ROLX_3 --Target FSX_SIT_ROLX --Host clientgateway103 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_4 --Sender RSIT_ROLX_4 --Target FSX_SIT_ROLX --Host clientgateway104 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_5 --Sender RSIT_ROLX_5 --Target FSX_SIT_ROLX --Host clientgateway105 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_6 --Sender RSIT_ROLX_6 --Target FSX_SIT_ROLX --Host clientgateway106 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_7 --Sender RSIT_ROLX_7 --Target FSX_SIT_ROLX --Host clientgateway107 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_8 --Sender RSIT_ROLX_8 --Target FSX_SIT_ROLX --Host clientgateway108 --Port 5001 &
python3 /app/data/qa-tools/rolx_fix_client/initiator/rolx_performance_test/rolx_performance_application.py --account RSIT_ACCOUNT_9 --Sender RSIT_ROLX_9 --Target FSX_SIT_ROLX --Host clientgateway109 --Port 5001 &
