using System;
using System.Collections.Generic;
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
using System.Windows.Shapes;

namespace Lnc_dis
{
    /// <summary>
    /// Welcome_Window.xaml 的交互逻辑
    /// </summary>
    public partial class Welcome_Window : Window
    {
        public Welcome_Window()
        {
            InitializeComponent();
        }

        private void okbutton_Click(object sender, RoutedEventArgs e)
        {
            var dialong = new Main_Window();
            this.Close();
            dialong.ShowDialog();
        }

        private void quit_button_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}
