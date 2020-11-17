# -*- coding: utf-8 -*-
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
    app = wx.App()
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
        self.SetStatusText("This is a testing Python GUI program")

    def init_icon(self):
        icon = wx.Icon('res/cd_16x16.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(icon)
        return icon

    def init_basic_panel(self):
        # create a panel in the frame
        panel = wx.Panel(self, -1)

        # create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)

        # put some text with a larger bold font on it
        default_label = "CDPlayer's Base Frame"
        st = self.add_text(text=default_label, parent=panel)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))

        self.button = wx.Button(panel, -1, "Click", pos=(50, 80))
        self.Bind(wx.EVT_BUTTON, self.on_click, self.button)
        self.button.SetDefault()

        panel.SetSizer(sizer)

    def add_text(self, text, parent, point_size=5):
        # put some text with a larger bold font on it
        default_label = text
        st = wx.StaticText(
            parent=parent,
            label=default_label)
        font = st.GetFont()
        font.PointSize += point_size
        font = font.Bold()
        st.SetFont(font)
        return st

    def add_hello_item(self, file_menu):
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        hello_item = file_menu.Append(
            -1, "&测试",
            "Test MessageBox.")
        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)

    def add_exit_item(self, file_menu):
        # When using a stock ID we don't need to specify the menu item's label
        exit_item = file_menu.Append(id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

    def make_file_menu(self):
        # Make a file menu with Hello and Exit items
        file_menu = wx.Menu()
        self.add_hello_item(file_menu)
        file_menu.AppendSeparator()
        self.add_exit_item(file_menu)
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
        self.file_menu = self.make_file_menu()
        self.help_menu = self.make_help_menu()

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        self.menu_bar.Append(menu=self.file_menu, title="&File")
        self.menu_bar.Append(menu=self.help_menu, title="&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(self.menu_bar)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)
        self.app.ExitMainLoop()

    def on_hello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Success, This is the MessageBox")

    def on_click(self, event):
        self.button.SetLabel("Clicked")

    def on_about(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a testing GUI program by wxPython",
                      "Copyright by okcd00.",
                      wx.OK | wx.ICON_INFORMATION)

    def start(self):
        self.Show()
        self.app.MainLoop()


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    frm = BaseFrame(None, title='CDPlayer\'s Hello-world')
    frm.start()
