import json
import logging

logfix = logging.getLogger('logfix')


def compare_field_values(self, json_file1, json_file2, field_name1, field_name2):
    resList = []
    with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    records1 = data1['testCase']
    records2 = data2
    # 判断记录数量是否相同
    if len(records1) != len(records2):
        # 逐组比较字段值并输出结果
        for i, (record1, record2) in enumerate(zip(records1, records2), 1):
            if record1[field_name1] == ["8"]:
                if record1[field_name2] in record1[field_name2]:
                    self.Success += 1
                    resList.append('success')
                else:
                    print("failed")
                    self.Fail += 1
                    logfix.info(f"第 {i} 条数据的指定字段值不相同" + "," + "errorCode:" + str(record2['errorCode']))
                    resList.append('failed')
                    logfix.info(
                        "Except:" + str(record1[field_name1]) + " ，" + "ordStatus: " + str(record2[field_name1]))
            elif record1[field_name1] == record2[field_name1]:
                self.Success += 1
                resList.append("success")
            else:
                self.Fail += 1
                logfix.info(f"第 {i} 条数据的指定字段值不相同" + "," + "clordId:" + str(record2['clordId']))
                resList.append("failed")
                logfix.info("Except:" + str(record1[field_name1]) + " ，" + "ordStatus: " + str(record2[field_name1]))

    else:
        logfix.info("两个文件记录数量不一致，比对结果不准确，请仔细核对数据，再次进行比对！")
    return resList
