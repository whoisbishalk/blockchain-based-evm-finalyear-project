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

![image alt](https://github.com/whoisbishalk/blockchain-based-evm-finalyear-project/blob/main/connection1.png?raw=true)
![image alt](https://github.com/whoisbishalk/blockchain-based-evm-finalyear-project/blob/main/connection2.png?raw=true)


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


Added: Here's the full final year report 









