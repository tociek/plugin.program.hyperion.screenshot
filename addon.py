import xbmc
import os
import sys
import xbmcaddon
import xbmcgui
import time
import subprocess
import urllib2

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )

line1 = "Welcome!"
line2 = "We take a screenshot now :)"

xbmcgui.Dialog().ok(addonname, line1, line2)
try:
    lsusb_output = subprocess.check_output('lsusb')
    if "1b71:3002" in lsusb_output:
        grabber = "utv007"
    elif "05e1:0408" in lsusb_output:
        grabber = "stk1160"

    if grabber != "":
        if "video0" in subprocess.check_output(['ls','/dev']):
            xbmcgui.Dialog().ok(addonname, "Compatible video grabber has been detected. Make sure that the source video standard is PAL")
        else:
            xbmcgui.Dialog().ok(addonname, "Video grabber has been detected but video0 does not exist. Please install drivers or use different disto")
    else:
        xbmcgui.Dialog().ok(addonname, "We have not detected the grabber. Plugin will exit...")
        sys.exit()
        
    #generating screenshot
    subprocess.call(["killall", "hyperiond"])
    os.chdir("/storage")
    if grabber == "utv007":
        xbmcgui.Dialog().ok(addonname,subprocess.check_output(["/storage/hyperion/bin/hyperion-v4l2.sh","--video-standard","PAL","--screenshot"]))
    else:
        xbmcgui.Dialog().ok(addonname,subprocess.check_output(["/storage/hyperion/bin/hyperion-v4l2.sh","--video-standard","PAL","--width","240","--height","192","--screenshot"]))
    okno = xbmcgui.WindowDialog(xbmcgui.getCurrentWindowId())
    obrazek = xbmcgui.ControlImage(0,0,1280,720,"/storage/screenshot.png")
    okno.addControl(obrazek)
    okno.show()
    obrazek.setVisible(True)
    time.sleep(5)
    okno.close()
 
except Exception, e:
     xbmcgui.Dialog().ok(addonname, repr(e),"Please report an error at plugin github issue list")


