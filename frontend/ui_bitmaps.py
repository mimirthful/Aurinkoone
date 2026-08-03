import os
import wx


class UiBitmaps:
    def __init__(self):
        self.bus_stop = self._set_bitmaps("icons8-bus-64")
        self.weather = self._set_bitmaps(
            "icons8-partly-cloudy-day-64")
        self.settings = self._set_bitmaps("icons8-settings-64")
        self.uv = self._set_bitmaps("icons8-sun-64")
        self.umbrella = self._set_bitmaps("icons8-umbrella-64")
        self.wind = self._set_bitmaps("icons8-wind-64")

    def _set_bitmaps(self, icon_name: str) -> wx.Bitmap:
        try:
            base_path = os.path.dirname(__file__)
            path = os.path.join(
                base_path, "..", "icons_ui", f'{icon_name}.png')
            path = os.path.normpath(path)
            img = wx.Image(path)
            img.Rescale(64, 64)
            bmp = wx.Bitmap(img)
            return bmp
        except Exception:
            img = wx.Image()
            img.Rescale(64, 64)
            bmp = wx.Bitmap(img)
            return bmp
