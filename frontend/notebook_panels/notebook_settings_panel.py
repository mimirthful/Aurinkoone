import wx
from frontend.settings import WeatherSettingsPanel, BusStopSettingsPanel, InfoSettingsPanel


class NotebookSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        weather_setting_panel = wx.Panel(self)
        weather_setting_sizer = wx.BoxSizer()
        weather_setting_panel.SetSizer(weather_setting_sizer)
        weather_settings = WeatherSettingsPanel(weather_setting_panel)
        weather_setting_sizer.Add(weather_settings, 1)

        bus_setting_panel = wx.Panel(self)
        bus_setting_sizer = wx.BoxSizer()
        bus_setting_panel.SetSizer(bus_setting_sizer)
        bus_settings = BusStopSettingsPanel(bus_setting_panel)
        bus_setting_sizer.Add(bus_settings, 1)

        info_setting_panel = wx.Panel(self)
        info_setting_sizer = wx.BoxSizer()
        info_setting_panel.SetSizer(info_setting_sizer)
        info = InfoSettingsPanel(info_setting_panel)
        info_setting_sizer.Add(info, 1)

        sizer.Add(weather_setting_panel,
                  flag=wx.ALL | wx.EXPAND, border=5)
        sizer.Add(bus_setting_panel,  flag=wx.ALL | wx.EXPAND, border=5)
        sizer.Add(info_setting_panel,  flag=wx.EXPAND |
                  wx.ALL, border=5)
