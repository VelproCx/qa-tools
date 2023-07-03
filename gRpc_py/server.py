import grpc
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2_grpc

from datetime import datetime

def timestamp_to_datetime(timestamp):
    # 将时间戳转换为datetime对象
    dt = datetime.fromtimestamp(timestamp)
    return dt


def uat_user():
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('traderauth.uat.rsec.oddlotx.com:443', credentials=creds)
    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(username='HRT_UAT_USER_1', password='hrtuatuser1'))
    print(response)
    return response

def sit_user():
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('traderauth.sit.rsec.oddlotx.com:443', credentials=creds)
    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(username='HRT_SIT_USER_1', password='hrtsituser1'))
    # print(response)
    return response




if __name__ == '__main__':
    a = uat_user()
    sit_user()
    # prod_user_second()