import time
from bingimage import getBingImage
from settings import BING_CHINA

import sys
_ver = sys.version_info
py3_or_upper = (_ver[0] > 2)

def setWallpaperWithBingImage():
    if py3_or_upper == False:
        return -1
    if sys.platform != "win32":
        return -1

    imgData = getBingImage(BING_CHINA)
    if imgData == None:
        return -1

    import tempfile
    fp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    if fp == None:
        return -1
    fp.write(imgData)
    tmp_name = fp.name
    fp.close()
    fp = None

    import ctypes
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDCHANGE = 2
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, tmp_name, SPIF_SENDCHANGE | SPIF_UPDATEINIFILE)

    import os
    os.remove(tmp_name)

    print("Set wallpaper successful.")

    return 0

if __name__=="__main__":
    res = 0
    i = 0
    while i < 6:
        res = setWallpaperWithBingImage()
        if res == 0:
            break
        time.sleep(2)
        i += 1

    sys.exit(res)
