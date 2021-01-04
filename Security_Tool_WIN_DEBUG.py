import socket
import threading
import ipaddress
import subprocess
from queue import Queue
import time
import telnetlib
import paramiko # paramiko==2.7.2
import re
import numpy as np # numpy==1.19.3
# -------------------------------------------------------------------------------------------------------------------------------------
#   VERSION      AUTHOR        DATE          DESCRIPTION                             Email
#   1.12Debug    Shaun Craig    10/02/2018    Finished Program For Dissertations     s.craig@2014.ljmu.ac.uk
#
#   1.3         Shaun craig     04/01/2021  Wow, after looking again at this, I've
#                                           made so many mistakes, fixed a few
#                                           and made it nicer, uploading to github   releasedcookie@gmail.com
#
#                                                   Project! Could do GUI
#
# -------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------ VARIABLES -------------------------------------------------------
ShortestTime = []
PasswordPosition = []
SSHHosts = []
TelnetHosts = []
print_lock = threading.Lock()
vulnerabilities_counter = 0
Host_Count = 0
AttackTime = []

# ------------------------------------------------------ TELNET ATTACK CODE ---------------------------------------------------------
def telnet_attack(tn, user, password):
    # ************************************** Connects to host
    print("CHECKING THIS USERNAME: ", user)
    print("CHECKING THIS PASSWORD: ", password)
    # ***************************************** trys username
    try:
        tn.read_until(b"login: ")
    except EOFError:
        print("Read Login Failed")
    try:
        tn.write(user.encode('ascii') + b"\n")
    except socket.error:
        print("error failed to write username")
    # ******************************************* trys password
    try:
        tn.read_until(b"Password:")
    except EOFError:
        print("Read password part Failed")
    try:
        tn.write(password.encode('ascii') + b"\n")
    except socket.error:
        print("password failed to write")

# ------------------------------------------------------ TELENET PICKING CODE ----------------------------------------------------------
def runTelnetAttack(host):
    passwordtrys = 0
    TelnetAttackTime = time.time()  # Time test
    PasswordFound = False
    # --------------- open username and password lists
    passwordlist = open("wordlist.txt", "r")
    usernames = open("userlist.txt", "r")
    usernames = usernames.readlines()
    passwords = passwordlist.readlines()

    for user in usernames:
        user = user.strip()
        for pwd in passwords:
            tn = telnetlib.Telnet(host)
            password = pwd.strip()
            print("CHECKING THIS HOST: ", host)
            telnet_attack(tn, user, password)

            passwordtrys = passwordtrys + 1
            # -------------------------------------------------- PASSWORD CHECKER, IF INCORRECT IS IN THE CHECK
            # print(Check, "----------------------------------------")           # DEBUG THE READ EAGER LINE
            Check = (str(tn.read_very_eager()))
            while ("b" in Check):
                if ("incorrect" in Check):
                    print("--------------------------------- Incorrect Password")
                    PasswordFound = False
                    break
                elif ("@" in Check):
                    print("********************************* PASSWORD ACTUALLY FOUND!!!!!!!!!!!!")
                    PasswordFound = True
                    break  # if found, jump out of for loop
                else:
                    # print("********************************* Having Trouble Trying !!!!!!!!!!!!")
                    PasswordFound = False
                Check = (str(tn.read_very_eager()))
            if PasswordFound == True:
                break
        if PasswordFound == True:
            break

    if PasswordFound == False:
        print("------------------------- Password Was Not Found ------------------------- ")
        print("TELNET ATTACK TIME WAS:", time.time() - TelnetAttackTime, 'Seconds')
    else:
        print(" -------------------------  PASSWORD IS", password,  "------------------------- ")
        print("TELNET ATTACK TIME WAS:", time.time() - TelnetAttackTime, 'Seconds')
        AttackTime.append([time.time() - TelnetAttackTime, host])
        PasswordPosition.append(passwordtrys)

    # usernames.close()
    passwordlist.close()

# ------------------------------------------------------ SSH ATTACK  ------------------------------------------------------
def run_SSH_ATTACK(host):
    PasswordFound = False
    passwordtrys = 0
    SSHAttackTime = time.time()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    passwordlist = open("wordlist.txt", "r")
    usernames = open("userlist.txt", "r")

    usernames = usernames.readlines()
    passwords = passwordlist.readlines()
    for user in usernames:
        user = user.strip()
        passwordtrys = 0
        for pwd in passwords:
            password = pwd.strip()
            passwordtrys = passwordtrys + 1
            print("CHECKING THIS IP ADDRESS: ", host)
            print("CHECKING THIS USERNAME: ", user)
            print("CHECKING THIS PASSWORD: ", password)
            try:
                ssh.connect(host, username=user, password=password)
            except paramiko.ssh_exception.AuthenticationException:
                print("--------------------------------- Incorrect Password")
                pass
            except EOFError:
                print(" --------------------------------- Having Trouble Trying ")
            else:
                print("********************************* PASSWORD ACTUALLY FOUND!!!!!!!!!!!!")
                PasswordFound = True
                break
            ssh.close()
        if PasswordFound == True:
            break

    if PasswordFound == False:
        print("------------------------- Password Was Not Found ------------------------- ")
        print("SSH ATTACK TIME WAS:", time.time() - SSHAttackTime, 'Seconds')
    else:
        print("-------------------------  PASSWORD IS", password, "------------------------- ")
        AttackTime.append([time.time() - SSHAttackTime, host])
        PasswordPosition.append(passwordtrys)
        print("SSH ATTACK TIME WAS:", time.time() - SSHAttackTime, 'Seconds')
    #usernames.close()
    passwordlist.close()

# ------------------------------------- Begin Brute Force Attacks / Testing the hosts on the network  -----------------------------------------
def Dictonary_Attack():
    for Target in ([IPAddress[0] for IPAddress in TelnetHosts]):
        print("Testing", Target + "'s Telnet Port...")
        runTelnetAttack(Target)

    for Target in ([IPAddress[0] for IPAddress in SSHHosts]):
        print("Testing", Target + "'s SSH Port...")
        run_SSH_ATTACK(Target)
    NetworkScoreAlgorithm()

# ------------------------------------------------------ Network Scoring Algorithm  ------------------------------------------------------
def NetworkScoreAlgorithm():
    if not AttackTime:
        print('***************************************************************************************')
        print("Network password score would be 0")
        print("The Lower The Score The More Secure The Network")
        print("CONGRATULATIONS YOUR NETWORK IS SECURE ACCORDING TO THIS APPLICATION")
        # ********************************************** Smallest Attack Time ***********************************/
    else:
        counter = 0
        for Timewise in ([Time[0] for Time in AttackTime]):
            ShortestTime.append(Timewise)
            ST = min(ShortestTime)
        print("Shortest Time is ", ST)
        # ********************************************** Weakest IP Address ***********************************/
        for WeakestHost in ([Time[0] for Time in AttackTime]):
            if AttackTime[counter][0] == ST:
                WeakestIPAddress = AttackTime[counter][1]
                break
            counter = counter + 1
        ("Weakest IP Address Target is ", WeakestIPAddress)
        # ********************************************** Weakest IP addresses PING ***********************************/
        # ********************** Telnet Checking
        counter2 = 0
        for WeakHostSearch in ([Time[0] for Time in TelnetHosts]):
            if TelnetHosts[counter2][0] == WeakestIPAddress:
                ping = TelnetHosts[counter2][1]
            else:
                counter2 = counter2 + 1
        # ********************** SSH Checking
        counter2 = 0
        for WeakHostSearch in ([Time[0] for Time in SSHHosts]):
            if SSHHosts[counter2][0] == WeakestIPAddress:
                ping = SSHHosts[counter2][1]
            else:
                counter2 = counter2 + 1
        print('***************************************************************************************')
        print("The Weakest IP Address is ", WeakestIPAddress, "with a ping of", ping, "which was attacked in ", ST,
              "Seconds")
     # ********************************************************************* Calculation
        FastestTime = ST
        PasswordPlace = min(PasswordPosition)

        VulnStat = (vulnerabilities_counter / Host_Count * 100)
        print("Networks Vulnerability Score: ", VulnStat)

        ping = ping / 100
        PassPosScore = PasswordPlace ** -0.5
        TimeWPing = FastestTime ** (-ping - 0.25)

        print("PASSWORD POSSITION SCORE: ", PassPosScore)
        print("TIME WITH PING SCORE: ", TimeWPing)
        CombScore = ((PassPosScore + TimeWPing) / 2) * 100
        print("OVERALL PASSWORD SCORE: ", CombScore)

        FinalScore = (VulnStat + CombScore) / 2

        print("Network password score would be ", FinalScore)
        print("The Lower The Score The More Secure The Network")
        print('***************************************************************************************')
        if 0 < FinalScore <= 50:
            print("0 and 50")
            print("Your password management is good but you still have passwords on the top 100 list.")
            print("Create harder to crack passwords by using numbers, capital letters and punctuation.")
            print("Passphrases are harder to crack and sometimes easier to remember, try experimenting.")
            print("Try using a password manager to store more complicated passwords.")
        elif 50 < FinalScore <= 100:
            print("50 and 100")
            print("Your password management is alright but you still have passwords on the top 100 list.")
            print("Create harder to crack passwords by using numbers, capital letters and punctuation.")
            print("Passphrases are harder to crack and sometimes easier to remember, try experimenting.")
            print("Try using a password manager to store more complicated passwords.")
        elif 100 < FinalScore <= 200:
            print("100 and 200")
            print("Your password management is bad!")
            print("Create harder to crack passwords by using numbers, capital letters and punctuation.")
            print("Passphrases are harder to crack and sometimes easier to remember, try experimenting.")
            print("Try using a password manager to store more complicated passwords.")
        elif FinalScore > 200:
            print("200 and 300")
            print("Your password management is SHOCKING!!! You may already have been hacked!!!")
            print("Create harder to crack passwords by using numbers, capital letters and punctuation.")
            print("Passphrases are harder to crack and sometimes easier to remember, try experimenting.")
            print("Try using a password manager to store more complicated passwords.")

    print('***************************************************************************************')


#******************************************************* Picking of Target Network **********************************************************/
# Gets the hostname and IP address of current machine
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)

# Converts IP address to /24 subnet
IPEdit = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.',IPAddr)
network_submask = str(IPEdit[0]) + "0/24"

# Asks user if they want to change subnet?
picked_network_submask = input("Your network Submask is " + network_submask + " Click enter to scan this submask OR type a new mask for example 192.168.1.0/24:") # let this line live at end of project
if picked_network_submask == "":
    picked_network_submask = network_submask

# Get all of the hosts from the subnet and starts to Scan
ip_net = ipaddress.ip_network(network_submask) #change IP too network_submask later
print("Scanning IP Range" , network_submask + "...                   (This May Take Some Time)")
StartTime = time.time() # Time test
All_Hosts = list(ip_net.hosts())  #selects all hosts from the sub-mask

#******************************************************* Scans Target Network **********************************************************/
for i in range(len(All_Hosts)):
    output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(All_Hosts[i])], stdout=subprocess.PIPE).communicate()[0]

    if "Destination host unreachable" in output.decode('utf-8'):
        # pass
        print(str(All_Hosts[i]), "is Offline")
    elif "Request timed out" in output.decode('utf-8'):
        # pass
        print(str(All_Hosts[i]), "is Offline")
    else:
        print(str(All_Hosts[i]), "is Online")
        output2 = subprocess.check_output("ping " + str(All_Hosts[i]), shell=False,universal_newlines=True).splitlines()
        Host_Count = (Host_Count + 1)
        Up_Host = str(All_Hosts[i])
        for b in output2:
            if "Packets" in b:
                PckLoss = int(re.search(r'\d+', str(re.findall(r'Lost =\s\d*',b))).group())
                print("Packet lost: " + str(PckLoss))
            if "Minimum" in b:
                AvgPing = int(re.search(r'\d+', str(re.findall(r'Average =\s\d*',b))).group())
                print("Packet Average: " + str(AvgPing))
#*************************************************** IF HOST UP THEN SCAN PORTS ****************************************/
        def portscan(port):
            s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print(" -- Scanning ", port , " On Host: ", Up_Host)

            try:
                con = s.connect((Up_Host,port))
                print(con)
                with print_lock:
                    global vulnerabilities_counter
                    vulnerabilities_counter = (vulnerabilities_counter + 1)
                    print('IP Address',Up_Host,'***** Port',port,'is open')
                    if (port == 23):
                        TelnetHosts.append([Up_Host, AvgPing])
                    if (port == 22):
                        SSHHosts.append([Up_Host, AvgPing])
                con.close()
            except:
                # print('IP Address', Up_Host, '***** Port', port, 'is closed')
                pass


# *************************************************** SPEEDS UP SCANNING WITH THREADING ***************************************
        def threader():
                while True:
                    worker = q.get()
                    portscan(worker)
                    q.task_done() #finish

        q = Queue()
# ************************************ Uses a worker per port *********

        for x in range (20): # how many processes it runs at the same time LOWER FOR LOWER CPUs
            t = threading.Thread(target=threader) # target is Up_Host
            t.daemon # dies when thread dies
            t.start() # starts next thread

        for worker in range (22,24):
            q.put(worker)

        q.join()
#********************************************************** RESULT INFORMATION TEXT *********************************************************************

print('***************************************************************************************')
print('You have ', Host_Count, 'Hosts online')
print('You have ', vulnerabilities_counter, 'vulnerabilities in your network')
print('----------')
print('Time taken to run is', time.time()-StartTime, 'Seconds')
print('----------')


# ------------------------------------------------------ ETHIC PERMISSION PART
if vulnerabilities_counter > 0:
    ActiveSSHHosts = np.array(SSHHosts)
    ActiveTelnetHosts = np.array(TelnetHosts)
    if SSHHosts:
        print("Hosts with Port 22 Open that are susceptible to attack: ", ActiveSSHHosts[:, 0])
    if TelnetHosts:
        print("Hosts with Port 23 Open that are susceptible to attack: ", ActiveTelnetHosts[:, 0])
    print("-------------------------------------------------------------------------------------------------------------------")
    print("Dictionary attacking to provide password strenth statistics requires Ethical Approval")
    print("Ethical Approval can only come from the person who owns the network")
    Ethical = (input("Does this program have permission to dictionary attack the network? (Yes or No): "))
    if Ethical.lower() == "yes":
        print('***************************************************************************************')
        Dictonary_Attack()
    else:
        print("------ Value entered was not 'Yes' therefore program is terminating -------")
print("-------------------------------------------------------------------------------------------------------------------")
print('PROGRAM FINISHED - Run Time:', time.time() - StartTime)
