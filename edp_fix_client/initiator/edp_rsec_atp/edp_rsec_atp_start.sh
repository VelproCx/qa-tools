#!/bin/sh
sleep 5
python3 edp_hrt_application.py --data '{
    "Source": "your_source",
    "Ip": "192.168.0.20",
    "Port": "11113",
    "Sender": "TRADER_C",
    "Target": "terminal_1",
    "Account": "RSIT_EDP_ACCOUNT_1",
    "Market": "EDP",
    "ActionType": "NewAck",
    "Price":"2023",
    "OrderQty": 100,
    "OrdType": "2",
    "Side": "1",
    "Symbol": "9989.EDP",
    "SecurityID":"509090809",
    "TimeInForce": "0",
    "CrossingPriceType": "EDP",
    "OrderCapacity": "P",
    "CashMargin": "1",
    "MarginTransactionType": "0",
    "MinQty": 0,
    "OrderClassification": "3",
    "SelfTradePreventionId": "0",
    "ExDestination":"EiB Market"}
'