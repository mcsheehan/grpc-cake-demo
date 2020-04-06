using System;
using Grpc.Core;

using Cake;

namespace CakeDistribution
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            // Channel channel = new Channel("cake.stackbadger.net:50051", ChannelCredentials.Insecure);
            Channel channel;
            try
            {
                channel = new Channel("localhost:50051", ChannelCredentials.Insecure);
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                return;
            }

            var greeter = new CakeDistributer.CakeDistributerClient(channel);
            String user = "john";

            NameMessage message = new NameMessage {Name = user};
            var a = new NameMessage();
            a.Name = "badgers";

            var reply = greeter.SayHello(message);
            // var reply = greeter.SayHello(a);
                
            Console.WriteLine("Greeting: " + reply.Message);

            channel.ShutdownAsync().Wait();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}