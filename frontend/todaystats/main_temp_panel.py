import wx
from frontend import png_to_bitmap
from pubsub import pub


class MainTempPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.set_widget()
        pub.subscribe(self.update_content, f"hourly_forecast.now")

    def set_widget(self):
        font = wx.Font(pointSize=60, family=wx.FONTFAMILY_DECORATIVE,
                       style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_SEMIBOLD)
        self.temperature = wx.StaticText(self, wx.ID_ANY, "Loading")
        self.temperature.SetFont(font)
        placeholder_img = wx.Image(200, 200, False).ConvertToBitmap()

        self.icon = wx.StaticBitmap(self, wx.ID_ANY, placeholder_img)
        self.sizer.Add(self.temperature, 1, flag=wx.ALIGN_CENTRE_VERTICAL |
                       wx.ALL, )
        self.sizer.Add(self.icon, 1, flag=wx.ALIGN_CENTRE_VERTICAL |
                       wx.ALL,)
        self.Layout()

    def update_content(self, data):
        label = data.get("label")
        image = data.get("image")
        if label and image:
            self.temperature.SetLabel(label)
            bitmap_obj = png_to_bitmap(image, 200)
            self.icon.SetBitmap(wx.BitmapBundle(bitmap_obj))
            self.Layout()
