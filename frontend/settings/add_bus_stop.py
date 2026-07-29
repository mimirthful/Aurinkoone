import wx
from pubsub import pub


class AddBusStopWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.text = wx.StaticText(
            self, label="Add a bus stop by typing it's code (ie. 0002)")
        self.input = wx.TextCtrl(self)
        self.button = wx.Button(self, label="Send")
        self.success_text = wx.StaticText(
            self, label="")
        self.Bind(wx.EVT_BUTTON, self.on_click, source=self.button)
        self.sizer.AddMany(((self.text, 1, wx.ALL, 5), (self.input, 1, wx.ALL, 5),
                           (self.button, 1, wx.ALL, 5), (self.success_text, 1)))
        pub.subscribe(self.on_created, "bus_stop_created_message")

    def on_created(self, message):
        self.success_text.SetLabel(message)
        self.sizer.Layout()

    def on_click(self, evt):
        data = self.input.GetValue()
        pub.sendMessage("new stop", stop_code=data)
