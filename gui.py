import wx
from frontend.notebook_panels import NotebookWeatherPanel, NotebookBusPanel, NotebookSettingsPanel
from frontend.ui_bitmaps import UiBitmaps
from pubsub import pub


class FrontFrame(wx.Frame):  # inherits wx.Frame
    def __init__(self, windowTitle):
        super().__init__(parent=None, title=windowTitle)
        # panel and sizer
        self.SetBackgroundColour(wx.Colour("#0E0E3A"))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        # Notebook
        self.notebook = wx.Listbook(panel, wx.ID_ANY)
        self.notebook.ListView.SetBackgroundColour(wx.Colour("#0E0E3A"))
        image_list = wx.ImageList(64, 64)
        self.notebook.AssignImageList(image_list)
        # Icons
        icons = UiBitmaps()

        # Page 1
        self.page_one = NotebookWeatherPanel(self.notebook)
        icon_one_bitmap = icons.weather
        icon_one_index = image_list.Add(
            icon_one_bitmap)
        # Page 2
        self.page_two = NotebookBusPanel(self.notebook)
        icon_two_bitmap = icons.bus_stop
        icon_two_index = image_list.Add(icon_two_bitmap)
        # Page 3
        page_three = NotebookSettingsPanel(self.notebook)
        icon_three_bitmap = icons.settings
        icon_three_index = image_list.Add(icon_three_bitmap)
        # Add pages
        self.notebook.AddPage(self.page_one, "Weather",
                              True, icon_one_index)
        self.notebook.AddPage(self.page_two, "Bus",
                              False, icon_two_index)
        self.notebook.AddPage(page_three, "Settings", False, icon_three_index)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, border=20)
        sizer.SetSizeHints(self)
        self.Centre(wx.BOTH)
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        wx.CallAfter(self.on_ui_ready)

    def on_ui_ready(self):
        pub.sendMessage("ui ready")

    def OnClose(self, event):
        pub.sendMessage("Closing")
        event.Skip()
