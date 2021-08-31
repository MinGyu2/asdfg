"""
Simple BLE advertisement example
"""
from time import sleep
import bluetooth._bluetooth as bluez

from bluetooth_utils import (toggle_device, start_le_advertising,
                             stop_le_advertising, change_advert)
#import os

dev_id = 0  # the bluetooth device is hci0
toggle_device(dev_id, True)

try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

try:
    #os.system("hciconfig hci0 leadv 0")
    start_le_advertising(sock,
                         min_interval=0, max_interval=0,
                        # data=(0x11, 0x22, 0x33) + (0x01,) * 27)
                        ##data=(0x2,0x1,0x1a,0x1a,0xff,0x4c,0x0,0x2,0x15,0xe2,0xa,0x39,0xf4,0x73,0xf5,0x4b,0xc4,0xa1,0x2f,0x17,0xd1,0xad,0x7,0xa9,0x61,0x0,0x0,0x0,0x0,0xc8,0x0))
                         data=(0x4,0xff,0x01,0x02,0x00,))
    a = 0
    while True:
        if a == 2:
            data = (0x4,0xff,0x55,0x66,0x00)
            change_advert(sock,data)
        sleep(2)
        a +=1
except:
    stop_le_advertising(sock)
    raise