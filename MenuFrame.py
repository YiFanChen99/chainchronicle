# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import SubMenuFrame
import Utilities

GROUP_STATIC_INFO = 'Static Info'
GROUP_ACCOUNT_JP = 'Fuji Account'
GROUP_ACCOUNT_TW = 'Yama Account'
GROUPS = [GROUP_STATIC_INFO, GROUP_ACCOUNT_JP, GROUP_ACCOUNT_TW]


class MenuFrame(Frame):
    def __init__(self, master, height, **kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

        radiobuttons = Utilities.RadiobuttonController(self, height=height, button_type=1)
        for group_index in range(len(GROUPS)):
            def selecting_group(obj=self, my_index=group_index):
                obj.selecting_group(my_index)

            radiobuttons.create_button(145 + 165 * group_index, -1, GROUPS[group_index],
                                       selecting_group, width=14)

            # 預設選擇第一個
            if group_index == 0:
                radiobuttons.selecting_button(0, selecting_group)

    # 幫 master 進行切換
    def selecting_group(self, index):
        self.master.update_sub_menu_frame(self.create_sub_menu_frame(index))

    def create_sub_menu_frame(self, index):
        height = 28
        if GROUPS[index] == GROUP_STATIC_INFO:
            return SubMenuFrame.StaticGroupFrame(self.master, height=height)
        elif GROUPS[index] == GROUP_ACCOUNT_JP:
            return SubMenuFrame.AccountGroupFrame(self.master, height=height, db_suffix='JP')
        elif GROUPS[index] == GROUP_ACCOUNT_TW:
            return SubMenuFrame.AccountGroupFrame(self.master, height=height, db_suffix='TW')
        else:
            raise Exception("Wrong group selected!")