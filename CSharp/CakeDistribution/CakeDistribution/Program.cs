﻿using System;
using Grpc.Core;

using Cake;

namespace CakeDistribution
{
    internal class Program
    {
        private const String StackBadgerServerAddress = "cake.stackbadger.net:50051";
        private const String LocalHostAddress = "localhost:50051";
        
        public static void Main(string[] args)
        { 
            String user = "john";
            
            Channel channel = new Channel(StackBadgerServerAddress, ChannelCredentials.Insecure);
            var greeter = new CakeDistributer.CakeDistributerClient(channel);

            NameMessage message = new NameMessage {Name = user};

            var reply = greeter.SayHello(message);
            Console.WriteLine(reply.Message);

            channel.ShutdownAsync().Wait();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}