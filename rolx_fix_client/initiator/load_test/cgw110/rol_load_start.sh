##!/bin/sh
#cd ./initiator/cgw110
#sleep 5
#python3 edp_fullstock_client.py edp_fullstock_client.cfg


#!/bin/sh
cd /app/data/auto_fix_client/initiator/load_test/cgw110
sleep 5
python3 /app/data/auto_fix_client/initiator/load_test/cgw110/rol_load_client.py /app/data/auto_fix_client/initiator/load_test/cgw110/rol_load_client.cfg
