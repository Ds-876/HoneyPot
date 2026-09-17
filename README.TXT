Project Overview: WEB BASED HONEYPOT
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
We have two VMs Honeypot VM and Real VM
	1. Honeypot VM has the web honeypot hosted where everything is monitored. 
	2. Real VM has actual website hosted where only legitimate users are redirected.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SETUP.PY is the main setup file that creates 2 folders Honeypot_VM and Real_VM; 
Each VM file can be transferred to respective VMs 
Transfer realvm file to actual VM ( I have already transfered it)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This is the flow 

Traffic -> Honeypot VM first-> Master Logs are created-> Alert logs created in case anything is suspicious-> Email sent to security team-> Legitimate traffic sent to Real VM
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SETTING UP HONEYPOT VM

1.Run python3 setup.py to create both honeypot and real VM

Transfer Real_VM folder in another VM.

1.Move to Honeypot_VM Directory in Honeypot VM. 

2.Run python3 honeypot.py

This setup the honeypot on our VM, It prmopts to enter email for security team where the alert mail will be sent. 

It automatically creates the template folder with fake login page that looks same as real login page.

It creates master and alert log folders with log files which will be filled later with required details. 
You can see the web page is now hosted. 

The LOG file will be created later once some logs are created in backend.

----------------------------------------------------------------------------------------


This project demonstrates how a honeypot works in a virtualized Linux environment using VirtualBox.
A honeypot is a "security mechanism" designed to attract attackers and monitor their activities in order to understand attack methods and improve system security.
Instead of protecting real data, the honeypot acts as a decoy system.Any interaction with the honeypot is considered suspicious and is logged for analysis.

---
## Aim of the Project

* To understand how cyber attacks occur
* To study attacker behavior in a controlled environment
* To demonstrate intrusion detection using a honeypot
* To improve knowledge of network security concepts
---

## Tools & Technologies Used

* **VirtualBox** – For virtualization
* **Linux OS (Ubuntu/Kali)** – Honeypot environment
* **Honeypot Service** (e.g., SSH-based honeypot)
* **Terminal & Log Files** – For monitoring attacks
---
## How the Honeypot Works (Explanation)

1. The honeypot is installed on a Linux virtual machine.
2. It exposes fake vulnerable services such as SSH or Telnet, Brute Force.
3. When an attacker tries to connect:

   * The honeypot *allows interaction*
   * Records **IP address, commands, login attempts, Time-stamps *
4. No real system or data is harmed.
5. All attacker actions are **logged and analyzed**.

This helps security professionals understand:

* Common attack techniques
* Frequently used usernames/passwords
* Malicious command behavior
---

## Architecture Overview

Attacker System
       ↓
Virtual Network
       ↓
Linux VM (Honeypot)
       ↓
Log Files & Monitoring
---

# How to Use / Demonstration Steps

## Step 1: Create Virtual Machine

* Open **VirtualBox**
* Create a new VM
* Install **Linux OS** (Ubuntu/Kali)
* Configure network (NAT or Bridged)

SETTING UP REAM VM

1. Move to Real_VM Directory.
2. Run Python3 real.py
This will host the actual website where the legitimate traffic will be sent.


On honeypot we are trying test and test123 as user and pass which is incorrect. 
Since the test is not recorded user it flags as suspicious. 

Lets enter correct credential and check if it will take to actual website. Notice that honeypot runs on .2 IP and real website is on .3 IP


Correct creds are alice and Password123


Lets see master logger it logs all legitimate and malicious traffic but alert only has malicious logs | easier for security team to check

It detects that someone has attempted bruteforce with time and IP.
for other info like useragent one can check master log. 



## Step 5: Monitor Logs

* Open honeypot log files
* Observe:

  * IP addresses
  * Login attempts
  * Time Stamps, Browser, Versions
  * Commands entered by attacker

## Step 6: Analyze Data

* Study attacker behavior
* Identify attack patterns
* Understand security risks
---

## Output / Result

* Successful capture of attacker activity
* Logs showing unauthorized access attempts
* Demonstration of honeypot effectiveness

---

## Advantages of Honeypot

* Early attack detection
* No risk to real systems
* Detailed attacker analysis
* Improves security awareness

---

## Conclusion

This project successfully demonstrates the working of a **honeypot in a Linux virtual environment**. 
It shows how honeypots can be used as an effective tool for **intrusion detection and cyber security research**. 
The use of VirtualBox ensures safe testing without affecting real systems.
