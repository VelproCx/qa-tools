import json
import requests
import warnings


class RunMethod(object):

    def post_main(self, url, headers, data=None):
        # 忽略不安全的请求告警信息
        warnings.filterwarnings("ignore")

        response = requests.post(url=url, headers=headers, data=data, verify=False)

        return response

    def get_main(self, url, headers, data=None):

        # 忽略不安全的请求告警信息
        warnings.filterwarnings("ignore")

        response = requests.get(url=url, headers=headers, data=data, verify=False)

        return response

    def run_main(self, method, url, headers, data):

        # 忽略不安全的请求告警信息
        warnings.filterwarnings("ignore")

        # 判断调用接口的时候传的请求方式
        if method == "POST":
            response = self.post_main(url, headers, data)
        elif method == "GET":
            response = self.get_main(url, headers, data)
        # 将 Python 对象编码成 JSON 字符串
        # return json.dumps(response, ensure_ascii=False, sort_keys=False, indent=2)
        # 将响应的的数据以字典数据结构和json数据格式返回
        # return res.json()
        return response.json()


if __name__ == "__main__":
    run = RunMethod()
    method = "POST"
    url = "http://adminui.sit.fsx.oddlotx.com//api/admin/auth/login"
    data = json.dumps({
        "email": "admin@fsx.com",
        "password": "ab12345678",
        "verifyCode": 111
        }
    )
    headers = {
        'Content-Type': 'application/json'
    }
    result = run.run_main(method, url, headers, data)
    print(result)
