#!/bin/sh
sleep 5

python3 edp_hrt_application.py --data '{
    "Ip": "10.4.128.117",
    "Port": "11131",
    "Sender": "HRT_SIT_EDP_D_1",
    "Target": "s_t2",
    "Account": "HRT_SIT_EDP_ACCOUNT_1",
    "Market": "EDP",
    "ActionType": "NewAck",
    "Price":"2023",
    "OrderQty": 10000,
    "OrdType": "2",
    "Side": "2",
    "Symbol": "9989.EDP",
    "SecurityID":"509090809",
    "TimeInForce": "1",
    "CrossingPriceType": "EDP",
    "OrderCapacity": "A",
    "CashMargin": "1",
    "MarginTransactionType": "0",
    "MinQty": 0,
    "OrderClassification": "3",
    "SelfTradePreventionId": "0",
    "ExDestination":"EiB Market"}
'

#python3 edp_hrt_atp_batch_application.py -m 2 -s 5 -t 10
#python3 edp_hrt_atp_batch_application.py -m 100000 -s 5 -t 9

#python3 edp_hrt_application.py --data '{
#    "Ip": "192.168.0.20",
#    "Port": "11113",
#    "Sender": "TRADER_C",
#    "Target": "terminal_1",
#    "Account": "HRT_SIT_EDP_ACCOUNT_2",
#    "Market": "EDP",
#    "ActionType": "NewAck",
#    "Price":"2023",
#    "OrderQty": 10000,
#    "OrdType": "2",
#    "Side": "2",
#    "Symbol": "8750.EDP",
#    "SecurityID":"509090809",
#    "TimeInForce": "1",
#    "CrossingPriceType": "EDP",
#    "OrderCapacity": "P",
#    "CashMargin": "1",
#    "MarginTransactionType": "0",
#    "MinQty": 0,
#    "OrderClassification": "3",
#    "SelfTradePreventionId": "0",
#    "ExDestination":"EiB Market"}
#'


