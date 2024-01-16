import json

import pandas as pd

from model.logger import setup_logger
import logging
import csv

setup_logger('logfix', 'logs/eod_check_report.log')
logfix = logging.getLogger('logfix')


# csv 转 json
def csv_to_json(csv_file, json_file):
    csvfile = open(csv_file, 'r')
    jsonfile = open(json_file, 'w')
    reader = csv.DictReader(csvfile)
    out = json.dumps([row for row in reader])
    jsonfile.write(out)


# xlsx 转 csv
def xlsx_to_csv(xlsx_file, sheet_index, start_cell, csv_file):
    df = pd.read_excel(xlsx_file, sheet_name=sheet_index, header=None, engine='openpyxl')
    start_row = int(start_cell[1]) - 1
    start_col = ord(start_cell[0].upper()) - 65
    df = df.iloc[start_row:, start_col:]
    df.to_csv(csv_file, index=False, header=False)


# 文件内容比对
def compare_json_files(file_a, file_b):
    with open(file_a, 'r') as f:
        data_a = json.load(f)

    with open(file_b, 'r') as f:
        data_b = json.load(f)
    # print(len(data_a), len(data_b))
    # 判断文件数量是否相同
    if len(data_a) == len(data_b):
        for impacted_order_list in data_a:
            for eod_order_list in data_b:
                # 判断ClOrdID是否相同，相同则继续判断LastPx及BBO情报
                if int(impacted_order_list['ClOrdID']) == int(eod_order_list['OrderID']):
                    if impacted_order_list['LastPx'] != eod_order_list['TradePrice']:
                        logfix.info(
                            'ClOrdId:' + str(
                                impacted_order_list['ClOrdID']) + ',' + 'LastPx 不同,' + 'impactedOrderLastPx: ' + str(
                                impacted_order_list['LastPx']) + ',' + 'eodOrderLastPx:' + str(
                                eod_order_list['TradePrice']))
                    if impacted_order_list['Side'] != eod_order_list['Side']:
                        logfix.info(
                            'ClOrdId:' + str(
                                impacted_order_list['ClOrdID']) + ',' + 'Side 不同,' + 'impactedOrderSide: ' + str(
                                impacted_order_list['Side']) + ',' + 'eodOrderSide:' + str(eod_order_list['Side']))
                    if impacted_order_list['PrimaryLastPx'] != eod_order_list['PrimaryLastPx']:
                        logfix.info('ClOrdId:' + str(
                            impacted_order_list[
                                'ClOrdID']) + ',' + 'PrimaryLastPx 不同,' + 'impactedOrderPrimaryLastPx: ' + str(
                            impacted_order_list['PrimaryLastPx']) + ',' + 'eodOrderPrimaryLastPx:' + str(
                            eod_order_list['PrimaryLastPx']))
                    if impacted_order_list['PrimaryBidPx'] != eod_order_list['PrimaryBidPx']:
                        logfix.info('ClOrdId:' + str(
                            impacted_order_list[
                                'ClOrdID']) + ',' + 'PrimaryBidPx 不同,' + 'impactedOrderPrimaryBidPx: ' + str(
                            impacted_order_list['PrimaryBidPx']) + ',' + 'eodOrderPrimaryBidPx:' + str(
                            eod_order_list['PrimaryBidPx']))
                    if impacted_order_list['PrimaryAskPx'] != eod_order_list['PrimaryAskPx']:
                        logfix.info('ClOrdId:' + str(
                            impacted_order_list[
                                'ClOrdID']) + ',' + 'PrimaryAskPx 不同,' + 'impactedOrderPrimaryAskPx: ' + str(
                            impacted_order_list['PrimaryAskPx']) + ',' + 'eodOrderPrimaryAskPx:' + str(
                            eod_order_list['PrimaryAskPx']))
    else:
        logfix.info('impacted_order_list 与 eod_order_list 数量不一致,' + 'impacted_order_list:' + str(len(
            data_a)) + ',' + 'eod_order_list:' + str(len(data_b)))
    logsCheck()


# 对保存对log文件进行检查
def logsCheck():
    with open('logs/eod_check_report.log', 'r') as f:
        content = f.read()
    if '不同' in content:
        logfix.info('eod check failed')
    elif '数量不一致' in content:
        logfix.info('eod check failed')
    else:
        logfix.info('eod check success')


def run():
    # xlsx 转 csv
    xlsx_file = 'Impacted Order List_20230608.xlsx'
    sheet_index = 1
    start_cell = 'B3'
    csv_file = 'Impacted_Order_List.csv'
    xlsx_to_csv(xlsx_file, sheet_index, start_cell, csv_file)

    # csv 转 json
    csv_to_json(r'RSec_Trade_20230608.csv', r'Eod_Order_List.json')
    csv_to_json(r'Impacted_Order_List.csv', r'Impacted_Order_List.json')

    # 数据比对
    compare_json_files('Impacted_Order_List.json', 'Eod_Order_List.json')


run()
