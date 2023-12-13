import argparse
import csv
import time

from common.utils import download_eod, get_date

run_env = ''


class Validate:
    data_list = []
    current_field = []
    env = run_env
    filename = 'EDP_RSec_Order'

    # download_eod(env, filename)

    # 将csv文件的数据存入list中
    def data_generation(self):
        # 打开csv文件
        open_file = "{}_{}.csv".format(self.filename, get_date())
        print(open_file)
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
        print(self.current_field)
        accept_field = ['Account', 'OrderID', 'OrderPrice', 'OrderQty', 'Side', 'Market', 'Symbol', 'TimeInForce',
                        'CashMargin', 'MarginTransactionType', 'OrderType', 'OrderEventType', 'OrderAckNo',
                        'TransactionTime', 'OrderVenue', 'PrimaryLastPx', 'PrimaryBidPx', 'PrimaryAskPx']
        for current, accept in zip(self.current_field, accept_field):
            if current == accept:
                # print(f"Field inconsistency: {current}")
                pass
            else:
                print(f"Field not inconsistency: current:{current}，accept:{accept}")
        print(f"字段验证完成")

    # 判断数据是否正常
    def validate_eod(self):
        self.data_generation()
        self.validate_eod_field()
        # 打印数据列表
        for data_dict in self.data_list:
            # 判断账号是否为空及账号是否为当前环境的账号
            if data_dict["Account"].strip() and 'R{}_EDP_ACCOUNT_'.format(self.env) in data_dict["Account"]:
                pass
            else:
                print('Account not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderID是否为空，因规则是自定的，ID规则无需校验
            if data_dict["OrderID"]:
                pass
            else:
                print('OrderID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderPrice是否为空是否等于0.0000
            if data_dict["OrderPrice"] and data_dict["OrderPrice"] == "0.0000":
                # 因只有OrderType == 1 的情况下，orderPrice为0.0000，故需要判断OrderType
                if data_dict["OrderType"] == "1":
                    pass
                else:
                    print('OrderPrice not inconsistency,Because OrderType != 1 OrderID:{}'.format(data_dict["OrderID"]))
            else:
                print('OrderPrice not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 其他字段值校验在后面添加
            # for key, value in data_dict.items():
            #     if key
            #     print(f"{key}: {value}")
            #     time.sleep(10)


def main():
    global run_env
    # 使用argparse的add_argument方法进行传参
    parser = argparse.ArgumentParser()  # 创建对象
    parser.add_argument('-e', default='UAT', help='SIT/UAT')
    parser.add_argument('-f', default='EDP_RSec_Order', help='Example:EDP_RSec_Order')

    args = parser.parse_args()  # 解析参数
    run_env = args.e
    validate_instance = Validate()
    validate_instance.validate_eod()


if __name__ == '__main__':
    main()
