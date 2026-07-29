import wx


def png_to_bitmap(path: str, size: int) -> wx.Bitmap:

    img = wx.Image(path, wx.BITMAP_TYPE_PNG)
    resized = img.Rescale(size, size)
    bmp = resized.ConvertToBitmap()
    return bmp
