using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Lnc_dis
{
    /// <summary>
    /// Lnc_Dis_Page.xaml 的交互逻辑
    /// </summary>
    public partial class Lnc_Dis_Page : Page
    {
        private void ass_dataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

            var a = ass_dataGrid.SelectedItem;
            var dis = a as Disease;
            if (dis == null)
            {
                return;
            }
            SQL sql = new SQL();
            //获取已知记录
            string query = String.Format("select * from dis_lnc where dis_id = {0} and link=1", dis.id);
            SqlDataReader DR = sql.query(query);
            List<Lnc_dis_link> link_list = new List<Lnc_dis_link>();
            int rank = 1;
            while (DR.Read())
            {
                Lnc_dis_link lk = new Lnc_dis_link(rank, Convert.ToInt32(DR[0]), Convert.ToSingle(DR[2]));
                lk.show = lk.link.ToString();
                if (lk.link == 1)
                {
                    lk.show = "已知";
                    rank++;
                    link_list.Add(lk);
                }
            }
            //获取预测的前50条记录并排序
            string q2 = String.Format("select top 50 * from dis_lnc where dis_id = {0} order by link desc", dis.id);
            DR = sql.query(q2);
            while (DR.Read())
            {
                Lnc_dis_link lk = new Lnc_dis_link(rank, Convert.ToInt32(DR[0]), Convert.ToSingle(DR[2]));
                lk.show = lk.link.ToString();
                link_list.Add(lk);
                rank++;
            }

            dataGrid.ItemsSource = link_list;
            dataGrid.UpdateLayout();
            for (int i = 0; i < dataGrid.Items.Count; i++)//已知变色
            {
                Lnc_dis_link drv = dataGrid.Items[i] as Lnc_dis_link;
                float lk = Convert.ToSingle(drv.link);
                if (lk == 1)
                {
                    var row = dataGrid.ItemContainerGenerator.ContainerFromItem(dataGrid.Items[i]) as DataGridRow;
                    row.Background = new SolidColorBrush(Colors.Red);
                }
            }
        }
        private void dataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            dataGrid.UpdateLayout();
            for (int i = 0; i < dataGrid.Items.Count; i++)//已知变色
            {
                Lnc_dis_link drv = dataGrid.Items[i] as Lnc_dis_link;
                float lk = Convert.ToSingle(drv.link);
                if (lk == 1)
                {
                    var row = dataGrid.ItemContainerGenerator.ContainerFromItem(dataGrid.Items[i]) as DataGridRow;
                    row.Background = new SolidColorBrush(Colors.Red);
                }
            }
        }
        public Lnc_Dis_Page()
        {
            InitializeComponent();
        }

        private void find_textBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            SQL sql = new SQL();
            string content = find_textBox.Text;
            string q1 = String.Format("select * from disease_info where PATINDEX('{0}%',NAME)!= 0", content);
            SqlDataReader DR = sql.query(q1);
            List<Disease> dis_list = new List<Disease>();
            while (DR.Read())
            {
                Disease dis = new Disease(Convert.ToInt32(DR[0]), Convert.ToString(DR[1]), Convert.ToString(DR[2]));
                dis_list.Add(dis);
            }
            ass_dataGrid.ItemsSource = dis_list;
        }

        private void search_button_Click(object sender, RoutedEventArgs e)
        {
            SQL sql = new SQL();
            string content = find_textBox.Text;
            if(content == "")
            {
                return;
            }
            string[] kw = content.Split(' ');
            string q1 = "select * from disease_info where";
           for (int i = 0;i < kw.Length-1;i++)
            {
                q1 += String.Format(" PATINDEX('%{0}%',NAME)!= 0 and",kw[i]);
            }
            q1 += String.Format(" PATINDEX('%{0}%',NAME)!= 0", kw[kw.Length - 1]);
            SqlDataReader DR = sql.query(q1);
            List<Disease> dis_list = new List<Disease>();
            while (DR.Read())
            {
                Disease dis = new Disease(Convert.ToInt32(DR[0]), Convert.ToString(DR[1]), Convert.ToString(DR[2]));
                dis_list.Add(dis);
            }
            ass_dataGrid.ItemsSource = dis_list;
        }
    }
}
