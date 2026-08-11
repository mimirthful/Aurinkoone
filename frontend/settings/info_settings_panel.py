import wx
from wx import adv
from pubsub import pub


class InfoSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        pub.subscribe(self.update_latest_response_date,
                      "latest_response_date_changed")

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.firstpanel = self.InfoTextPanel(
            self, 'Aurinkoone • Tampere weather and bus stop app by Alex Lankio [Mimirthful]')
        self.authorpanel = self.InfoTextPanel(
            self, 'Licensed under MIT License © 2026 Alex Lankio • ', "GitHub", 'https://github.com/mimirthful')
        self.parter = self.InfoTextPanel(
            self, '♡')
        self.weathericonspanel = self.InfoTextPanel(
            self, f'Weather symbols © 2015 Yr/NRK, licensed under CC BY 4.0.')
        self.weatherpanel = self.InfoTextPanel(
            self, f'Weather Data from MET Norway • ', "yr.no", "https://developer.yr.no/doc/License/")
        self.buspanel = self.InfoTextPanel(
            self, f'Live transit data © Digitransit • ', "Digitransit", "https://digitransit.fi/en/developers/apis/7-terms-of-use/")
        self.icon_info = self.InfoTextPanel(
            self, "UV, Rain change, and Wind speed, Menu and placeholder image Icons by ", "Icons8", "https://icons8.com")

        sizer.Add(self.firstpanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.authorpanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.parter, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.weatherpanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.weathericonspanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.buspanel, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        sizer.Add(self.icon_info, 1, flag=wx.ALL |
                  wx.ALIGN_CENTER_HORIZONTAL, border=2)
        wx.CallAfter(pub.sendMessage, "get_latest_response_date")

    def update_latest_response_date(self, date):
        str = f'Live transit data © Digitransit - {date} • '
        self.buspanel.info.SetLabel(str)
        self.Layout()

    class InfoTextPanel(wx.Panel):
        def __init__(self, parent, text, link_label=None, link_url=None):
            super().__init__(parent)
            self.sizer = wx.BoxSizer()
            self.SetSizer(self.sizer)
            self.info = wx.StaticText(
                self, label=text)
            self.sizer.Add(self.info, 0)
            if link_label and link_url:
                self.link = adv.HyperlinkCtrl(
                    self, label=link_label, url=link_url)
                self.sizer.Add(self.link, 0)
