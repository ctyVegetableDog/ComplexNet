   M S B A M L   `   `   `  ����B  >Lnc_dis, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null!clr-namespace:Lnc_disLnc_dis  5   	       Lnc_dis.Main_Window   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   'localclr-namespace:Lnc_dis     5   	     � Title$  Main_Window��5   	    � WindowState$ Normal=�6    � 
ResizeMode$ NoResize=�62   $��727.79��6H   $��1331.491��6X    � 	Resources 5	       	  FIcon �� 
TargetType �� Property �� Value��%V  &	        �� 5   
   " ��6   .�5      ��  � ��$7 1/K.Framework.Controls;component/Resources/#SF2015)�6+   6g   �� 5       � ��
 �   �6+   �� 5       �@��TextAlignment$ Center=�6.   �� 5       � ��$ Center=�64   �� 5       � ��$ Center=�62   �� 5       � ��$ 20(�6)   5      5      .��5      � $	��704��6   $	��Top=�6    J� RenderTransformOrigin$ -0.567,-1.018&�61   $
��Left=�6X   $
��1321��6s   $��0,0,0,-5q�6�   
����� �.+�5   
   	� -   5         	�Name$ accountButton��5      $��RadioButton��6-   $
��Left=�6C   $��	299,5,0,0q�6^   $	��Top=�6q   $	��100��6�   $	��100��6�   ��5      �� 5      " 	�6   .�5       ��  � �� 5!      �� 5"      	 �� 
TargetType"	 	�6.   .R�5#   "   �� 
 ��Name$
 btnbg��6(   $��Resources/account.png��67    �� Triggers 5$   "   P� 5%   &    P� Property �@J�IsMouseOver P� Value . . �5&   *   ��  �� 
TargetName$ btnbg��6h    � ��$! Resources/accountChoose.png��6D   6h   5'   '   P� 5(   &    �@d�	IsChecked$
 TrueY�6C   . �5)   *   �� $ btnbg��6h    � ��$! Resources/accountChoose.png��6D   6h   5*   '   P� 5+   &    � {� .  . �5,   *   �� $ btnbg��6e    � ��$ Resources/accountcant.png��6C   6e   5-   '   5/      51      52      54      	� 55   
   -   5        $ 
skipButton��55      $��RadioButton��6*   $
��Left=�6@   $��
865,10,0,0q�6[   $	��Top=�6o   $	��100��6�   $	��100��6�   ��56      �� 57      " 	�6   .�58      ��  � �� 59      �� 5:      "	 	�6.   .R�5;   "   �� $
 btnbg��6(   $��Resources/skip.png��67    5<   "   P� 5=   &    �@J�IsMouseOver . . �5>   *   �� $ btnbg��6e    � ��$ Resources/skipChoose.png��6D   6e   5?   '   P� 5@   &    �@d�	IsChecked$
 TrueY�6C   . �5A   *   �� $ btnbg��6e    � ��$ Resources/skipChoose.png��6D   6e   5B   '   5D      5F      5G      5I       � 5J   
   -   5          �Name$ frame1��5J      $�� ��6    $
��Left=�6+   $	��514��6F   $��
29,164,0,0q�6S   $	��Top=�6g   $
��1260��6     � NavigationUIVisibility$ Hidden=�6�   
�������6�   �� 5K   
   -   5         ��Name$ accountlabel��5K      $��LncRNA-疾病关联预测��6&   $
��Left=�6>   $��247,110,0,0q�6Y   $	��Top=�6n   $��Arial)�6�   $
��Bold"�6�   $��20(�6�   �� 5L   
   -   5        $ 	skiplabel��5L      $��返回��6#   $
��Left=�60   $��889,120,0,0q�6K   $	��Top=�6`   $��Arial)�6x   $
��Bold"�6�   $��20(�6�   �� 5M   
   -   5        $
 image��5M      $
��Left=�6   $	��133��6:   $��1079,10,0,0q�6G   $	��Top=�6\   $	��133��6t   $��Resources/精灵球.png��6�   �� 5N   
   -   5        $
 image_Copy1��5N      $
��Left=�6%   $	��133��6@   $��
503,10,0,0q�6M   $	��Top=�6a   $	��133��6y   $��Resources/掌印.png��6�   �� 5O   
   -   5        $
 image_Copy2��5O      $
��Left=�6%   $	��133��6@   $��
689,10,0,0q�6M   $	��Top=�6a   $	��133��6y   $��Resources/掌印.png��6�   	� 5P   
   -	   5        $ startButton��5P      $��RadioButton��6+   $
��Left=�6A   $��
113,10,0,0q�6\   $	��Top=�6p   $	��100��6�   $	��100��6�   ��5Q      �� 5R      " 	�6   .�5S      ��  � �� 5T      �� 5U      "	 	�6.   .R�5V   "   �� $
 btnbg��6(   $��Resources/开始.png��67    5W   "   P� 5X   &    �@J�IsMouseOver . . �5Y   *   �� $ btnbg��6^    � ��$ Resources/开始1.png��6D   6^   5Z   '   P� 5[   &    �@d�	IsChecked$
 TrueY�6C   . �5\   *   �� $ btnbg��6^    � ��$ Resources/开始1.png��6D   6^   5]   '   P� 5^   &    � {� .  . �5_   *   �� $ btnbg��6\    � ��$ Resources/开始.png��6C   6\   5`   '   5b      5d      5e      5g      �� 5h   
   -
   5        $ accountlabel_Copy��5h      $��开始预测��6+   $
��Left=�6:   $��113,115,0,0q�6U   $	��Top=�6j   $��Arial)�6�   $
��Bold"�6�   $��20(�6�   5i      5j      