using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lnc_dis
{
    public class Disease
    {
        public int id { get; set; }
        public string doid { get; set; }
        public string name { get; set; }
        public Disease(int id, string doid, string name)
        {
            this.id = id;
            this.doid = doid;
            this.name = name;
        }
    }
}
