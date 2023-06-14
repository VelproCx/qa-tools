import json

def compare_field_values(json_file1, json_file2, field_name):
    resList = []
    with open(json_file1, 'r') as f1, open(json_file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    records1 = data1['testCase']
    records2 = data2
    # 判断记录数量是否相同
    if len(records1) != len(records2):
        print("两个文件记录数量不一致，比对结果不准确，请仔细核对数据，再次进行比对！")
    # 逐组比较字段值并输出结果
    for i, (record1, record2) in enumerate(zip(records1, records2), 1):
        if record1[field_name] == record2[field_name]:
            resList.append('success')
        else:
            print(f"第 {i} 组数据的指定字段值不相同")
            resList.append('failed')
            print("Except:" + str(record1[field_name]) + " ，" + "ordStatus: " + str(record2[field_name]))
    return resList

