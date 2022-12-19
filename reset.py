import os
import time
from uiautomator import Device


def Click(device, button):
    while True:
        device.wait.idle()
        device.dump()
        if device(text=button).wait.exists(timeout=5000):
            device(text=button).click()
        elif not device(text=button).exists:
            break

def Click2(device, button):
    while True:
        device.wait.idle()
        device.dump()
        if device(text=button).wait.exists(timeout=5000):
            device(text=button).click()
            break

def factory_reset(device):   
    d = Device(device)
    '''
    #reboot
    cmd= "adb -s %s reboot" % (device)
    os.system(cmd)
    time.sleep(30)

    '''
    #Factory reset
    cmd= "adb -s %s shell am start -a android.settings.SETTINGS" % (device)
    os.system(cmd)
    if d(resourceId="com.android.car.settings:id/car_ui_recycler_view").scroll.to(text="System"):
        Click2(d, "System")
        d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.to(text="Reset options")
        Click2(d, "Reset options")
        Click2(d, "Erase all data (factory reset)")
        Click2(d, "Erase all data")
        Click2(d, "Erase everything")
        time.sleep(75)
    '''

    cmd= "adb -s %s reboot bootloader" % (device)
    os.system(cmd)
    time.sleep(2)
    cmd= "fastboot -s %s -w" % (device)
    os.system(cmd)
    time.sleep(2)
    cmd= "fastboot -s %s reboot" % (device)
    os.system(cmd)
    time.sleep(85)    
    print("countdown end")
    '''

    #Check if need to set up profile
    Click(d, "Set up profile")
    Click(d, "OK")
    Click(d, "Skip")
    Click(d, "Skip")
    Click(d, "Next")
    Click(d, "Next")
    Click(d, "Accept")
    Click(d, "Done for now")

    #Turn on Wifi
    ssid = "GoogleGuest-Legacy"
    ssid2 = "GoogleGuest"
    cmd= "adb -s %s shell am start -a android.settings.WIRELESS_SETTINGS" % (device)
    os.system(cmd)
    if d(text="Wi‑Fi").wait.exists(timeout=3000):
        d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.to(text="Join other network")
        Click2(d, "Join other network")
        while True:
            if not d(text=ssid).exists:
                d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.to(text=ssid)
                if d(text=ssid).exists:
                    Click2(d, ssid)
                    break
            if d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.toEnd():
                d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.toBeginning(steps=4)
            if not d(text=ssid2).exists:
                d(resourceId="com.android.car.settings:id/car_ui_internal_recycler_view").scroll.to(text=ssid2)
                if d(text=ssid2).exists:
                    Click2(d, ssid2)
                    break
            
    time.sleep(2)
    #Turn on Location
    cmd= "adb -s %s shell am start -a android.settings.LOCATION_SOURCE_SETTINGS" % (device)
    os.system(cmd)
    d.dump()
    if d(text="Use location for Driver Assistance").right(className="android.widget.Switch").info['checked'] == \
    True and d(text="Use location").right(className="android.widget.Switch").info['checked'] == True:
        pass
    elif d(text="Use location for Driver Assistance").right(className="android.widget.Switch").info['checked'] == \
        False and d(text="Use location").right(className="android.widget.Switch").info['checked'] == True:
        Click2(d, "Use location")
        Click2(d, "OK")
        Click2(d, "Use location")
    else:
        Click2(d, "Use location")

    #reboot
    cmd= "adb -s %s reboot" % (device)
    os.system(cmd)