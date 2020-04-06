from __future__ import print_function
import logging

import grpc

import cake_pb2
import cake_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cake_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(cake_pb2.NameMessage(name='nelson'))

    print(response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
