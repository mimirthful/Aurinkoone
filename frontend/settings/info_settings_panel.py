import wx
from wx import adv


class InfoSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.authorpanel = self.InfoTextPanel(
            self, 'Tampere weather and bus stop app by ', "Alex Lankio [Mimirthful]", 'https://github.com/mimirthful')

        self.weatherpanel = self.InfoTextPanel(
            self, 'Yr weather symbols © 2015 by Yr/NRK. Weather Data from MET Norway ', "yr.no", "https://www.yr.no/")
        # self.icon_text = wx.ico
        self.icon_info = self.InfoTextPanel(
            self, "UV, Rain change, and Wind speed, Menu and placeholder image Icons by ", "Icons8", "https://icons8.com")

        sizer.Add(self.authorpanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=5)
        sizer.Add(self.weatherpanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=5)
        sizer.Add(self.icon_info, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    class InfoTextPanel(wx.Panel):
        def __init__(self, parent, text, link_label, link_url):
            super().__init__(parent)
            self.sizer = wx.BoxSizer()
            self.SetSizer(self.sizer)
            self.info = wx.StaticText(
                self, label=text)
            self.link = adv.HyperlinkCtrl(
                self, label=link_label, url=link_url)
            self.sizer.Add(self.info, 0)
            self.sizer.Add(self.link, 0)
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
