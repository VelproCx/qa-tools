#!/bin/sh
cd /Users/elevenchen/Desktop/qa-tools/gRpc_py
python3 sit_client.py
sleep 15


cd /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_regression_test
sleep 5
python3 edp_regression_client.py edp_client.cfg
