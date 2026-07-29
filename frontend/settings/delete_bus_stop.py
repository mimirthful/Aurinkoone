import wx
from pubsub import pub


class DeleteBusStopWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.codes = []
        self.text = wx.StaticText(
            self, label="Delete a bus stop")
        self.choicebox = wx.Choice(self, choices=self.codes)
        self.button = wx.Button(self, label="Send")

        self.sizer.Add(self.text, 1, flag=wx.ALL, border=5)
        self.sizer.Add(self.choicebox, 1, flag=wx.ALL, border=5)
        self.sizer.Add(self.button, 1, flag=wx.ALL, border=5)

        pub.subscribe(self.on_receive_codes, "stop_list_codes")
        self.Bind(wx.EVT_BUTTON, self.on_click, source=self.button)
        self.choicebox.Bind(wx.EVT_CHOICE, self.OnChoice)

    def on_receive_codes(self, codes):
        self.codes = codes
        self.choicebox.Clear()
        self.choicebox.AppendItems(self.codes)

    def OnChoice(self, event):
        if self.choicebox:
            self.choice = self.choicebox.GetString(
                self.choicebox.GetSelection())

    def on_click(self, evt):
        if self.choice:
            pub.sendMessage("delete stop", stop_code=self.choice)
