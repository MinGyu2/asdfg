"""
Simple BLE advertisement example
"""
import time
import bluetooth._bluetooth as bluez

from bluetooth_utils import (toggle_device, start_le_advertising,
                             stop_le_advertising, change_advert)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 21
GPIO_ECHO = 18
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def read_distance():
    try:
        while True:
            data = []
            stop = 0
            start = 0
            GPIO.output(GPIO_TRIGGER, False)
            time.sleep(1)

            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            while GPIO.input(GPIO_ECHO) == 0:
                start = time.time()
            while GPIO.input(GPIO_ECHO) == 1:
                stop = time.time()
            elapsed = stop-start
            if(stop and start):
                distance = elapsed * 17000
                distance = round(distance, 2)
                print("Distance : %.2f cm" % distance)
                data.append(int((distance*100)/100))
                data.append(int((distance*100)%100))
                print(data)
                return data
    except KeyboardInterrupt:
        print("Ultrasonic Distance Measurement End")
        GPIO.cleanup()
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
                         min_interval=1000, max_interval=1000,
                        # data=(0x11, 0x22, 0x33) + (0x01,) * 27)
                        ##data=(0x2,0x1,0x1a,0x1a,0xff,0x4c,0x0,0x2,0x15,0xe2,0xa,0x39,0xf4,0x73,0xf5,0x4b,0xc4,0xa1,0x2f,0x17,0xd1,0xad,0x7,0xa9,0x61,0x0,0x0,0x0,0x0,0xc8,0x0))
                         data=(0x4,0xff,233,88,0x00,))
    a = 0
    while True:
        if a == 1:
            temp = read_distance()
            #print(temp)
            #data = (0x4,22,33,5,0x00,)
            data = (0x4, 0xff, temp[0], temp[1], 0x00,)
            print(data)
            change_advert(sock,data)
            a=0
        time.sleep(1)
        a +=1
except:
    stop_le_advertising(sock)
    raise
