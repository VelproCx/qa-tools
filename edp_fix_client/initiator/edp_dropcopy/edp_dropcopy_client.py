"""FIX GATEWAY"""
import sys
import argparse
from datetime import timedelta, datetime
import quickfix
from edp_dropcopy_application import Application
import time
global initiator


def main(config_file):
    try:
        settings = quickfix.SessionSettings(config_file)
        application = Application()
        storefactory = quickfix.FileStoreFactory(settings)
        logfactory = quickfix.FileLogFactory(settings)
        initiator = quickfix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()

        application.load_test_case()
        # 执行完所有测试用例后等待时间
        sleep_duration = timedelta(minutes=60)
        end_time = datetime.now() + sleep_duration
        while datetime.now() < end_time:
            time.sleep(1)

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument("file_name", type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)
