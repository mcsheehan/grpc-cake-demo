from collections import defaultdict
from concurrent import futures
import logging

import grpc

import cake_pb2
import cake_pb2_grpc


class Cake:
    def __init__(self):
        self.cake_list = defaultdict(lambda: 1)
        self.initialise_cake_list_with_extra_cake()

    def add_name_to_cake_list(self, name):
        self.cake_list[name] = 1

    def get_amount_of_cake_for_person(self, name):
        if name not in self.cake_list:
            self.add_name_to_cake_list(name)

        return self.cake_list[name]

    def set_amount_of_cake(self, name, amount):
        if name not in self.cake_list:
            self.add_name_to_cake_list(name)

        self.cake_list[name] = amount

    def initialise_cake_list_with_extra_cake(self):
        self.cake_list = {"john": 2,
                          "nelson": 2,
                          "helen": 2,
                          "aengus": 2,
                          "duyshant": 2}


class Greeter(cake_pb2_grpc.CakeDistributerServicer):

    def __init__(self):
        self.cake = Cake()

    def ProvideCake(self, request, context):
        return super().ProvideCake(request, context)

    def HowMuchCake(self, request, context):
        caller = request.name

        pieces_of_cake = self.cake.get_amount_of_cake_for_person(caller)

        message = f"Wow you get {pieces_of_cake} pieces of cake"

        response = cake_pb2.AmountOfCakeMessage(numberOfCakes=pieces_of_cake,
                                                message=message,
                                                numberOfPiecesOfCakeYouOweMark=10)

        return response

    def StealAllTheCake(self, request, context):
        cake_to_steal = self.cake.get_amount_of_cake_for_person(request.stealFromName)
        current_cake = self.cake.get_amount_of_cake_for_person(request.stealToName)

        self.cake.set_amount_of_cake(request.stealFromName, 0)
        self.cake.set_amount_of_cake(request.stealToName, current_cake + cake_to_steal)

        return  cake_pb2.CakeStolenConfirmation()

    def WhoHasTheMostCake(self, request, context):
        max_value = 0
        most_cake = ""
        for key, value in self.cake.cake_list.items():
            if value > max_value:
                most_cake = key
                max_value = value

        response = cake_pb2.MostCakeMessage(name=most_cake,
                                            amountOfCake=max_value)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cake_pb2_grpc.add_CakeDistributerServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    cake = Cake()
    logging.basicConfig()
    serve()
