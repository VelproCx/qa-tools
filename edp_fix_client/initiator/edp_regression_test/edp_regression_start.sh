#!/bin/sh
#cd /app/data/qa-tools/gRpc_py
#python3 /app/data/qa-tools/gRpc_py/sit_regression_client.py
#sleep 10
#
#
#cd /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test
#sleep 5
#python3 /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.py /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.cfg
#cd ./initiator/edp_regression_client
#sleep 5
#python3 edp_regression_client.py edp_regression_client.cfg


cd /var/jenkins_home/workspace/gRpc_py
python3 sit_regression_client.py
sleep 10


cd /var/jenkins_home/workspace/edp_regression_test/edp_fix_client/initiator/edp_regression_test
sleep 5
python3 edp_regression_client.py edp_regression_client.cfg



