import wx
from frontend import png_to_bitmap
from pubsub import pub


class HourlyForecastHourWidget(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, id=wx.ID_ANY)
        # weather widget
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetMinSize(wx.Size(100, -1))

        # content
        self.hour = self.ChildTextPanel(self, "00")
        self.placeholder_img = wx.Image(64, 64, False).ConvertToBitmap()
        self.image = wx.StaticBitmap(self, wx.ID_ANY, self.placeholder_img)
        self.label = self.ChildTextPanel(self, "00.0°C")
        self.rain_label = self.ChildTextPanel(self, " 0.0%")
        sizer.Add(self.hour, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        sizer.Add(self.image, 2, flag=wx.EXPAND)
        sizer.Add(self.label, 1, flag=wx.EXPAND | wx.TOP, border=5)
        sizer.Add(self.rain_label, 1, flag=wx.EXPAND | wx.BOTTOM, border=5)

    def update_content(self, data):
        hour = data.get("hour")
        image = data.get("image")
        label = data.get("label")
        rain_change = data.get("rain_change")
        if hour and image and label and rain_change:
            self.hour.update_content(hour)
            bitmap_obj = png_to_bitmap(image, 64)
            self.image.SetBitmap(wx.BitmapBundle(bitmap_obj))
            self.label.update_content(label)
            self.rain_label.update_content(rain_change)
            self.Layout()

    class ChildTextPanel(wx.Panel):
        def __init__(self, parent, label):
            super().__init__(parent, id=wx.ID_ANY)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(sizer)
            self.text = wx.StaticText(self, wx.ID_ANY, label=label)
            sizer.Add(self.text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        def update_content(self, label):
            self.text.SetLabel(label)
