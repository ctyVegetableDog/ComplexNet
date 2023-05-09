using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lnc_dis
{
    public class Lnc_dis_link
    {
        public int rank { get; set; }
        public int lnc_id { get; set; }
        public float link { get; set; }
        public string show { get; set; }
        public Lnc_dis_link(int rank, int lnc_id, float link)
        {
            this.rank = rank;
            this.lnc_id = lnc_id;
            this.link = link;
        }
    }
}
