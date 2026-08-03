import wx
from frontend.bus_stop import BusStopPanel
from frontend.todaystats import CurrentDate
from pubsub import pub
import wx.lib.scrolledpanel as scrolled


class NotebookBusPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.clock = CurrentDate(self)
        self.main_sizer.Add(self.clock, proportion=0, flag=wx.ALL, border=10)

        self.child_panel = scrolled.ScrolledPanel(
            self)
        self.child_panel.SetupScrolling()
        self.child_panel.SetMinClientSize(wx.Size(300, 470))
        self.child_sizer = wx.GridSizer(2, wx.Size(1, 1))
        self.child_panel.SetSizer(self.child_sizer)
        self.main_sizer.Add(self.child_panel, 0, wx.EXPAND |
                            wx.CENTER | wx.ALL, 10)
        pub.subscribe(self.clear_sizer, "clear notebook_bus_panel")
        pub.subscribe(self.create_stop_widgets, 'stop available')

    # Creates a stop widget
    def create_stop_widgets(self, data):
        bus_panel = BusStopPanel(self.child_panel, data)
        self.child_sizer.Add(
            bus_panel, 1, wx.ALL, border=10)
        self.child_sizer.Layout()
        self.main_sizer.Layout()

    def clear_sizer(self):
        self.child_sizer.Clear(True)
        self.child_sizer.Layout()
        self.main_sizer.Layout()
        pub.sendMessage("notebook_bus_panel empty")
