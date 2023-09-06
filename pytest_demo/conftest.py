import pytest
import time
import random


# 确保sessionID fixture返回一个可迭代的对象
@pytest.fixture(scope='class')
def sessionID(get_sessionId):
    return get_sessionId,

@pytest.fixture(scope='function')
def getClOrdID():
    # "随机数生成ClOrdID"
    # 获取当前时间并且进行格式转换
    t = int(time.time())
    str1 = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
    ClOrdID = str(t) + str1
    return ClOrdID