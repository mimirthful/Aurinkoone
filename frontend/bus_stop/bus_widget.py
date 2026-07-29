import wx
from datetime import datetime as dt


class BusWidget(wx.Panel):
    def __init__(self, parent: wx.Window,  background_color, identify):
        super().__init__(parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.identify = identify
        self.parent_panel = parent
        self.SetSizer(sizer)
        self.SetBackgroundColour(background_color)
        self.bus_name = ChildPanel(self)
        self.headsign = ChildPanel(self)
        self.bus_dep = ChildPanel(self)

        sizer.Add(self.bus_name, 1, flag=wx.ALIGN_CENTER_VERTICAL |
                  wx.TOP | wx.BOTTOM, border=7)
        sizer.Add(self.headsign, 1, flag=wx.ALIGN_CENTER_VERTICAL |
                  wx.TOP | wx.BOTTOM, border=7)
        sizer.AddStretchSpacer()
        sizer.Add(self.bus_dep, 1, flag=wx.ALIGN_CENTER_VERTICAL |
                  wx.TOP | wx.BOTTOM, border=7)

    def update_content(self, data):
        self.bus_name.update_content(data["bus_short_name"])
        self.headsign.update_content(data["headsign"])
        self.bus_dep.set_up_deltashow(
            data["bus_scheduled_dep"], data["bus_real_time_dep"], data["realtime"])

    def Hide(self) -> bool:

        ret = super().Hide()
        panel = self.GetParent().GetParent()
        if panel:
            panel.on_bus_departed(self.identify)  # type: ignore
        parent = self.GetParent()
        if parent and parent.GetSizer():
            parent.GetSizer().Layout()
            parent.Refresh()

        return ret

    # custom destroy logic because the timer inside child_panel crashes everything otherwise
    # DO NOT DELETE

    def Destroy(self) -> bool:
        self.bus_name.Destroy()
        self.headsign.Destroy()
        self.bus_dep.Destroy()
        return super().Destroy()


class ChildPanel(wx.Panel):
    def __init__(self, parent: wx.Window,):
        super().__init__(parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.SetSizer(sizer)
        self.text = wx.StaticText(
            self, wx.ID_ANY, label="Loading")
        sizer.Add(self.text, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.arrive_time = dt.now()
        self.timer = None
        self.is_realtime = False
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def update_content(self, label):
        self.text.SetLabel(str(label))
        self.Layout()

    def set_up_deltashow(self, scheduled_label: dt, realtime_label: dt, is_realtime: bool):
        self.is_realtime = is_realtime
        if self.is_realtime:
            self.text.SetForegroundColour(wx.Colour("#D0FE1D"))
            self.arrive_time = realtime_label
        else:
            self.text.SetForegroundColour(wx.Colour("#FFFFFF"))
            self.arrive_time = scheduled_label

        if self.timer is None:
            self.timer = wx.Timer(self)
            self.timer.Start(1000)

    def OnTimer(self, evt):
        if self.timer is None or self.IsBeingDeleted():
            return

        parent = self.GetParent()
        if parent is None or not parent.IsShownOnScreen():
            return

        if self.arrive_time > dt.now():
            if self.is_realtime:
                time_left = self.arrive_time - dt.now()
                minutes = int(time_left.total_seconds()) // 60
                self.update_content(minutes)
            else:
                styled = self.arrive_time.strftime("%H:%M")
                self.update_content(styled)
        else:
            if self.timer is not None:
                self.timer.Stop()
                self.timer = None
                self.GetParent().Hide()

    def Destroy(self):
        if self.timer is not None:
            self.timer.Stop()
            self.timer = None
        self.Unbind(wx.EVT_TIMER, handler=self.OnTimer)
        return super().Destroy()
