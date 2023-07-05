"""FIX GATEWAY"""
import sys
import argparse
import quickfix
from edp_regression_application import Application
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
        time.sleep(5)
        initiator.stop()

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        # initiator.stop()
        sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument("file_name", type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)
