from .hourly_forecast_hour_widget import HourlyForecastHourWidget
import wx
import wx.lib.scrolledpanel as scrolled
from pubsub import pub


class HourlyForecastPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.StaticBoxSizer(wx.StaticBox(
            self), wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.scroll_panel = scrolled.ScrolledPanel(
            self.sizer.GetStaticBox(), size=wx.Size(410, -1))
        self.scroll_panel.SetupScrolling()

        self.sizer.Add(self.scroll_panel, 1, wx.EXPAND)
        self.child_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.scroll_panel.SetSizer(self.child_sizer)
        self.add_widgets()
        pub.subscribe(self.scroll_panel.Layout, "hourlyforecastpanel_updated")

    def today_weather_forecast(self) -> list:
        hours_list = ["now", "1_hours_from_now", "2_hours_from_now",
                      "3_hours_from_now", "4_hours_from_now", "5_hours_from_now",
                      "6_hours_from_now", "7_hours_from_now", "8_hours_from_now",
                      "9_hours_from_now", "10_hours_from_now", "11_hours_from_now"]
        widget_list = []
        for item in hours_list:
            widget = HourlyForecastHourWidget(
                self.scroll_panel)
            topic_name = f"hourly_forecast.{item}"
            pub.subscribe(widget.update_content, topic_name)
            widget_list.append(widget)

        return widget_list

    def add_widgets(self):
        self.weather_forecast = self.today_weather_forecast()
        for item in self.weather_forecast:
            self.child_sizer.Add(
                item, proportion=0, flag=wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, border=5)
        self.scroll_panel.Layout()
        self.scroll_panel.SetupScrolling(scroll_x=True, scroll_y=False)
