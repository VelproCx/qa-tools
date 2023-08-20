#!/usr/bin/python3
# -*- coding: utf-8 -*-
import grpc
from gen.connamara.ep3.v1beta1 import order_entry_api_pb2, order_entry_api_pb2_grpc
from gen.connamara.ep3.instruments.v1beta1 import instruments_api_pb2, instruments_api_pb2_grpc, instruments_api_pb2, \
    instruments_api_pb2_grpc
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2
from gen.connamara.ep3.auth.v1beta1 import basic_auth_api_pb2_grpc
import argparse

AUTH_HOST = 'adminauth.sit.rsec.oddlotx.com:443'
ADMIN_HOST = 'adminapi.sit.rsec.oddlotx.com:443'

PRODUCT = ['ROLB', 'ROLS', 'REXB', 'REXS']


def login(username, password):
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(AUTH_HOST, credentials=creds)

    stub = basic_auth_api_pb2_grpc.BasicAuthAPIStub(channel)
    response = stub.Login(basic_auth_api_pb2.LoginRequest(username=username, password=password))
    return response


def createOrderEntryConnection(access_token):
    # 证书选择SSL类型
    creds = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(target=ADMIN_HOST, credentials=creds,
                                  options=[('grpc.max_send_message_length', 20 * 1024 * 1024),
                                           ('grpc.max_receive_message_length', 20 * 1024 * 1024)], )

    connection = instruments_api_pb2_grpc.InstrumentsAPIStub(channel=channel)
    return connection


def modSymbolsStatus(access_token, conn, symbols_list, status):
    meta = [('authorization', access_token)]

    if 'open' == status:
        for symbol in symbols_list:
            for product in PRODUCT:
                conn.UpdateInstrumentState(
                    instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol + '.' + product,
                                                                     state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_OPEN),
                    metadata=meta)
    elif 'close' == status:
        for symbol in symbols_list:
            for product in PRODUCT:
                conn.UpdateInstrumentState(
                    instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol + '.' + product,
                                                                     state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_CLOSED),
                    metadata=meta)
    else:
        for symbol in symbols_list:
            for product in PRODUCT:
                conn.UpdateInstrumentState(
                    instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol + '.' + product,
                                                                     is_scheduled=True,
                                                                     state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_CLOSED),
                    metadata=meta)


def modSymbolsStatusForNoProduct(access_token, conn, symbols_list, status):
    meta = [('authorization', access_token)]

    if 'open' == status:
        for symbol in symbols_list:
            conn.UpdateInstrumentState(instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol,
                                                                                        state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_OPEN),
                                       metadata=meta)
    elif 'close' == status:
        for symbol in symbols_list:
            conn.UpdateInstrumentState(instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol,
                                                                                        state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_CLOSED),
                                       metadata=meta)
    else:
        for symbol in symbols_list:
            conn.UpdateInstrumentState(
                instruments_api_pb2.UpdateInstrumentStateRequest(instrument_id=symbol, is_scheduled=True,
                                                                 state=instruments_api_pb2.InstrumentState.INSTRUMENT_STATE_CLOSED),
                metadata=meta)


def listSymbolsTofile(access_token, conn, file):
    list_symb = listSymbols(access_token, conn)
    wf = open(file, 'w+', encoding='utf-8')
    for item in list_symb:
        wf.write(item + '\n')


def allSymbolsOpen(access_token, conn, status):
    list = []

    list_symb = listSymbols(access_token, conn)
    for item in list_symb:
        list.append(item)
    print(list)
    modSymbolsStatusForNoProduct(access_token, conn, list, status)


def allRolSymbolsOpen(access_token, conn, status):
    list = []

    list_symb = listSymbols(access_token, conn)
    for item in list_symb:
        if 'ROL' == item[-4:-1]:
            list.append(item)
    print(list)
    modSymbolsStatusForNoProduct(access_token, conn, list, status)


def allRexSymbolsOpen(access_token, conn, status):
    list = []

    list_symb = listSymbols(access_token, conn)
    for item in list_symb:
        if 'REX' == item[-4:-1]:
            list.append(item)
    print(list)
    modSymbolsStatusForNoProduct(access_token, conn, list, status)


def listSymbols(access_token, conn):
    meta = [('authorization', access_token)]

    rst = conn.ListSymbols(instruments_api_pb2.ListSymbolsRequest(), metadata=meta)
    return rst.symbols


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EP3 Symbols status modification tool')

    parser.add_argument('-u', '--user_name', default="admin",
                        help='user name to use for test, default: admin')

    parser.add_argument('-p', '--password', default="admin@123$%^",
                        help='user password to use for test')

    parser.add_argument('-s', '--status', default="on", choices=['on', 'off', 'follow'],
                        help='Set the symbol status to on or off or follow product')

    parser.add_argument('--symbols', default="7267,6758,9432,8306,9984,9434,8035,4063,4661,6367,6501",
                        help='Comma separated list of symbols, example: 7267,6758')

    parser.add_argument('--adm_auth_host', default="adminauth.sit.rsec.oddlotx.com:443",
                        help='admin grpc auth host, example: adminauth.sit.rsec.oddlotx.com:443')

    parser.add_argument('--adm_host', default="adminapi.sit.rsec.oddlotx.com:443",
                        help=' admin grpc api host, example: adminapi.sit.rsec.oddlotx.com:443')

    parser.add_argument('-l', '--list_admin_symbols', action='store_true', help='Query the list of all symbols in ep3')

    parser.add_argument('--file', default="data/ep3_symbols.txt",
                        help='Save the list of all symbols in ep3')

    parser.add_argument('--open_all', action='store_true',
                        help='open/close all symbols in ep3, need -s to specify status')

    parser.add_argument('--rol_open_all', action='store_true',
                        help='open/close all symbols of ROL in ep3, need -s to specify status')

    parser.add_argument('--rex_open_all', action='store_true',
                        help='open/close all symbols of REX in ep3, need -s to specify status')

    try:
        args = parser.parse_args()
        symbls = args.symbols.split(',')
        AUTH_HOST = args.adm_auth_host
        ADMIN_HOST = args.adm_host

        file = args.file

        print("user name : " + args.user_name)
        print("user password : " + args.password)
        print("symbol status : " + args.status)
        print("symbols : " + str(symbls))
        print("admin grpc auth host : " + AUTH_HOST)
        print("admin grpc api host : " + ADMIN_HOST)
        print("file : " + file)

        login_info = login(args.user_name, args.password)
        connection = createOrderEntryConnection(login_info.access_token)

        if args.list_admin_symbols:
            listSymbolsTofile(login_info.access_token, connection, file)
            print("Successfully finished")
        elif args.open_all:
            allSymbolsOpen(login_info.access_token, connection, args.status)
            print("Successfully finished")
        elif args.rol_open_all:
            allRolSymbolsOpen(login_info.access_token, connection, args.status)
            print("Successfully finished")
        elif args.rex_open_all:
            allRexSymbolsOpen(login_info.access_token, connection, args.status)
            print("Successfully finished")
        else:
            modSymbolsStatus(login_info.access_token, connection, symbls, args.status)
            print("Successfully finished")

    except Exception as e:
        print("Exception : ", e)
        exit(-1)
