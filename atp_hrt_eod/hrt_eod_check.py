import csv
import re
from tqdm import tqdm

__SOH__ = chr(1)


class AtpEod:
    edp_order_num_acc = 0
    edp_order_num_rej = 0
    edp_order_num_exc = 0
    edp_order_num_fill = 0
    edp_order_datas_list = []
    trade_num = 0
    trade_datas_list = []

    rol_order_num_acc = 0
    rol_order_num_rej = 0
    rol_order_num_exc = 0
    rol_order_num_fill = 0
    rol_order_datas_list = []

    @classmethod
    def sum_eod_num(cls):
        with open("logs/fix_terminal2_20240109.log", "r") as file:
            for line in tqdm(file):
                if "send" in line and "35=8" in line:
                    if "56=HRT_UAT_EDP_D_" in line and "49=s_t" in line:

                        if "39=8" in line:
                            cls.edp_order_num_rej += 1
                            order_data = re.sub(r"\x01", "|", line)
                            # print(order_data)
                            cls.edp_order_datas_list.append(order_data)
                        if "39=4" in line:
                            cls.edp_order_num_exc += 1
                            order_data = re.sub(r"\x01", "|", line)
                            # print(order_data)
                            cls.edp_order_datas_list.append(order_data)
                        if "39=2" in line or "39=1":
                            cls.edp_order_num_fill += 1
                            order_data = re.sub(r"\x01", "|", line)
                            # print(order_data)
                            cls.edp_order_datas_list.append(order_data)
                        # if "39=0" in line:
                        #     cls.order_num_acc += 1
                        #     order_data = re.sub(r"\x01", "|", line)
                        #     # print(order_data)
                        #     cls.order_datas_list.append(order_data)
                        cls.trade_num += 1
                        trade_data = re.sub(r"\x01", "|", line)
                        cls.trade_datas_list.append(trade_data)


                elif "56=HRT_SIT_ROL_D" in line and "49=s_t" in line:
                    if "39=8" in line:
                        cls.rol_order_num_rej += 1
                        order_data = re.sub(r"\x01", "|", line)
                        # print(order_data)
                        cls.rol_order_datas_list.append(order_data)
                    if "39=4" in line:
                        cls.rol_order_num_exc += 1
                        order_data = re.sub(r"\x01", "|", line)
                        # print(order_data)
                        cls.rol_order_datas_list.append(order_data)
                    if "39=2" in line or "39=1":
                        cls.rol_order_num_fill += 1
                        order_data = re.sub(r"\x01", "|", line)
                        print(order_data)
                        cls.rol_order_datas_list.append(order_data)
                    if "39=0" in line:
                        cls.edp_order_num_acc += 1
                        order_data = re.sub(r"\x01", "|", line)
                        # print(order_data)
                        cls.rol_order_datas_list.append(order_data)
                    cls.trade_num += 1
                    trade_data = re.sub(r"\x01", "|", line)
                    cls.trade_datas_list.append(trade_data)

            print(f"rol Eod check:rej: {cls.rol_order_num_rej}, exe: {cls.rol_order_num_exc}, "
                  f"fill: {cls.rol_order_num_fill}, acc: {cls.rol_order_num_acc}")
            print(f"rol Eod check:rej: {cls.edp_order_num_rej}, exe: {cls.edp_order_num_exc}, "
                  f"fill: {cls.edp_order_num_fill}, acc: {cls.edp_order_num_acc}")


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
        with open("logs/fix_terminal2_20231211.log", "r") as f:
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
    # print('order:{}'.format(1654705+125+244+0+278115+66+4197+0))
    # print('trade:{}'.format(313+4584))
