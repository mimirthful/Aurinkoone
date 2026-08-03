import wx


class BusStopTimesHeader(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, id=wx.ID_ANY)

        sizer = wx.GridSizer(4)
        self.SetSizer(sizer)

        bus_short_name = self.AddInfo("Line")
        bus_first_dep = self.AddInfo("Min")

        sizer.Add(bus_short_name, flag=wx.EXPAND)
        sizer.AddStretchSpacer(1)
        sizer.AddStretchSpacer(1)
        sizer.Add(bus_first_dep, flag=wx.EXPAND)

    def AddInfo(self, label):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        text = wx.StaticText(
            panel, wx.ID_ANY, label=label)
        text.SetForegroundColour(wx.Colour("white"))
        sizer.Add(text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        return panel
