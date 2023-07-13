import json

file_path = "/Users/zhenghuaimao/Desktop/qa-tools/edp_fix_client/initiator/edp_regression_test/case/EDP_Functional_Test_Matrix.json"

def updateCaseid1(case_file):
    with open(case_file, "r") as f:
        date = json.load(f)

    testCase = date["testCase"]
    for i, testCase in enumerate(testCase):
        if i == 0:
            testCase["Id"] = "1"
        else:
            testCase["Id"] = str(i + 1)

    with open(case_file, "w") as file:
        json.dump(date, file)
        print("id更新完成，请打开{}文件更新显示样式".format(file_path))


updateCaseid1(file_path)


