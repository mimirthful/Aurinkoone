from .week_forecast_day_widget import WeekForecastDayWidget
from .week_forecast_title_widget import WeekForecastTitleWidget
import wx
from pubsub import pub


class WeekForecastPanel(wx.Panel):
    def __init__(self, parent, ):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.set_widget_list()
        # Background drawing events
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def set_widget_list(self):
        # List of the widgets
        weather_forecast = self.days_weather_forecast()
        # Push items on the list to the sizer
        for item in weather_forecast:
            self.sizer.Add(
                item, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.Layout()

    def days_weather_forecast(self) -> list[WeekForecastDayWidget]:
        '''Returns a list of WeekForecastDayWidgets'''
        target_days = 7
        widget_list = []
        # Adding title to the list
        title = WeekForecastTitleWidget(self)
        widget_list.append(title)

        # Widgets
        i = 0
        while i < target_days:
            widget = WeekForecastDayWidget(self, i)
            topic_name = f"daily_forecast.{i}"
            pub.subscribe(widget.update_content, topic_name)
            widget_list.append(widget)
            i = i + 1
        return widget_list


# --- BACKGROUND ---

    def OnPaint(self, event):

        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)

        gc.SetPen(wx.Pen(wx.Colour("#4530BF7A"), 1))
        gc.SetBrush(wx.Brush(wx.Colour("#4530BF7A")))
        size = self.GetSize()
        x = 0
        y = 0
        w = size.width
        h = size.height

        gc.DrawRoundedRectangle(x, y, w, h, 5)
        y += 100

    def OnEraseBackground(self, event):
        pass
