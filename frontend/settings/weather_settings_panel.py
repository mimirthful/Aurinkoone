import wx
from .change_weather_area import ChangeWeatherAreaWidget


class WeatherSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        title = wx.StaticText(self, label="- Weather -")
        sizer.Add(title, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=5)
        change = ChangeWeatherAreaWidget(self)
        sizer.Add(change, 1, flag=wx.ALL, border=5)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)


# BACKGROUND

    def OnPaint(self, event):

        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)

        gc.SetPen(wx.Pen(wx.Colour("#4530BF59"), 1))
        gc.SetBrush(wx.Brush(wx.Colour("#4530BF59")))
        size = self.GetSize()
        x = 0
        y = 0
        w = size.width
        h = size.height

        gc.DrawRoundedRectangle(x, y, w, h, 5)

    def OnEraseBackground(self, event):
        pass
