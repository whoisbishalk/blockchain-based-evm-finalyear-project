#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import json
from pyfingerprint.pyfingerprint import PyFingerprint
from RPLCD.i2c import CharLCD
from web3 import Web3

# ==============================
# Hardware setup
# ==============================
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()
lcd.write_string("Initializing...")

BTN3 = 15  # Next voter
BTN4 = 16  # Exit

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN3, GPIO.IN)
GPIO.setup(BTN4, GPIO.IN)

VOTER_FILE = "voter_list.json"

# ==============================
# Blockchain setup (Ganache)
# ==============================
GANACHE_URL = "http://192.168.1.72:7545"  # Change to your Ganache RPC URL
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    lcd.clear()
    lcd.write_string("Ganache Error!")
    print("? Cannot connect to Ganache! Check network or RPC URL.")
    exit(1)

accounts = w3.eth.accounts
if not accounts:
    lcd.clear()
    lcd.write_string("No Accounts!")
    print("? No Ethereum accounts found in Ganache.")
    exit(1)

print(f"Connected to Ganache. Total accounts: {len(accounts)}")

# ==============================
# Load or create voter list
# ==============================
try:
    with open(VOTER_FILE, "r") as f:
        voter_list = json.load(f)
except FileNotFoundError:
    voter_list = {}
    with open(VOTER_FILE, "w") as f:
        json.dump(voter_list, f, indent=4)
    print(f"Created new voter list file: {VOTER_FILE}")

# ==============================
# Initialize fingerprint sensor
# ==============================
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("Wrong fingerprint sensor password!")
except Exception as e:
    lcd.clear()
    lcd.write_string("Sensor Error!")
    print("Fingerprint sensor init failed:", e)
    exit(1)
    
lcd.clear()
lcd.write_string("System Ready")
time.sleep(1.5)

# ==============================
# Helper functions
# ==============================
def display(line1="", line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    if line2:
        lcd.crlf()
        lcd.write_string(line2[:16])

def save_voter_list():
    with open(VOTER_FILE, "w") as fjson:
        json.dump(voter_list, fjson, indent=4)
    display("Data Saved", "")
    print("? Voter list saved.")
    time.sleep(1)

def capture_finger(scan_num, voter_name):
    display(f"{voter_name}", f"Scan {scan_num}/4")
    print(f"Waiting for finger... Scan {scan_num}/4")
    while True:
        if f.readImage():
            f.convertImage(0x01)
            template = f.downloadCharacteristics(0x01)
            display(f"{voter_name}", f"Captured {scan_num}/4")
            print(f"? Fingerprint scan {scan_num} captured")
            time.sleep(2)  # 2 sec delay after each capture
            return [int(x) for x in template]
        time.sleep(0.2)

def get_next_eth_address():
    """Assign next unused Ganache address automatically."""
    used_addresses = {v["address"] for v in voter_list.values() if "address" in v}
    for acc in accounts:
        if acc not in used_addresses:
            print(f"? Assigning new address: {acc}")
            return acc
    return None

def is_duplicate_fingerprint(template):
    """Compare new fingerprint with existing templates."""
    for stored in voter_list.values():
        for t in stored["templates"]:
            f.uploadCharacteristics(0x01, template)
            f.uploadCharacteristics(0x02, t)
            score = f.compareCharacteristics()
            if score > 50:  # Threshold for duplicate detection
                return True
    return False

# ==============================
# Enrollment Function
# ==============================
def enroll_voter(voter_name):
    templates = []

    # Capture 4 fingerprints
    for i in range(1, 5):
        template = capture_finger(i, voter_name)

        # Duplicate check after each capture
        if is_duplicate_fingerprint(template):
            display("Duplicate Found", "")
            print("? This fingerprint already exists in database.")
            time.sleep(2)
            return False

        templates.append(template)

    # Assign Ethereum address only if unique fingerprint
    eth_address = get_next_eth_address()
    if not eth_address:
        display("No Free Addr", "")
        print("? No free Ethereum address left in Ganache!")
        return False

    # Save voter data
    voter_list[voter_name] = {
        "templates": templates,
        "has_voted": False,
        "address": eth_address
    }

    display("Voter Saved", voter_name)
    print(f"? Voter '{voter_name}' enrolled with address {eth_address}")
    save_voter_list()
    time.sleep(2)
    return True

# ==============================
# Main Loop
# ==============================
try:
    display("BTN3: Next", "BTN4: Exit")
    print("Press BTN3 to enroll new voter, BTN4 to exit")

    while True:
        if GPIO.input(BTN3) == GPIO.HIGH:
            display("Enter Name:", "")
            voter_name = input("Enter voter name: ").strip()
            if not voter_name:
                display("Invalid Name", "")
                time.sleep(1)
                continue

            success = enroll_voter(voter_name)
            if success:
                print("Voter enrollment completed.")
            else:
                print("Enrollment cancelled or failed.")

            display("BTN3: Next", "BTN4: Exit")

        elif GPIO.input(BTN4) == GPIO.HIGH:
            display("Exiting...", "")
            print("Exiting voter enrollment...")
            save_voter_list()
            time.sleep(2)
            break

        time.sleep(0.2)

except KeyboardInterrupt:
    display("Interrupted!", "")
    save_voter_list()

finally:
    GPIO.cleanup()
    display("Program Ended", "")
