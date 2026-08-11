import wx
from .bus_widget import BusWidget
from .bus_stop_times_header import BusStopTimesHeader
from .bus_stop_info_header import BusStopInfoHeader


class BusStopPanel(wx.Panel):
    def __init__(self, parent: wx.Window, stop_info):
        super().__init__(parent, id=wx.ID_ANY)
        self.stop_info = stop_info
        self.departed = []
        self.last_added_list_index = 0
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetMinSize(wx.Size(470, -1))
        self.SetSizer(self.sizer)
        info_header = BusStopInfoHeader(
            self, self.stop_info["name"], self.stop_info["code"])
        self.sizer.Add(info_header, 1, wx.EXPAND)
        time_header = BusStopTimesHeader(self)
        self.sizer.Add(time_header, proportion=1, flag=wx.EXPAND)
        self.bus_panel = wx.Panel(self)
        self.bus_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bus_panel.SetSizer(self.bus_sizer)
        self.sizer.Add(self.bus_panel, flag=wx.EXPAND)
        self.add_widgets()
        self.SetBackgroundColour(wx.Colour(21, 56, 105))

    def add_widgets(self):
        for bus in self.stop_info["stop_times"]:
            self.add_bus(bus)

    def add_bus(self, bus):
        if self.IsBeingDeleted():
            return
        identify = (bus["bus_short_name"], bus["bus_scheduled_dep"])
        if self._has_departed(identify):
            return
        children = self.bus_sizer.GetChildren()
        visible = []
        for child in children:
            if child.GetWindow() and child.GetWindow().IsShown():
                visible.append(child)

        if len(visible) <= 7:
            colour = wx.Colour(f'#{bus["bus_color"]}')
            widget = BusWidget(self.bus_panel, colour, identify)

            widget.update_content(bus)
            self.bus_sizer.Add(widget, 1, flag=wx.EXPAND |
                               wx.LEFT | wx.RIGHT, border=3)
            self.last_added_list_index = self.last_added_list_index + 1

    def on_bus_departed(self, bus_data):
        self.departed.append(bus_data)
        new_bus_index = self.last_added_list_index + 1
        if new_bus_index < len(self.stop_info["stop_times"]):
            bus = self.stop_info["stop_times"][new_bus_index]
            self.add_bus(bus)

    def _has_departed(self, bus):
        return bus in self.departed

    # custom destroy logic because the timer inside bus_widget crashes everything otherwise
    # DO NOT DELETE
    def Destroy(self) -> bool:
        children = self.bus_sizer.GetChildren()

        for child in children:
            win = child.GetWindow()
            if win and not win.IsBeingDeleted():
                win.Destroy()
        return super().Destroy()
