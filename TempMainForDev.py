# -*- coding: utf-8 -*-
from Tkinter import *
from MainFrameNew.MyCharacterFrame import *
from MainFrameNew.FriendFrame import FriendRecordFrame
from MainFrameNew.BaseFrame import TableModelAdvance, TableView
from ModelUtility.CommonState import *
from ModelUtility.Filter import FilterRuleManager



class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        print get_account()
        print get_db_suffix()
        set_account('Yama')
        print get_account()
        print get_db_suffix()
        set_account('Yama1')
        print get_account()
        print get_db_suffix()

    def the_print(self):
        print 1, 2, 5
        # popup.mainloop()
        # popup = BasicWindow1(self, width=30 , height=60)
        # popup.transient(self)
        # popup.focus()
        #
        # root.wait_window(popup)
        # popup = BasicWindow1(self, width=30 , height=60)
        # root.wait_window(popup)


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
