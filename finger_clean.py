#!/usr/bin/env python3
from pyfingerprint.pyfingerprint import PyFingerprint

try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('Sensor password is incorrect!')

    print('Currently used templates:', f.getTemplateCount())
    print('Deleting all templates...')

    f.clearDatabase()
    print('? All templates deleted successfully!')

except Exception as e:
    print('Operation failed!')
    print('Exception message:', str(e))
