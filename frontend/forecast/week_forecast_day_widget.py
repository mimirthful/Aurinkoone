import wx
from frontend import png_to_bitmap


class WeekForecastDayWidget(wx.Panel):
    def __init__(self, parent: wx.Window, id):
        super().__init__(parent, id=wx.ID_ANY)
        # weather widget
        self.id = id
        sizer = wx.GridSizer(0, 3, 0, 0)
        self.SetSizer(sizer)
        # info to be shown
        self.placeholder_img = wx.Image(40, 40, False).ConvertToBitmap()

        self.weekday_panel = self.WeekdayPanel(self)
        self.day_info_panel = self.InfoPanel(self, self.placeholder_img)
        self.night_info_panel = self.InfoPanel(self, self.placeholder_img)

        # add to sizer

        sizer.Add(self.weekday_panel, 1, flag=wx.EXPAND |
                  wx.LEFT, border=10)
        sizer.Add(self.day_info_panel, 1, flag=wx.EXPAND |
                  wx.RIGHT, border=10)
        sizer.Add(self.night_info_panel, 1,
                  flag=wx.EXPAND | wx.RIGHT, border=10)

    def update_content(self, data):
        weekday = data.get("weekday")
        temperature_day = data.get("temperature_day")
        image_day = data.get("image_day")
        temperature_night = data.get("temperature_night")
        image_night = data.get("image_night")
        if weekday:
            self.weekday_panel.update_content(weekday)
            self.day_info_panel.update_content(
                temperature_day, image_day)
            self.night_info_panel.update_content(
                temperature_night, image_night)
            self.Layout()

    class WeekdayPanel(wx.Panel):
        def __init__(self, parent):
            super().__init__(parent)
            self.sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.SetSizer(self.sizer)
            self.text = wx.StaticText(self, wx.ID_ANY, label="Someday")
            self.sizer.Add(self.text, 1, wx.LEFT, 5)

        def update_content(self, label):
            self.text.SetLabel(str(label))
            self.Layout()

    class InfoPanel(wx.Panel):
        def __init__(self, parent, placeholder_img):
            super().__init__(parent)
            sizer = wx.GridSizer(2)
            self.SetSizer(sizer)
            self.image = wx.StaticBitmap(self, wx.ID_ANY, placeholder_img)
            self.text = wx.StaticText(self, wx.ID_ANY, label="00.0°C")
            sizer.AddMany(
                [(self.image, 1, wx.LEFT, 10), (self.text, 2, wx.RIGHT, 10)])

        def update_content(self, label, path):
            if label and path:
                self.text.SetLabel(str(label))
                bitmap_obj = png_to_bitmap(path, 40)
                if bitmap_obj is not None:
                    self.image.SetBitmap(wx.BitmapBundle(bitmap_obj))
                self.Layout()
