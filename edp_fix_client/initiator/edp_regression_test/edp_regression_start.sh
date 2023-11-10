#!/bin/sh
#cd /app/data/qa-tools/gRpc_py
#python3 /app/data/qa-tools/gRpc_py/sit_regression_client.py
#sleep 10
#
#toolserver
#cd /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test
#sleep 5
#python3 /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.py /app/data/qa-tools/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.cfg
#cd ./initiator/edp_regression_client
#sleep 5
#python3 edp_regression_client.py edp_regression_client.cfg

#jenKens
#cd /var/jenkins_home/workspace/edp_regression_test/gRpc_py
#python3 sit_regression_client.py
#sleep 10
#
#cd /var/jenkins_home/workspace/edp_regression_test/edp_fix_client/initiator/edp_regression_test
sleep 5
python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_regression_test/edp_regression_client.py edp_regression_client.cfg

#本地
#cd /Users/zhenghuaimao/Desktop/qa-tools/gRpc_py
#python3 sit_regression_client.py
#sleep 10
#
#
#cd ./initiator/edp_regression_test
#sleep 5
#python3 edp_regression_client.py edp_regression_client.cfg


python3 main_edp.py /app/data/logs/edp-fsx-uat/clientgateway.log /app/data/logs/edp-fsx-uat/crossreport.log /app/data/logs/edp-fsx-uat/sor.log UAT 106 20231023