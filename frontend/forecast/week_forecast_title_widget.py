import wx
from frontend import png_to_bitmap
import os


class WeekForecastTitleWidget(wx.Panel):
    def __init__(self, parent: wx.Window):
        super().__init__(parent, id=wx.ID_ANY)
        sizer = wx.GridSizer(3)
        self.SetSizer(sizer)
        base_path = os.path.dirname(__file__)

        # Cal title
        self.image_cal = wx.Panel(self)
        image_cal_sizer = wx.BoxSizer(wx.VERTICAL)
        self.image_cal.SetSizer(image_cal_sizer)

        path = os.path.join(base_path, "..", "..",
                            "icons_ui", f'calendar.png')
        normalized = os.path.normpath(path)
        bitmap_obj = png_to_bitmap(normalized, 36)
        image_cal_text = wx.StaticBitmap(
            self.image_cal, wx.ID_ANY, wx.BitmapBundle(bitmap_obj))

        image_cal_sizer.AddSpacer(5)
        image_cal_sizer.Add(
            image_cal_text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL,)
        image_cal_sizer.AddSpacer(5)
        # Day title
        image_day = wx.Panel(self)
        image_day.SetBackgroundColour(wx.Colour("#E5BD2EFF"))
        image_day_sizer = wx.BoxSizer(wx.VERTICAL)
        image_day.SetSizer(image_day_sizer)
        path = os.path.join(base_path, "..", "..",
                            "icons_ui", f'sun.png')
        normalized = os.path.normpath(path)
        bitmap_obj = png_to_bitmap(normalized, 36)
        image_day_text = wx.StaticBitmap(
            image_day, wx.ID_ANY, wx.BitmapBundle(bitmap_obj))

        image_day_sizer.AddSpacer(5)
        image_day_sizer.Add(
            image_day_text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL, )
        image_day_sizer.AddSpacer(5)
        # Night title
        self.image_night = wx.Panel(
            self)
        image_night_sizer = wx.BoxSizer(wx.VERTICAL)
        self.image_night.SetSizer(image_night_sizer)

        path = os.path.join(base_path, "..", "..",
                            "icons_ui", f'moon.png')
        normalized = os.path.normpath(path)
        bitmap_obj = png_to_bitmap(normalized, 36)
        image_night_text = wx.StaticBitmap(
            self.image_night, wx.ID_ANY, wx.BitmapBundle(bitmap_obj))

        image_night_sizer.AddSpacer(5)
        image_night_sizer.Add(
            image_night_text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, )
        image_night_sizer.AddSpacer(5)

        sizer.Add(self.image_cal, 1, flag=wx.EXPAND | wx.LEFT, border=5)
        sizer.Add(image_day, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=1)
        sizer.Add(self.image_night, 1, flag=wx.EXPAND | wx.RIGHT, border=5)
        self.image_cal.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.image_cal.Bind(wx.EVT_PAINT, self.OnPaintLeft)
        self.image_night.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.image_night.Bind(wx.EVT_PAINT, self.OnPaintRight)

    def OnPaintLeft(self, event):

        pdc = wx.PaintDC(self.image_cal)
        gc = wx.GCDC(pdc)

        gc.SetPen(wx.Pen(wx.Colour("#E94558FF"), 1))
        gc.SetBrush(wx.Brush(wx.Colour("#E94558FF")))
        size = self.image_cal.GetSize()
        x = 0 + 5
        y = 0
        w = size.width + 5
        h = size.height

        gc.DrawRoundedRectangle(x, y, w, h, 5)
        y += 100

    def OnEraseBackground(self, event):
        pass

    def OnPaintRight(self, event):

        pdc = wx.PaintDC(self.image_night)
        gc = wx.GCDC(pdc)

        gc.SetPen(wx.Pen(wx.Colour("#3AC1DCFF"), 1))
        gc.SetBrush(wx.Brush(wx.Colour("#3AC1DCFF")))
        size = self.image_night.GetSize()
        x = -5
        y = 0
        w = size.width
        h = size.height

        gc.DrawRoundedRectangle(x, y, w, h, 5)
        y += 100
