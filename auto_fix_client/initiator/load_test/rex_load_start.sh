#!/bin/sh
cd ./initiator/load_test
sleep 5
python3 rex_load_client.py rex_load_client.cfg
