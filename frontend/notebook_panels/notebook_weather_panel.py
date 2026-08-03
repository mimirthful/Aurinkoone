import wx
from frontend.forecast import HourlyForecastPanel, WeekForecastPanel
from frontend.todaystats import MainTempPanel, StatPanel, CurrentInfo


class NotebookWeatherPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        # Lower and half sizers
        self.maintemp_panel = MainTempPanel(self)
        self.current_info = CurrentInfo(self)

        inner_sizer = wx.GridBagSizer(0, 10)

        sizer.Add(inner_sizer, proportion=1,
                  flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)

        self.hourly_forecast_panel = HourlyForecastPanel(self)
        self.week_forecast_panel = WeekForecastPanel(self)
        self.stat_panel = StatPanel(self)
        inner_sizer.Add(self.current_info, pos=(0, 0))
        inner_sizer.Add(self.maintemp_panel, pos=(0, 1))
        inner_sizer.Add(
            self.stat_panel, pos=(1, 0), span=(2, 1), flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)

        inner_sizer.Add(
            self.hourly_forecast_panel, (3, 0), flag=wx.EXPAND | wx.ALL, border=5)

        inner_sizer.Add(
            self.week_forecast_panel, (1, 1), (3, 2), flag=wx.EXPAND | wx.ALL, border=5)
