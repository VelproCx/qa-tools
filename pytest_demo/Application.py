import time
import quickfix as fix

__SOH__ = chr(1)


class Application(fix.Application):


    def __init__(self):
        super().__init__()
        self.received_messages = []
        self.sessionID = None

    def onCreate(self, sessionID):
        # "服务器启动时候调用此方法创建"
        self.sessionID = sessionID
        print("onCreate : Session ({})".format(sessionID.toString()))
        return

    def onLogon(self, sessionID):
        # "客户端登陆成功时候调用此方法"
        self.sessionID = sessionID
        print("Successful Logon to session '{}'.".format(sessionID.toString()))
        return

    def onLogout(self, sessionID):
        # "客户端断开连接时候调用此方法"
        print("Session ({}) logout !".format(sessionID.toString()))
        return

    def toAdmin(self, message, sessionID):
        # "发送会话消息时候调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        print("(Core) S >> {}".format(msg))
        return

    def toApp(self, message, sessionID):
        # "发送业务消息时候调用此方法"
        print("-------------------------------------------------------------------------------------------------")
        msg = message.toString().replace(__SOH__, "|")
        print("(sendMsg) New Ack >> {}".format(msg))
        return

    def fromAdmin(self, message, sessionID):
        # "接收会话类型消息时调用此方法"
        msg = message.toString().replace(__SOH__, "|")
        print("(Core) R << {}".format(msg))
        return

    def fromApp(self, message, sessionID):
        print("-------------------------------------------------------------------------------------------------")

        received_msg = str(message)
        symbol = message.getField(55)
        # if symbol == '7203':
        #     self.ORDERS_DICT = message.getField(11)
        #     print(self.ORDERS_DICT)

        self.received_messages.append(received_msg)
        time.sleep(1)
        # self.received_messages = received_msg
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass