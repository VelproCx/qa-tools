import argparse
import csv
import time

import yaml

from common.utils import download_eod, get_date

env = ''
filename = ''


class Validate:
    data_list = []
    current_field = []

    # download_eod(env, filename)

    # 将csv文件的数据存入list中
    def data_generation(self):
        # 打开csv文件
        open_file = "{}_{}.csv".format(filename, get_date())
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
        with open('cfg/edp_field.yaml', 'r') as file:
            yaml_data = file.read()
            data = yaml.safe_load(yaml_data)
            accept_field = data[filename]

        for current, accept in zip(self.current_field, accept_field):
            if current == accept:
                # print(f"Field inconsistency: {current}")
                pass
            else:
                print("Field not inconsistency: current:{current}，accept:{accept}")
        print(f"字段验证完成")

    # 判断数据是否正常
    def validate_eod_data(self):
        self.data_generation()
        self.validate_eod_field()
        # 打印数据列表
        for data_dict in self.data_list:
            # 提取共有字段
            # 判断Side是否为空及是否为正确的值
            if data_dict["Side"] and data_dict["Side"] == "1" or data_dict["Side"] == "2":
                pass
            else:
                print('Side not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断Side是否为空
            if data_dict["OrderQty"]:
                pass
            else:
                print('OrderQty not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderID是否为空，因规则是自定的，ID规则无需校验
            if data_dict["OrderID"]:
                pass
            else:
                print('OrderID not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

            # 判断OrderPrice是否为空是否等于0.0000,yinw
            if data_dict["OrderPrice"]:
                pass
            else:
                print('OrderPrice not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))

                # 判断账号是否为空及账号是否为当前环境的账号
            if data_dict["Account"].strip() and 'R{}_EDP_ACCOUNT_'.format(env) in data_dict["Account"]:
                pass
            else:
                print('Account not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
            # 判断Symbol是否为空是否等于0.0000
            if data_dict["Symbol"]:
                if filename != "EDP_HRT_Order":
                    if ".EDP" not in data_dict["Symbol"]:
                        pass
                    else:
                        print('Symbol not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
                else:
                    if ".EDP" in data_dict["Symbol"]:
                        pass
                    else:
                        print('Symbol not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
            else:
                print('Symbol not inconsistency,OrderID:{}'.format(data_dict["OrderID"]))
            # 其他字段值校验在后面添加
            # for key, value in data_dict.items():
            #     if key
            #     print(f"{key}: {value}")
            #     time.sleep(10)


def main():
    global env
    global filename
    # 使用argparse的add_argument方法进行传参
    parser = argparse.ArgumentParser()  # 创建对象
    parser.add_argument('-e', default='UAT', help='1、SIT 2、UAT')
    parser.add_argument('-f', default='EDP_RSec_Order',
                        help='1、EDP_RSec_Order 2、EDP_RSec_Trade 3、EDP_RSec_MarketData 4、EDP_HRT_Trade 5、EDP_HRT_Order')

    args = parser.parse_args()  # 解析参数
    env = args.e
    filename = args.f
    validate_instance = Validate()
    validate_instance.validate_eod_data()


if __name__ == '__main__':
    main()
