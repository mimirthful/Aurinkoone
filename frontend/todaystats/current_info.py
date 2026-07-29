import wx
from .current_date import CurrentDate
from .current_place import PlaceNamePanel


class CurrentInfo(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.place = PlaceNamePanel(self)
        self.date = CurrentDate(self)
        self.sizer.Add(self.place, 1, wx.EXPAND)
        self.sizer.Add(self.date, 1, wx.EXPAND)
