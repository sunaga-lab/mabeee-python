#!/usr/bin/env python3

from bluepy import btle
import sys
import os
import cmd

def scan_for(print_list=False, name=None, scan_duration=3.0):
    scanner = btle.Scanner(0)
    devices = scanner.scan(scan_duration)
    result = None
    for device in devices:
        for (code, description, val) in device.getScanData():
            if code == 9 and val.startswith("MaBeee"):
                if print_list:
                    print(f"- Device {val} addr {device.addr}")
                if val == name:
                    result = device.addr
                break
    return result


def connect(mac_addr):
    peripheral = btle.Peripheral()
    peripheral.connect(mac_addr, btle.ADDR_TYPE_RANDOM)
    return peripheral

def write_pwm(peripheral, value):
    PWM_HANDLE = 17
    PWM_INDEX = 1
    data = bytearray(peripheral.readCharacteristic(PWM_HANDLE))
    data[PWM_INDEX] = value
    peripheral.writeCharacteristic(17, bytes(data), True)


if len(sys.argv) <= 1:
    print("""Usage: 
    ./mabeee_ctrl.py scan             Device scan (requires root):
    ./mabeee_ctrl.py [MAC addr|name]  Connect to device
""")
    
elif sys.argv[1] == "scan":
    scan_for(print_list=True)
else:
    target = sys.argv[1]
    if target.startswith("MaBeee"):
        target_addr = scan_for(name=target)
    else:
        target_addr = target
    peripheral = connect(target_addr)
    
    while True:
        print("PWM 0-100: ", end="")
        sys.stdout.flush()
        line = sys.stdin.readline()
        try:
            value = int(line.strip())
            write_pwm(peripheral, value)
        except ValueError:
            break
    
    peripheral.disconnect()
    print("End.")
        
        

