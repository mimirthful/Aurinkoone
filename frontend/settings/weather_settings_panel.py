import wx
from .change_weather_area import ChangeWeatherAreaWidget


class WeatherSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(wx.Size(450, 250)))
        # Notebook panel's main sizer
        sizer = wx.StaticBoxSizer(wx.StaticBox(
            self,  label=" Weather settings"), wx.VERTICAL)
        self.SetSizer(sizer)
        change = ChangeWeatherAreaWidget(sizer.GetStaticBox())
        sizer.Add(change, 1, flag=wx.ALL, border=10)
