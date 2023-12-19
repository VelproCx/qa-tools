#!/bin/sh

sleep 3
python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py -f EDP_RSec_Order
sleep 30
python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py -f EDP_HRT_Trade
sleep 30
python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py -f EDP_HRT_Order
sleep 30
python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py -f EDP_RSec_MarketData
#sleep 30
#python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py -f EDP_RSec_Trade
#sleep 1
#python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py
#sleep 1
#python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py
#sleep 1
#python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py
#sleep 1
#python3 /Users/elevenchen/Desktop/qa-tools/edp_fix_client/initiator/edp_eod/edp_eod.py
