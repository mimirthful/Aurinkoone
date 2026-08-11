import wx
from frontend.settings import WeatherSettingsPanel, BusStopSettingsPanel, InfoSettingsPanel, MessagePanel


class NotebookSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        upper_panel = wx.Panel(self)
        upper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        upper_panel.SetSizer(upper_sizer)

        first_row_panel = wx.Panel(upper_panel)
        first_row_sizer = wx.BoxSizer(wx.VERTICAL)
        first_row_panel.SetSizer(first_row_sizer)

        weather_setting_panel = wx.Panel(first_row_panel)
        weather_setting_sizer = wx.BoxSizer()
        weather_setting_panel.SetSizer(weather_setting_sizer)
        weather_settings = WeatherSettingsPanel(weather_setting_panel)
        weather_setting_sizer.Add(weather_settings)

        message_panel = wx.Panel(first_row_panel)
        message_sizer = wx.BoxSizer()
        message_panel.SetSizer(message_sizer)
        message_inner = MessagePanel(message_panel)
        message_sizer.Add(message_inner)

        bus_setting_panel = wx.Panel(upper_panel)
        bus_setting_sizer = wx.BoxSizer()
        bus_setting_panel.SetSizer(bus_setting_sizer)
        bus_settings = BusStopSettingsPanel(bus_setting_panel)
        bus_setting_sizer.Add(bus_settings)

        first_row_sizer.Add(weather_setting_panel)
        first_row_sizer.Add(message_panel)
        upper_sizer.Add(first_row_panel,
                        flag=wx.ALL | wx.EXPAND, border=5)
        upper_sizer.Add(bus_setting_panel,  flag=wx.ALL | wx.EXPAND, border=5)

        lower_panel = wx.Panel(self)
        lower_sizer = wx.BoxSizer(wx.VERTICAL)
        lower_panel.SetSizer(lower_sizer)

        info_setting_panel = wx.Panel(lower_panel)
        info_setting_sizer = wx.BoxSizer()
        info_setting_panel.SetSizer(info_setting_sizer)
        info = InfoSettingsPanel(info_setting_panel)
        info_setting_sizer.Add(info)
        lower_sizer.Add(info_setting_panel,  flag=wx.EXPAND |
                        wx.ALL, border=5)

        main_sizer.Add(upper_panel, 1, wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.Add(lower_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
