   M S B A M L   `   `   `  ����B  >Lnc_dis, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null!clr-namespace:Lnc_disLnc_dis  5          Lnc_dis.Lnc_Dis_Page   5      \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5      R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5      Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5      @d2http://schemas.microsoft.com/expression/blend/2008     5      'localclr-namespace:Lnc_dis     5        N� Title$  Lnc_Dis_Page��5	      .��5      � .+�5   
   &   System.Windows.Controls.DataGrid  -   5          Name$ dataGrid��5      $
��Left=�6%   $	��Top=�6@   $	��514��6X   $	��795��6e      CanUserAddRows .     AutoGenerateColumns .     
IsReadOnly .    EnableRowVirtualization .     Columns 5      0  *System.Windows.Controls.DataGridTextColumn  5      ,  &System.Windows.Controls.DataGridColumn   Header$ 排名��6%      Width5  /System.Windows.Controls.DataGridLengthConverter$	 265 61   1  +System.Windows.Controls.DataGridBoundColumn	   Binding	 6=   �� 
 �� Path$

 rank� �� Mode$ TwoWay=� �� UpdateSourceTrigger$ PropertyChanged=�  5      $ LncRNA��6%   $	 265 65   	 6A   �� $
 lnc_id�$ TwoWay=�$ PropertyChanged=�  5      $ 关联得分��6%   $	 265 63   	 6?   �� $

 show�$ TwoWay=�$ PropertyChanged=�5        5   
   -   5        $ ass_dataGrid��5      $
��Left=�6)   $	��Top=�6D   $	��480��6\   $	��423��6i    .   .  $��837,35,0,-1q�6�    .  5        5      $ 编号��6%   $ 31 61   	 6<   �� $
 id�$ TwoWay=�$ PropertyChanged=�  5      $
 DOID��6%   $	 101 63   	 6?   �� $

 doid�$ TwoWay=�$ PropertyChanged=�  5      $ 	疾病名��6%   $	 311 62   	 6>   �� $

 name�$ TwoWay=�$ PropertyChanged=�5      �� 5   
   -   5         ��Name$ find_textBox��5      $
��Left=�6(   $��34��6C    �� TextWrapping$
 Wrap=�6O   $�� ��6c   $	��Top=�6k   $	��388��6�   $��	872,0,0,0q�6�   $��12(�6�   $��Center=�6�   6�   �� 5   
   -   5         ��Name$ search_button��5      $��Button��6(   $
��Left=�69   $	��Top=�6T   $��35��6l   $��35��6w    J� RenderTransformOrigin$ 1.173,0.478&�6�   $��	837,0,0,0q�6�   ��5      �� 5       �� 
TargetType" ��6   .�5      ��  �� Property � �� �� Value 5      �� 5        �� 
TargetType" ��6.   .R�5!   "   ��  ��Name$ btnbg��6(   $��Resources/search.png��67   $��35��6U   $��35��6a    �� Triggers 5"   "   P� 5#   &    P� Property �@J�IsMouseOver P� Value . . �5$   *   ��  �� 
TargetName$ btnbg��6g    � ��$  Resources/searchChoose.png��6D   6g   5%   '   5'      5)      5*      5,      � 5-   
   $
��Left=�6   $	��514��6*   $��	795,0,0,0q�67   $	��Top=�6J   $��42��6b   
����� �6m   5.      5/      