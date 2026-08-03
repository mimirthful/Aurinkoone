import wx
from .change_weather_area import ChangeWeatherAreaWidget


class WeatherSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.StaticBoxSizer(wx.StaticBox(
            self,  label=" Weather settings"), wx.VERTICAL)
        self.SetSizer(sizer)
        change = ChangeWeatherAreaWidget(self)
        sizer.Add(change, 1, flag=wx.ALL, border=5)
