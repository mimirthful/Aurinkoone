import wx
from .add_bus_stop import AddBusStopWidget
from .delete_bus_stop import DeleteBusStopWidget


class BusStopSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # Notebook panel's main sizer
        sizer = wx.StaticBoxSizer(wx.StaticBox(
            self, label=" Bus stop settings"), wx.VERTICAL)
        self.SetSizer(sizer)
        add_stop = AddBusStopWidget(self)
        delete_stop = DeleteBusStopWidget(self)
        sizer.Add(add_stop, 1, flag=wx.ALL, border=5)
        sizer.Add(delete_stop, 1, flag=wx.ALL, border=5)
