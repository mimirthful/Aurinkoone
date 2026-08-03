import wx


class StatWidget(wx.Panel):
    def __init__(self, parent: wx.Window, icon: wx.Bitmap, info_name_label) -> None:
        super().__init__(parent, id=wx.ID_ANY)

        # weather widget
        sizer = wx.StaticBoxSizer(wx.StaticBox(
            self, style=wx.ALIGN_CENTRE_HORIZONTAL, label=info_name_label), wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.SetMinSize(150, -1)
        # content
        static_bmp = wx.StaticBitmap(
            sizer.GetStaticBox(), wx.ID_ANY, icon)  # type: ignore
        self.info_text = wx.StaticText(sizer.GetStaticBox(), wx.ID_ANY, "0")

        # Add to sizer
        sizer.Add(static_bmp, 2, flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.ALL, border=10)
        sizer.Add(self.info_text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.ALL, border=10)

    def update_content(self, data):
        self.info_text.SetLabel(data.get("info_label", "Load..."))
        self.Layout()
