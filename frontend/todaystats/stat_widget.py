import wx


class StatWidget(wx.Panel):
    def __init__(self, parent: wx.Window, icon: wx.Bitmap, info_name_label, bg_colour) -> None:
        super().__init__(parent, id=wx.ID_ANY)
        self.bg_colour = bg_colour
        # info to be shown

        # weather widget
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.SetMinSize(150, -1)
        title = wx.StaticText(self, label=info_name_label)
        sizer.Add(title, flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.TOP, border=10)
        # content
        static_bmp = wx.StaticBitmap(
            self, wx.ID_ANY, icon)  # type: ignore
        self.info_text = wx.StaticText(self, wx.ID_ANY, "0")

        # Add to sizer
        sizer.Add(static_bmp, 2, flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.ALL, border=10)
        sizer.Add(self.info_text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.ALL, border=10)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def update_content(self, data):
        self.info_text.SetLabel(data.get("info_label", "Load..."))
        self.Layout()

    def OnPaint(self, event):

        pdc = wx.PaintDC(self)
        gc = wx.GCDC(pdc)

        gc.SetPen(wx.Pen(self.bg_colour, 1))
        gc.SetBrush(wx.Brush(self.bg_colour))
        size = self.GetSize()
        x = 0
        y = 0
        w = size.width
        h = size.height

        gc.DrawRoundedRectangle(x, y, w, h, 5)
        y += 100

    def OnEraseBackground(self, event):
        pass
