from .stat_widget import StatWidget
from pubsub import pub
from frontend.ui_bitmaps import UiBitmaps
import wx


class StatPanel(wx.Panel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bitmaps = UiBitmaps()

        self.SetSizer(self.sizer)
        self.add_widgets()

    def add_widgets(self):
        self.sizer.Clear(delete_windows=True)

        # UV
        uv_widget = StatWidget(self, self.bitmaps.uv, "UV")
        pub.subscribe(uv_widget.update_content, "uv")
        # Rain change
        rain_widget = StatWidget(
            self, self.bitmaps.umbrella, "Rain change")
        pub.subscribe(rain_widget.update_content, "rain")
        # wind speed
        wind_widget = StatWidget(
            self, self.bitmaps.wind, "Wind speed")
        pub.subscribe(wind_widget.update_content, "wind")

        self.sizer.AddMany([(uv_widget, 1, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5),
                           (rain_widget, 1, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5),
                           (wind_widget, 1, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)])

        self.Layout()
