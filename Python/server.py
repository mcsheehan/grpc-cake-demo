from concurrent import futures
import logging

import grpc

import cake_pb2
import cake_pb2_grpc


class Greeter(cake_pb2_grpc.CakeDistributerServicer):

    people_who_get_extra_cake = {"john": 2,
                                 "nelson": 2,
                                 "helen": 2,
                                 "aengus": 2}

    def SayHello(self, request, context):
        caller = request.name

        pieces_of_cake = 1
        if caller in self.people_who_get_extra_cake:
            pieces_of_cake += self.people_who_get_extra_cake[caller]

        message = f"Wow you get {pieces_of_cake} pieces of cake"

        response = cake_pb2.AmountOfCakeMessage(numberOfCakes=pieces_of_cake, message=message)

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cake_pb2_grpc.add_CakeDistributerServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
