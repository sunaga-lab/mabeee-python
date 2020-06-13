#!/usr/bin/env python3

from bluepy import btle
import time
import sys
import os

peripheral = None
def scan():
    scanner = btle.Scanner(0)
    devices = scanner.scan(1.0)
     
    for device in devices:
        print(f"[ADDR {device.addr}]")
        print(f"  AddrType {device.addrType}")
        for (adTypeCode, description, valueText) in device.getScanData():
            print(f"  ad: code:{adTypeCode} {description}：{valueText}")

def connect():
    print("connecting...")
    MAC_ADDRESS = os.environ["MABEEE_ADDR"]
    peripheral = btle.Peripheral()
    peripheral.connect(MAC_ADDRESS, btle.ADDR_TYPE_RANDOM)
    return peripheral

def get_services(peripheral):
    print("Services:")
    for service in peripheral.getServices():
        print(f"UUID: {service.uuid}")
        for characteristic in service.getCharacteristics():
            print(f"  UUID: {characteristic.uuid}")
            print(f"  Handle: {characteristic.getHandle()}")
            prop = characteristic.propertiesToString()
            print(f"  Prop: {prop}")
            if "READ" in prop:
                read = peripheral.readCharacteristic(characteristic.getHandle())
                print(f"  Read Result：{read}")
        desc_list = service.getDescriptors()
        for desc in desc_list:
            print(desc.uuid)
            print(desc.handle)
            print(str(desc))

def test_write(peripheral):
    print("Test write:")
    PWM_HANDLE = 17
    PWM_INDEX = 1
    
    data = bytearray(peripheral.readCharacteristic(PWM_HANDLE))
    data[PWM_INDEX] = 0
    peripheral.writeCharacteristic(17, b"\xFF\xFF\xFF\xFF\xFF", True)


def write_pwm(peripheral, value):
    print(f"write_pwm: {value}")
    PWM_HANDLE = 17
    PWM_INDEX = 1
    data = bytearray(peripheral.readCharacteristic(PWM_HANDLE))
    data[PWM_INDEX] = value
    peripheral.writeCharacteristic(17, bytes(data), True)



candidates = [
    (17, b"\x01\x00\x00\x00\x00"),
    (20, b"\x00X\x02\x00\x00"),
    (23, b"\x00X\x02\x00\x00"),
    (41, b"\x00"),
]

def test_write_scan(peripheral):
    for (hndl, msg) in candidates:
        for idx in range(len(msg)):
            for n in range(0xFF):
                mut = bytearray(msg)
                mut[idx] = n
                msgw = bytes(mut)
                print(f" write {hndl} = {msgw} (idx:{idx}, n:{n})")
                peripheral.writeCharacteristic(hndl, msgw, True)
                time.sleep(0.05)
    
scan()
peripheral = connect()
# get_services(peripheral)
write_pwm(peripheral, 0)
time.sleep(1)
write_pwm(peripheral, 40)
time.sleep(10)
write_pwm(peripheral, 60)
time.sleep(10)
write_pwm(peripheral, 40)
time.sleep(1)
print("done.")

