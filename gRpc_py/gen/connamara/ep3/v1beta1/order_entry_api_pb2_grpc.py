# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from gen.connamara.ep3.v1beta1 import order_entry_api_pb2 as connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2



class OrderEntryAPIStub(object):
    """OrderEntryAPI is the API Surface for connected clients to send and modify orders.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InsertOrder = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrder',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderResponse.FromString,
                )
        self.InsertOrderCross = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrderCross',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossResponse.FromString,
                )
        self.InsertOrderList = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrderList',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListResponse.FromString,
                )
        self.CancelOrder = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/CancelOrder',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderResponse.FromString,
                )
        self.CancelOrderList = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/CancelOrderList',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListResponse.FromString,
                )
        self.CancelReplaceOrder = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/CancelReplaceOrder',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderResponse.FromString,
                )
        self.CancelReplaceOrderList = channel.unary_unary(
                '/connamara.ep3.v1beta1.OrderEntryAPI/CancelReplaceOrderList',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListResponse.FromString,
                )
        self.CreateOrderSubscription = channel.unary_stream(
                '/connamara.ep3.v1beta1.OrderEntryAPI/CreateOrderSubscription',
                request_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionRequest.SerializeToString,
                response_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionResponse.FromString,
                )


class OrderEntryAPIServicer(object):
    """OrderEntryAPI is the API Surface for connected clients to send and modify orders.
    """

    def InsertOrder(self, request, context):
        """InsertOrder inserts orders into the exchange and returns the exchange assigned order ID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InsertOrderCross(self, request, context):
        """InsertOrderCross creates a new order cross and returns the exchange assigned order IDs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InsertOrderList(self, request, context):
        """InsertOrderList inserts a list of orders into the exchange and returns the exchange assigned order IDs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelOrder(self, request, context):
        """CancelOrder requests cancellation of a working order.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelOrderList(self, request, context):
        """CancelOrderList requests cancellation of a list of working orders.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelReplaceOrder(self, request, context):
        """CancelReplaceOrder requests modification of a working order.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelReplaceOrderList(self, request, context):
        """CancelReplaceOrderList requests modification of a list of working orders.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateOrderSubscription(self, request, context):
        """CreateOrderSubscription creates a subscription for working orders and updates.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderEntryAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InsertOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.InsertOrder,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderResponse.SerializeToString,
            ),
            'InsertOrderCross': grpc.unary_unary_rpc_method_handler(
                    servicer.InsertOrderCross,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossResponse.SerializeToString,
            ),
            'InsertOrderList': grpc.unary_unary_rpc_method_handler(
                    servicer.InsertOrderList,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListResponse.SerializeToString,
            ),
            'CancelOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelOrder,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderResponse.SerializeToString,
            ),
            'CancelOrderList': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelOrderList,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListResponse.SerializeToString,
            ),
            'CancelReplaceOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelReplaceOrder,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderResponse.SerializeToString,
            ),
            'CancelReplaceOrderList': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelReplaceOrderList,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListResponse.SerializeToString,
            ),
            'CreateOrderSubscription': grpc.unary_stream_rpc_method_handler(
                    servicer.CreateOrderSubscription,
                    request_deserializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionRequest.FromString,
                    response_serializer=connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'connamara.ep3.v1beta1.OrderEntryAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderEntryAPI(object):
    """OrderEntryAPI is the API Surface for connected clients to send and modify orders.
    """

    @staticmethod
    def InsertOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrder',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InsertOrderCross(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrderCross',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderCrossResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InsertOrderList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/InsertOrderList',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.InsertOrderListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/CancelOrder',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelOrderList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/CancelOrderList',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelOrderListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelReplaceOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/CancelReplaceOrder',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelReplaceOrderList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/CancelReplaceOrderList',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CancelReplaceOrderListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateOrderSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/connamara.ep3.v1beta1.OrderEntryAPI/CreateOrderSubscription',
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionRequest.SerializeToString,
            connamara_dot_ep3_dot_v1beta1_dot_order__entry__api__pb2.CreateOrderSubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)