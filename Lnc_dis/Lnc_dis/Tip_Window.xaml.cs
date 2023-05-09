using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Lnc_dis
{
    /// <summary>
    /// Tip_Window.xaml 的交互逻辑
    /// </summary>
    public partial class Tip_Window : Window
    {
        public Tip_Window()
        {
            InitializeComponent();
        }

        private void cancel_button_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void ok_button_Click(object sender, RoutedEventArgs e)
        {
            string jsonString = "start";
            StaticClass.clientsocket.Send(UTF8Encoding.UTF8.GetBytes(jsonString));
            int receiveLength = StaticClass.clientsocket.Receive(StaticClass.reult);
            string res = UTF8Encoding.UTF8.GetString(StaticClass.reult, 0, receiveLength);
            Console.WriteLine(res);
        }
    }
}
