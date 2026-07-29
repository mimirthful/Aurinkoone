import wx


class BusStopInfoHeader(wx.Panel):
    def __init__(self, parent: wx.Window, name, code):
        super().__init__(parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        text = wx.StaticText(self, wx.ID_ANY, label=f'{name} ({code})')
        sizer.Add(text, 1, flag=wx.EXPAND | wx.ALL,  border=10)
