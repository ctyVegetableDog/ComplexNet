using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace lnc_third_layer
{
    class Program
    {
        static Socket SocketWatch;
        public static SQL sql = new SQL();
        static void Main(string[] args)
        {
            SocketWatch = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint endPoint = new IPEndPoint(StaticClass.ip, StaticClass.port);
            SocketWatch.Bind(endPoint);
            SocketWatch.Listen(10);
            Console.WriteLine("建立连接");
            Thread threadWatching = new Thread(watching);
            threadWatching.IsBackground = true;
            threadWatching.Start();
            Console.ReadKey();

        }
        static void watching()
        {
            Socket socket = null;
            while (true)
            {
                try
                {
                    socket = SocketWatch.Accept();
                }
                catch (Exception ex)
                {
                    break;
                }
                Console.WriteLine("成功与{0}客户端建立联系", socket.RemoteEndPoint.ToString());
                ParameterizedThreadStart pts = new ParameterizedThreadStart(recv);
                Thread thread = new Thread(pts);
                thread.IsBackground = true;
                thread.Start(socket);
            }

        }
        static void recv(object socketClientPara)
        {
            Socket socketSever = socketClientPara as Socket;
            while (true)
            {
                byte[] recmsg = new byte[1024 * 1024];
                try
                {
                    int lenth = socketSever.Receive(recmsg);
                    string jsonString = UTF8Encoding.UTF8.GetString(recmsg, 0, lenth);
                    string stringSendToSecondLayer = "";
                    try
                    {
                        float[][] messageFromSecondLayer = JsonConvert.DeserializeObject<float[][]>(jsonString);
                        //更新数据库
                        Console.WriteLine("开始更新数据库");
                        for (int i = 0; i < messageFromSecondLayer.Length; i++)
                        {
                            for (int j = 0; j < messageFromSecondLayer[i].Length; j++)
                            {
                                string q = String.Format("update dis_lnc set link={0} where lnc_id={1} and dis_id={2}", messageFromSecondLayer[i][j], i, j);
                                sql.Updata(q);
                            }
                        }
                        stringSendToSecondLayer = "更新完成";
                    }
                    catch
                    {
                        stringSendToSecondLayer = "更新失败";
                    }
                    socketSever.Send(UTF8Encoding.UTF8.GetBytes(stringSendToSecondLayer));
                    Console.WriteLine("Send to SecondLayer:" + stringSendToSecondLayer);

                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());
                    Console.WriteLine("客互端" + "已经中断连接");
                    socketSever.Close();
                    break;
                }
            }
        }
    }
}
