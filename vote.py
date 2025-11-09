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
lcd = CharLCD('PCF8574', 0x27)  # adjust I2C address if needed
lcd.clear()
lcd.write_string("Initializing...")

BTN1 = 11  # Candidate 1
BTN2 = 13  # Candidate 2
BTN3 = 15  # Candidate 3
BTN4 = 16  # Confirm vote

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN1, GPIO.IN)
GPIO.setup(BTN2, GPIO.IN)
GPIO.setup(BTN3, GPIO.IN)
GPIO.setup(BTN4, GPIO.IN)

VOTER_FILE = "voter_list.json"

# ==============================
# Load voter list
# ==============================
try:
    with open(VOTER_FILE, "r") as f:
        voter_list = json.load(f)
except FileNotFoundError:
    print("? No voter list found! Run voter_enroll.py first.")
    exit(1)

# ==============================
# Blockchain setup
# ==============================
GANACHE_URL = "http://192.168.1.72:7545"  # your Ganache RPC URL
CONTRACT_ADDRESS = "0xc0515470ff3bA418763974fb88f11f87d78dc648"  # update if redeployed
ABI_FILE = "Voting.json"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    lcd.clear()
    lcd.write_string("Ganache Error!")
    print("? Cannot connect to Ganache. Check network.")
    exit(1)

try:
    with open(ABI_FILE, "r") as f:
        contract_json = json.load(f)
    ABI = contract_json["abi"]
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
except Exception as e:
    print("? Error loading ABI:", e)
    exit(1)
    
# ==============================
# Fingerprint sensor
# ==============================
try:
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("Wrong fingerprint sensor password!")
except Exception as e:
    lcd.clear()
    lcd.write_string("Sensor Error!")
    print("? Fingerprint sensor init failed:", e)
    exit(1)

lcd.clear()
lcd.write_string("System Ready")
time.sleep(1)

# ==============================
# Helper functions
# ==============================
def display(line1="", line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    if line2:
        lcd.crlf()
        lcd.write_string(line2[:16])

def capture_finger():
    display("Place Finger", "")
    print("Waiting for finger...")
    while True:
        if f.readImage():
            f.convertImage(0x01)
            template = f.downloadCharacteristics(0x01)
            display("Captured", "")
            print("? Fingerprint captured")
            return [int(x) for x in template]
        time.sleep(0.2)

def identify_voter(template):
    for voter_name, data in voter_list.items():
        for t in data["templates"]:
            t_int = [int(x) for x in t]
            f.uploadCharacteristics(0x01, template)
            f.uploadCharacteristics(0x02, t_int)
            score = f.compareCharacteristics()
            if score > 50:
                return voter_name, data
    return None, None

def save_voter_list():
    with open(VOTER_FILE, "w") as fjson:
        json.dump(voter_list, fjson, indent=4)
    print("? Voter list updated.")

# ==============================
# Continuous Voting Loop
# ==============================
try:
    while True:
        display("Place Finger", "")
        template = capture_finger()
        voter_name, data = identify_voter(template)

        if voter_name is None:
            display("Not Eligible", "")
            print("? Fingerprint not found.")
            time.sleep(2)
            continue  # ask again

        if data["has_voted"]:
            display("Already Voted", "")
            print(f"? {voter_name} has already voted.")
            time.sleep(2)
            continue  # ask again

        voter_address = data.get("address")
        if not voter_address:
            display("No Address", "")
            print(f"? No Ethereum address for {voter_name}.")
            time.sleep(2)
            continue

        # Candidate selection
        display(f"Welcome {voter_name}", "Select Candidate")
        candidate = None
        while True:
            if GPIO.input(BTN1) == GPIO.HIGH:
                candidate = "Candidate 1"
                display("Selected:", candidate)
            elif GPIO.input(BTN2) == GPIO.HIGH:
                candidate = "Candidate 2"
                display("Selected:", candidate)
            elif GPIO.input(BTN3) == GPIO.HIGH:
                candidate = "Candidate 3"
                display("Selected:", candidate)

            if candidate and GPIO.input(BTN4) == GPIO.HIGH:
                display("Vote Confirmed", candidate)
                print(f"? {voter_name} voted for {candidate}")
                break
            time.sleep(0.2)

        # Blockchain transaction
        try:
            tx = contract.functions.vote(candidate).transact({'from': voter_address})
            tx_hash = w3.to_hex(tx)
            display("Vote Sent!", candidate)
            print(f"? Vote recorded on blockchain. TX hash: {tx_hash}")
        except Exception as e:
            display("Vote Failed", "")
            print("? Blockchain error:", e)
            time.sleep(2)
            continue  # go back for next voter

        # Mark as voted locally
        voter_list[voter_name]["has_voted"] = True
        save_voter_list()
        display("Thank You!", "")
        print(f"?? {voter_name}'s vote recorded successfully.")
        time.sleep(3)

        # After each vote, system ready again
        display("Next Voter", "Place Finger")
        print("\n----------------------------------------\n")

except KeyboardInterrupt:
    display("Interrupted!", "")
    save_voter_list()
    print("\n?? Voting process terminated by user.")

finally:
    GPIO.cleanup()
    display("Program Ended", "")
