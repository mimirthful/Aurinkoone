import wx
from pubsub import pub
from wx import adv


class SetBusKey(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.text = wx.StaticText(
            self, label="Enter Digitransit API-key")
        self.link = adv.HyperlinkCtrl(
            self, label="How to get API-key?", url="https://digitransit.fi/en/developers/api-registration/")
        self.input = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.add_key_button = wx.Button(self, label="Add key")
        self.add_key_button.GetDefaultSize(self)
        self.remove_key_button = wx.Button(self, label="Remove key")
        self.remove_key_button.SetForegroundColour(wx.Colour("Red"))
        self.remove_key_button.GetDefaultSize(self)

        self.Bind(wx.EVT_BUTTON, self.on_add_click, source=self.add_key_button)
        self.Bind(wx.EVT_BUTTON, self.on_remove_click,
                  source=self.remove_key_button)

        self.sizer.AddMany(((self.text, 0, wx.ALL, 5), (self.link, 0, wx.ALL, 5), (self.input, 0, wx.ALL, 5),
                           (self.add_key_button, 0, wx.ALL, 5), (self.remove_key_button, 0, wx.ALL, 5)))
        pub.subscribe(self.on_created, "api_key_changed_status_response")
        pub.subscribe(self.text_color_change, "api_key_info_changed")
        pub.sendMessage("api_key_status_check")

    def on_created(self, message):
        pub.sendMessage("notification_text_received",
                        label=f'Setting API key:\n{message}')

    def on_add_click(self, evt):
        data = self.input.GetValue()
        wx.CallAfter(pub.sendMessage, "api_key_added", key=data)

    def on_remove_click(self, evt):
        pub.sendMessage("remove_text_received",
                        label=f"Remove API key:\nRemoving your API key will delete ALL\nsaved bus stops permanently.\nTo restore data later, you'll need to:\n• Re-enter your API key\n• Re-add your bus stops manually")

    def text_color_change(self, key_exists):
        if key_exists:
            self.input.SetBackgroundColour(wx.Colour("Green"))
            self.input.SetValue("**************")
            self.input.Disable()
            self.add_key_button.Hide()
            self.remove_key_button.Show()
            self.Layout()
        else:
            self.input.SetBackgroundColour(wx.Colour("Red"))
            self.input.Enable()
            self.input.SetValue("")
            self.add_key_button.Show()
            self.remove_key_button.Hide()
            self.Layout()
