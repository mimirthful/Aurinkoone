import wx
import time


class CurrentDate(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.weekday = wx.StaticText(
            self, id=wx.ID_ANY, label="loading info...")
        self.date = wx.StaticText(
            self, id=wx.ID_ANY, label="")
        self.clock = wx.StaticText(
            self, id=wx.ID_ANY, label="")

        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        sizer.Add(self.weekday)
        sizer.Add(self.date)
        sizer.Add(self.clock)

        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def OnTimer(self, evt):
        t = time.localtime(time.time())
        day = time.strftime("%a")
        st = time.strftime("%H:%M", t)
        dt = time.strftime("%B %d", t)
        self.weekday.SetLabel(day)
        self.clock.SetLabel(st)
        self.date.SetLabel(dt)
