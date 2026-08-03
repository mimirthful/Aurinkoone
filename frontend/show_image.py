import wx
import os


def png_to_bitmap(path: str, size: int) -> wx.Bitmap:
    base_path = os.path.dirname(__file__)
    filepath = os.path.join(base_path, "..", path)
    normalized = os.path.normpath(filepath)
    img = wx.Image(normalized, wx.BITMAP_TYPE_PNG)
    resized = img.Rescale(size, size)
    bmp = resized.ConvertToBitmap()
    return bmp
