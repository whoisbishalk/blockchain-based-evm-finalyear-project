#Blockchain-Based EVM – Final Year Project#

This repository contains the source code for my final year project for the Bachelor of Information Technology (Hons) program.

The goal of this project is to demonstrate a secure electronic voting system using Blockchain (Ethereum Virtual Machine – EVM) to ensure transparency, immutability, and trust in the voting process.

🛠️ Technologies Used

Ethereum Blockchain (EVM)
Solidity – Smart contract development
Python (Web3.py) – Blockchain interaction
Ganache – Local Ethereum blockchain
Truffle – Smart contract compilation and deployment

#Hardware Componrnts:

Raspberry Pi – Hardware integration
Fingerprint Sensor – Voter authentication
I2C LCD Display & Capacitive Touch Button – User interface components
Capacitive Touch Button - input buttons
Female 2 Female Jumper Wire- For Wiring

Connection Details:
LCD Module
LCD ||Pin	Raspberry Pi Pin	Pin Number
GND	||Ground	Pin 6
VCC	||5V Power	Pin 4
SDA	||GPIO2 (I2C SDA)	Pin 3
SCL	||GPIO3 (I2C SCL)	Pin 5

#Capactive Touch Btn
Touch Button Pin ||	Raspberry Pi Pin	|| Pin Number
VCC	             || 3.3V Power	      ||Pin 1
GND	             ||Ground	            ||Pin 9
BTN1             || GPIO17	          ||Pin 11
BTN2             ||	GPIO27	          ||Pin 13
BTN3             ||	GPIO22	          ||Pin 15
BTN4             ||	GPIO23	          ||Pin 16


#Fingerprint Module
Fingerprint Scanner || Pin	Raspberry Pi Pin	|| Pin Number
TX	                   RX (GPIO15)	             Pin 10
RX	                   TX (GPIO14)	             Pin 8
GND	                   Ground	                   Pin 20
VCC	                   3.3V Power	               Pin 17


How to run the project?
1. Clone the repository:
git clone https://github.com/whoisbishalk/blockchain-based-evm-finalyear-project


2. Install dependencies:
Node.js & Truffle
Ganache
Python packages (web3, etc... look at the codes)

3. Start Ganache (local blockchain)
4. Choose Your IP:
5. Insert your gansche IP in vote.py and voter_enroll.py 
4. Compile and deploy smart contracts:
    truffle compile
    truffle migrate
5. You would get contract address copy it and place it in vote.py
6. Run voter_enroll.py to enroll voters.
7. Run vote.py for election
8. index.html to view result //Replace IP in this code too
9: explorer.html to view blockchain trx.

Thank Youuuu!
Final Year report would be uploaded here, once it's been approved by Project supervisor. 









