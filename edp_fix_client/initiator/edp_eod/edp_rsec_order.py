import argparse
import csv
import logging
import re
import time
from model.logger import setup_logger
import yaml

from common.utils import download_eod, get_date, validate_date_format





class Validator:
    def __init__(self, env, filename):
        self.env = env
        self.filename = filename
        self.data_list = []
        self.current_field = []
        # 定义常量
        self.EDP_HRT_ORDER = "EDP_HRT_Order"
        self.RSEC_MARKET_DATA = "EDP_RSec_MarketData"
        self.RSEC_ORDER = "EDP_RSec_Order"
        self.VALID_SIDES = ["1", "2"]
        self.VALID_MARKET = "EDP"
        self.VALID_QUOTE_VENUE = "XTKS"
        self.VALID_TIME_IN_FORCE = "0"
        # report
        setup_logger('self.logfix', '{}_report.log'.format(filename))
        self.logfix = logging.getLogger('self.logfix')

    # 将csv文件的数据存入list中
    def data_generation(self):
        download_eod(self.env, self.filename)
        # 打开csv文件
        open_file = "{}_{}.csv".format(self.filename, get_date())
        self.logfix.info(open_file)
        with open('temp_file/' + open_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # 获取表头
            self.current_field = header
            # 循环读取数据存入列表
            for row in csv_reader:
                data_dict = dict(zip(header, row))
                self.data_list.append(data_dict)

    # 判断字段是否存在并且顺序正常
    def validate_eod_field(self):
        with open('cfg/edp_field.yaml', 'r') as file:
            yaml_data = file.read()
            data = yaml.safe_load(yaml_data)
            accept_field = data[self.filename]

        for current, accept in zip(self.current_field, accept_field):
            if current == accept:
                # print(f"Field inconsistency: {current}")
                pass
            else:
                self.logfix.error("Field not inconsistency: current:{current}，accept:{accept}")
        self.logfix.info(f"字段验证完成")

    # 判断数据是否正常
    def validate_eod_data(self):
        self.data_generation()
        self.validate_eod_field()
        errors = []
        # 打印数据列表
        for data_dict in self.data_list:
            # 提取共有字段
            # 判断Side是否为空,并且是否是规则内的值1：Buy/2：Sell
            if not data_dict["Side"] or data_dict["Side"] not in self.VALID_SIDES:
                errors.append('Side not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderQty是否为空
            if not data_dict["OrderQty"]:
                errors.append('OrderQty not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderID是否为空，因规则是自定的，ID规则无需校验
            if not data_dict["OrderID"]:
                errors.append('OrderID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderPrice是否为空
            if not data_dict["OrderPrice"]:
                errors.append('OrderPrice not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断Symbol是否为空是
            if not data_dict["Symbol"]:
                errors.append('Symbol not inconsistency, OrderID: {}'.format(data_dict["OrderID"]))
            elif (self.filename != self.EDP_HRT_ORDER and ".EDP" in data_dict["Symbol"]) or (
                    self.filename == "EDP_HRT_Order" and ".EDP" not in data_dict["Symbol"]):
                errors.append('Symbol not inconsistency, OrderID: {}'.format(data_dict["OrderID"]))

            # 为EDP_HRT_Order文件做单独验证
            if self.filename == self.EDP_HRT_ORDER:
                # 判断ClOrdID是否为空，因规则是自定的，ID规则无需校验
                if not data_dict["ClOrdID"]:
                    errors.append('ClOrdID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断OrderType是否为空，并且是否是规则内的值1：Market/2：Limit
                if not data_dict["OrderType"] or data_dict["OrderType"] not in ["1", "2"]:
                    errors.append('OrderType not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断OrderType是否为空，规则内的值0：Day,因为hrt的订单只能为Day
                if not data_dict["TimeInForce"] or data_dict["TimeInForce"] != "0":
                    errors.append('TimeInForce not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断TransactionTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                if not data_dict["TransactionTime"] or not validate_date_format(data_dict["TransactionTime"]):
                    errors.append('TransactionTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断OrderVenue是否为空，是否为规则内的值‘EDP’
                if not data_dict["OrderVenue"] and data_dict["OrderVenue"] != "EDP":
                    errors.append('OrderVenue not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断OrderStatus是否为空
                if not data_dict["OrderStatus"] or data_dict["OrderStatus"] not in ["2", "4", "8"]:
                    errors.append('OrderStatus not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
            else:
                # 判断Account是否为空及Account是否为当前环境的Account
                if not data_dict["Account"].strip() and 'R{}_EDP_ACCOUNT_'.format(env) not in data_dict["Account"]:
                    errors.append('Account not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断Market是否为空，是否为规则内的值‘EDP’
                if not data_dict["Market"] and data_dict["Market"] != "EDP":
                    errors.append('Market not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                # 为EDP_RSec_MarketData文件做单独验证
                if self.filename == self.RSEC_MARKET_DATA:
                    # 判断TransactionTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                    if not data_dict["TransactionTime"] or not validate_date_format(data_dict["TransactionTime"]):
                        errors.append('TransactionTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断QuoteVenue是否为空，是否为规则内的值‘XTKS’
                    if not data_dict["QuoteVenue"] and data_dict["QuoteVenue"] != "XTKS":
                        errors.append('QuoteVenue not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断QuoteTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                    if not data_dict["QuoteTime"] or not validate_date_format(data_dict["QuoteTime"]):
                        errors.append('QuoteTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断QuotePrice是否为空
                    if not data_dict["QuotePrice"]:
                        errors.append('QuotePrice not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断QuoteQty是否为空
                    if not data_dict["QuoteQty"]:
                        errors.append('QuoteQty not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                else:
                    # 判断PrimaryLastPx是否为空
                    if data_dict["PrimaryLastPx"]:
                        # 因为EDP_RSec_Order被拒绝的订单可能存在BBO为0的情况，故需要判断正在检查的是否为EDP_RSec_Order
                        if self.filename != self.RSEC_ORDER:
                            # 判断BBO是否为0.0000
                            if data_dict["PrimaryLastPx"] != "0.0000":
                                pass
                            else:
                                errors.append('PrimaryLastPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                        else:
                            pass
                    else:
                        errors.append('PrimaryLastPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断PrimaryBidPx是否为空
                    if data_dict["PrimaryBidPx"]:
                        # 因为EDP_RSec_Order被拒绝的订单可能存在BBO为0的情况，故需要判断正在检查的是否为EDP_RSec_Order
                        if self.filename != self.RSEC_ORDER:
                            # 判断BBO是否为0.0000
                            if data_dict["PrimaryBidPx"] != "0.0000":
                                pass
                            else:
                                errors.append('PrimaryBidPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                        else:
                            pass
                    else:
                        errors.append('PrimaryBidPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    # 判断PrimaryAskPx是否为空
                    if data_dict["PrimaryAskPx"]:
                        # 因为EDP_RSec_Order被拒绝的订单可能存在BBO为0的情况，故需要判断正在检查的是否为EDP_RSec_Order
                        if self.filename != self.RSEC_ORDER:
                            # 判断BBO是否为0.0000
                            if data_dict["PrimaryAskPx"] != "0.0000":
                                pass
                            else:
                                errors.append('PrimaryAskPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                        else:
                            pass
                    else:
                        errors.append('PrimaryAskPx not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                    if self.filename == 'EDP_RSec_Order':
                        # 判断OrderType是否为空，规则内的值3：Day,因为Rsec的订单只能为IOC
                        if not data_dict["TimeInForce"] or data_dict["TimeInForce"] != "3":
                            errors.append('TimeInForce not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断CashMargin是否为空，规则内的值1：Cash
                        if not data_dict["CashMargin"] and data_dict["CashMargin"] != "1":
                            errors.append('CashMargin not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断MarginTransactionType是否为空，规则内的值0：None
                        if not data_dict["MarginTransactionType"] or data_dict["MarginTransactionType"] != "0":
                            errors.append(
                                'MarginTransactionType not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断OrderType是否为空，并且是否是规则内的值1：Market/2：Limit
                        if not data_dict["OrderType"] or data_dict["OrderType"] not in ["1", "2"]:
                            errors.append('OrderType not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断OrderEventType是否为空
                        if not data_dict["OrderEventType"]:
                            errors.append('OrderEventType not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断MarginTransactionType是否为空
                        if not data_dict["OrderAckNo"]:
                            errors.append('OrderAckNo not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断TransactionTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                        if not data_dict["TransactionTime"] or not validate_date_format(
                                data_dict["TransactionTime"]):
                            errors.append(
                                'TransactionTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断OrderVenue是否为空，是否为规则内的值‘EDP’
                        if not data_dict["OrderVenue"] or data_dict["OrderVenue"] != "EDP":
                            errors.append('OrderVenue not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                    else:
                        # 判断Counterparty是否为空，是否为规则内的值RSEC_PROP
                        if not data_dict["Counterparty"] or data_dict["Counterparty"] != "RSEC_PROP":
                            errors.append('Counterparty not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断VenueExecID是否为空
                        if not data_dict["VenueExecID"]:
                            errors.append('VenueExecID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断TradePrice是否为空,成交单TradePrice不能为0
                        if not data_dict["TradePrice"] or data_dict["TradePrice"] == "0.0000":
                            errors.append('TradePrice not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断TradeQty是否为空,成交单TradeQty不能为0
                        if not data_dict["TradeQty"] or data_dict["TradeQty"] == "0":
                            errors.append('TradeQty not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断TradeTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                        if not data_dict["TradeTime"] or not validate_date_format(data_dict["TradeTime"]):
                            errors.append(
                                'TradeTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断PrimaryPriceFlag是否为空，是否为规则内的值‘EDP’
                        if not data_dict["PrimaryPriceFlag"] or data_dict["PrimaryPriceFlag"] not in ["1", "9", "0"]:
                            errors.append('PrimaryPriceFlag not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断ToSTNeTOrderID是否为空
                        if not data_dict["ToSTNeTOrderID"]:
                            errors.append('ToSTNeTOrderID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断ToSTNeTExecutionID是否为空
                        if not data_dict["ToSTNeTExecutionID"]:
                            errors.append(
                                'ToSTNeTExecutionID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                        # 判断ToSTNeTTransactionTime是否为空，时间规则是否符合yyyy-MM-dd HH:mm:ss.nnnnnn000
                        if not data_dict["ToSTNeTTransactionTime"] and not validate_date_format(
                                data_dict["ToSTNeTTransactionTime"]):
                            errors.append(
                                'ToSTNeTTransactionTime not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
        self.logfix.info(errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', default='UAT', help='1、SIT 2、UAT')
    parser.add_argument('-f', default='EDP_RSec_Order', help='...')
    args = parser.parse_args()

    validator = Validator(args.e, args.f)
    validator.validate_eod_data()


if __name__ == '__main__':
    main()
