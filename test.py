import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
from pyfingerprint.pyfingerprint import PyFingerprint

# ========== PIN SETUP ==========
BTN1, BTN2, BTN3, BTN4 = 17, 27, 22, 23  # GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in [BTN1, BTN2, BTN3, BTN4]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ========== LCD SETUP ==========
lcd = CharLCD('PCF8574', 0x27)  # Try 0x3F if not working
lcd.clear()
lcd.write_string("Initializing...")

# ========== FINGERPRINT SENSOR ==========
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('Fingerprint sensor password is incorrect!')

except Exception as e:
    lcd.clear()
    lcd.write_string('Sensor Error!')
    print("The sensor could not be initialized!")
    print("Exception message: " + str(e))
    exit(1)

lcd.clear()
lcd.write_string("System Ready!")

# ========== FUNCTIONS ==========

def wait_for_touch():
    """Wait for a button press and return its number."""
    while True:
        if GPIO.input(BTN1): return 1
        if GPIO.input(BTN2): return 2
        if GPIO.input(BTN3): return 3
        if GPIO.input(BTN4): return 4
        time.sleep(0.1)

def enroll_finger():
    lcd.clear()
    lcd.write_string("Enroll Mode...")
    print("Waiting for finger...")

    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        lcd.clear()
        lcd.write_string("Already exists")
        time.sleep(2)
        return

    lcd.clear()
    lcd.write_string("Remove finger...")
    time.sleep(2)

    lcd.clear()
    lcd.write_string("Place same again")
    while not f.readImage():
        pass

    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        lcd.clear()
        lcd.write_string("No match")
        time.sleep(2)
        return

    f.createTemplate()
    positionNumber = f.storeTemplate()
    lcd.clear()
    lcd.write_string("Stored at pos:")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(str(positionNumber))
    print("Finger enrolled at position #" + str(positionNumber))
    time.sleep(3)


def search_finger():
    lcd.clear()
    lcd.write_string("Scan finger...")
    print("Waiting for finger...")

    while not f.readImage():
        pass

    f.convertImage(0x01)
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if positionNumber == -1:
        lcd.clear()
        lcd.write_string("Not found")
        print("No match found.")
    else:
        lcd.clear()
        lcd.write_string("Found ID: ")
        lcd.write_string(str(positionNumber))
        print("Found template at position #" + str(positionNumber))
        print("Accuracy: " + str(accuracyScore))

    time.sleep(3)


def delete_finger():
    lcd.clear()
    lcd.write_string("Enter ID to del")
    print("Enter ID to delete: ")
    try:
        positionNumber = int(input("Enter ID: "))
        if f.deleteTemplate(positionNumber):
            lcd.clear()
            lcd.write_string("Deleted ID:")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(str(positionNumber))
            print("Template deleted!")
    except Exception as e:
        lcd.clear()
        lcd.write_string("Error deleting")
        print("Error: " + str(e))
    time.sleep(3)

# ========== MAIN LOOP ==========

lcd.clear()
lcd.write_string("1-Enroll")
lcd.cursor_pos = (1, 0)
lcd.write_string("2-Verify 3-Del 4-Exit")

try:
    while True:
        btn = wait_for_touch()

        if btn == 1:
            enroll_finger()
        elif btn == 2:
            search_finger()
        elif btn == 3:
            delete_finger()
        elif btn == 4:
            lcd.clear()
            lcd.write_string("Goodbye :)")
            time.sleep(1)
            break

        lcd.clear()
        lcd.write_string("1-Enroll")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("2-Verify 3-Del 4-Exit")

except KeyboardInterrupt:
    pass

finally:
    lcd.clear()
    GPIO.cleanup()
