using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lnc_dis
{
    class MessageFormatWithSecondLayer
    {
        public int user_Operation;//用户操作
        public MessageFormatWithSecondLayer() { }
        public MessageFormatWithSecondLayer(int user_Operation)
        {
            this.user_Operation = user_Operation;
        }
    }
}
