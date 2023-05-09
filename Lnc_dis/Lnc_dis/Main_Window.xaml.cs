using System;
using System.Collections.Generic;
using System.Data.SqlClient;
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
    /// Main_Window.xaml 的交互逻辑
    /// </summary>
    public partial class Main_Window : Window
    {
        public Main_Window()
        {
            InitializeComponent();
        }

        private void accountButton_Checked(object sender, RoutedEventArgs e)
        {
            SQL sql = new SQL();
            string query = String.Format("select * from disease_info");
            SqlDataReader DR = sql.query(query);
            List<Disease> dis_list = new List<Disease>();
            while(DR.Read())
            {
                Disease dis = new Disease(Convert.ToInt32(DR[0]), Convert.ToString(DR[1]), Convert.ToString(DR[2]));
                dis_list.Add(dis);
            }
            Lnc_Dis_Page now_page = new Lnc_Dis_Page();
            now_page.ass_dataGrid.ItemsSource = dis_list;
            frame1.Content = now_page;
        }

        private void startButton_Checked(object sender, RoutedEventArgs e)
        {
            try
            {
                if(!StaticClass.clientsocket.Connected)
                    StaticClass.clientsocket.Connect(new IPEndPoint(StaticClass.ip, StaticClass.port));
            }
            catch (Exception ex)
            {
                MessageBox.Show("服务器连接失败");
                return;
            }
            var dialong = new Tip_Window();
            startButton.IsChecked = false;
            dialong.ShowDialog();
        }

        private void skipButton_Checked(object sender, RoutedEventArgs e)
        {
            var dialong = new Welcome_Window();
            this.Close();
            dialong.ShowDialog();
        }
    }
}
