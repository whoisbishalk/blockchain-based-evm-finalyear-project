#!/usr/bin/env python3
import json
from web3 import Web3

VOTER_FILE = "voter_list.json"
GANACHE_URL = "http://192.168.1.72:7545"  # update if needed

# ==============================
# Connect to Ganache
# ==============================
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
if not w3.is_connected():
    print("? Error: Cannot connect to Ganache! Check your RPC URL or network.")
    exit(1)

accounts = w3.eth.accounts
if not accounts:
    print("? No accounts found in Ganache. Run Ganache first.")
    exit(1)

print(f"? Connected to Ganache. Found {len(accounts)} available addresses.")

# ==============================
# Load voter list
# ==============================
try:
    with open(VOTER_FILE, "r") as f:
        voter_list = json.load(f)
except FileNotFoundError:
    print("? voter_list.json not found. Please run voter_enroll.py first.")
    exit(1)

# ==============================
# Assign new addresses
# ==============================
used_addresses = set()
addr_index = 0

for voter_name, data in voter_list.items():
    # Skip voters with existing new address if needed
    if addr_index >= len(accounts):
        print("?? Not enough Ganache accounts to assign all voters!")
        break

    new_addr = accounts[addr_index]
    voter_list[voter_name]["address"] = new_addr
    voter_list[voter_name]["has_voted"] = False  # reset for new election
    used_addresses.add(new_addr)
    print(f"? Updated {voter_name} ? {new_addr}")
    addr_index += 1

# ==============================
# Save updated voter list
# ==============================
with open(VOTER_FILE, "w") as f:
    json.dump(voter_list, f, indent=4)

print("\n?? All voter addresses updated successfully!")
print("??? Voting reset for new election.")
