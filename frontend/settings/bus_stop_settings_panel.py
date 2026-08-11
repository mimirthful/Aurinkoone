import wx
from .add_bus_stop import AddBusStopWidget
from .delete_bus_stop import DeleteBusStopWidget
from .set_bus_key import SetBusKey


class BusStopSettingsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(wx.Size(450, 550)))
        # Notebook panel's main sizer
        sizer = wx.StaticBoxSizer(wx.StaticBox(
            self, label=" Bus stop settings"), wx.VERTICAL)
        self.SetSizer(sizer)
        add_stop = AddBusStopWidget(sizer.GetStaticBox())
        delete_stop = DeleteBusStopWidget(sizer.GetStaticBox())
        set_key = SetBusKey(sizer.GetStaticBox())
        sizer.Add(add_stop, 1, flag=wx.ALL | wx.EXPAND, border=5)
        sizer.Add(delete_stop, 1, flag=wx.ALL | wx.EXPAND, border=5)
        sizer.Add(set_key, 1, flag=wx.ALL | wx.EXPAND, border=5)
