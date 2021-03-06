﻿using System;
using Cake;
using Grpc.Core;

namespace CakeDistributionDotNetCore
{
        internal class HowManyCakesDoIGetConsoleApp
        {
            private const String StackBadgerServerAddress = "cake.stackbadger.net:50051";
            private const String LocalHostAddress = "localhost:50051";
         
            public static void Main(string[] args)
            { 
                String user = "john";
            
                Channel channel = new Channel(StackBadgerServerAddress, ChannelCredentials.Insecure);
                var cakeDistributer = new CakeDistributer.CakeDistributerClient(channel);

                NameMessage message = new NameMessage {Name = user};

                var reply = cakeDistributer.HowMuchCake(message);
                Console.WriteLine(reply.Message);
                // Console.WriteLine(reply.NumberOfPiecesOfCakeYouOweMark);
                channel.ShutdownAsync().Wait();
                Console.WriteLine("Press any key to exit...");
                Console.ReadKey();
            }
    }
}