import wx
from pubsub import pub


class MessagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(wx.Size(450, 300)))
        # Notebook panel's main sizer
        self.sizer = wx.StaticBoxSizer(wx.StaticBox(
            self), wx.VERTICAL)
        self.SetSizer(self.sizer)
        notification = NotificationText(self.sizer.GetStaticBox())
        self.sizer.Add(notification, 1, flag=wx.ALL | wx.EXPAND, border=10)
        pub.subscribe(notification.edit_text, "notification_text_received")
        pub.subscribe(notification.remove_key, "remove_text_received")


class NotificationText(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.text = wx.StaticText(self, label="")

        self.button = wx.Button(self, label="Close")
        self.button.GetDefaultSize(self)
        self.button.Hide()
        self.delete_button = wx.Button(self, label="Remove")
        self.delete_button.SetForegroundColour(wx.Colour("Red"))
        self.delete_button.Hide()
        self.sizer.Add(self.text, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.delete_button, 0, wx.ALL, 5)
        self.sizer.Add(self.button, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.on_click, source=self.button)
        self.Bind(wx.EVT_BUTTON, self.delete_key_click,
                  source=self.delete_button)

    def edit_text(self, label):
        self.delete_button.Hide()
        self.text.SetLabel(label)
        self.button.Show()
        self.sizer.Layout()
        self.SendSizeEvent()

    def on_click(self, evt):
        self.delete_button.Hide()
        self.text.SetLabel("")
        self.button.Hide()

    def remove_key(self, label):
        self.text.SetLabel(label)
        self.delete_button.Show()
        self.button.Show()
        self.sizer.Layout()

    def delete_key_click(self, evt):
        wx.CallAfter(pub.sendMessage, "api_key_removed")
        self.delete_button.Hide()
        self.text.SetLabel("")
        self.button.Hide()
        pub.sendMessage("notification_text_received",
                        label=f'Remove API key:\nAPI key deleted succesfully.')
