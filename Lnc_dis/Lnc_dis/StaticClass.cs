using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Lnc_dis
{
    public static class StaticClass
    {
        public static Socket clientsocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);//socket
        public static IPAddress ip = IPAddress.Parse("192.168.1.101");//ip
        public static byte[] reult = new byte[1024 * 1024];//缓存
        public static int port = 8885;//端口
    }
}
