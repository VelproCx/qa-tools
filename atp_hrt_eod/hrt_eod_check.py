import csv
import re
from tqdm import tqdm
__SOH__ = chr(1)


class AtpEod:
    order_num = 0
    order_datas_list = []
    trade_num = 0
    trade_datas_list = []

    @classmethod
    def sum_eod_num(cls):
        with open("logs/fix_terminal2_20231201.log", "r") as file:
            for line in tqdm(file):
                if "send" in line and "35=8" in line and "56=HRT_UAT_EDP_D_1" in line:
                    if "39=0" in line:

                        cls.order_num += 1
                        order_data = re.sub(r"\x01", "|", line)
                        print(order_data)
                        cls.order_datas_list.append(order_data)

                    elif "39=1" in line or "39=2" in line:
                        # with open("logs/trade.log", "a") as logs:
                        #     log_data = re.sub(r"\x01", "|", line)
                        #     logs.write(log_data)
                        cls.trade_num += 1
                        trade_data = re.sub(r"\x01", "|", line)
                        cls.trade_datas_list.append(trade_data)
                else:
                    pass
        print(cls.order_num, cls.trade_num)

    @classmethod
    def generate_hrt_order_eod(cls):
        header = [
            "ClOrdID",
            "OrderID",
            "OrderPrice",
            "OrderQty",
            "Side",
            "Symbol",
            "OrderType",
            "TimeInForce",
            "TrasactionTime",
            "OrderVenue",
            "OrderStatus"
        ]
        with open("logs/fix_terminal2_20231118.bk.log", "r") as f:
            for log_data in tqdm(f):
                if "send" in log_data and "35=8" in log_data and "39=0" in log_data:
                    cls.order_num += 1
                    # print(log_data)
                    str_log_data = re.findall(r'send (.*?)10=', log_data)
                    # print(str_log_data[0])
                    log_data_list = str_log_data[0].split("\x01")

                    # client_order_id = re.findall(r"|11=(.*?)(?=14=)", log_data_list)
                    # print(log_data_list)
                    # cls.order_datas_list.append(log_data_list)
                else:
                    pass
        with open("HRT_Order.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(cls.order_datas_list)

        return


if __name__ == '__main__':
    AtpEod.sum_eod_num()
