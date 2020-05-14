# -*- coding: gbk -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : BaseFrame.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-05-10
#   desc     : basic wxPython Frame
# ==========================================================================
import wx


class BaseFrame(wx.Frame):
    """
    A Frame that says Hello World
    """
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(BaseFrame, self).__init__(*args, **kw)
        self.icon = self.init_icon()
        self.init_basic_panel()

        # create a menu bar
        self.menu_bar = None
        self.make_menu_bar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("这是一个测试用的Python GUI程序")

    def init_icon(self):
        icon = wx.Icon('res/cd_16x16.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(icon)
        return icon

    def init_basic_panel(self):
        # create a panel in the frame
        panel = wx.Panel(self)

        # put some text with a larger bold font on it
        default_label = "CDPlayer's Base Frame"
        st = wx.StaticText(
            parent=panel,
            label=default_label)
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
        panel.SetSizer(sizer)

    def make_file_menu(self):
        # Make a file menu with Hello and Exit items
        file_menu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        hello_item = file_menu.Append(
            -1, "&测试",
            "测试菜单的弹出消息框效果")
        file_menu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's label
        exit_item = file_menu.Append(id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        return file_menu

    def make_help_menu(self):
        help_menu = wx.Menu()
        about_item = help_menu.Append(id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        return help_menu

    def make_menu_bar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """
        self.menu_bar = wx.MenuBar()
        file_menu = self.make_file_menu()
        help_menu = self.make_help_menu()

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        self.menu_bar.Append(menu=file_menu, title="&文件")
        self.menu_bar.Append(menu=help_menu, title="&帮助")

        # Give the menu bar to the frame
        self.SetMenuBar(self.menu_bar)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)
        app.ExitMainLoop()

    def on_hello(self, event):
        """Say hello to the user."""
        wx.MessageBox("测试成功，弹窗展示MessageBox")

    def on_about(self, event):
        """Display an About Dialog"""
        wx.MessageBox("这是一个尝试用 wxPython 来实现 GUI 的测试程序",
                      "Copyright by okcd00.",
                      wx.OK | wx.ICON_INFORMATION)

    def start(self):
        self.Show()
        app.MainLoop()


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = BaseFrame(None, title='CDPlayer\'s Hello-world')
    frm.start()
