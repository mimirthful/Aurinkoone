
from pubsub import pub
import wx


class PlaceNamePanel(wx.Panel):
    def __init__(self, parent) -> None:
        pub.subscribe(self.update_text, "district_name_available")
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_MODERN,
                       style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_SEMIBOLD)
        self.label = wx.StaticText(self, label="")

        self.label.SetFont(font)
        self.sizer.Add(self.label, 1, wx.EXPAND)

    def update_text(self, district):
        self.label.SetLabel(f'Tampere\n{district}')
        self.sizer.Layout()
        self.Refresh()
