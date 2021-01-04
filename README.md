# home-network-security-tool
This is a easy to use quick security tool to check the hosts on your network for obvious vulnerabilities

This was dissertation project I created back in 2017/2018. I'd love to assure you that even though this code does run, I am a much better coder now. You can check out my dissertation called ["The investigation into IoT Security and Credential Management" here](https://drive.google.com/file/d/1g9ITfKl4SnVJKctgFr_E-rjV_ydnuF1Z/view?usp=sharing)

## Tl;Dr

The Mirai botnet shook the world when the botnet took down significant sites like Twitter, Netflix, CNN and many more. This botnet was propagated by exploiting the vulnerabilities of human password creation and looked for weak password strength in Internet-enabled devices. [In a survey conducted by TeleSign in 2015](https://www.entrepreneur.com/article/246902), 21% of users said that they had not changed their password in over ten years and with 20.5 billion IoT devices predicted to be connected to the internet in 3 years this heightens a massive problem in the Internet of Things era. This simple tool will check all of your devices on your network for open ports 22/23 and try a list of the top 100 passwords to try and break in to test if your network is susceptible to a botnet takeover.

# Windows
### Install Python 3
To download on windows machines, make sure you have python3 installed, you can download python from here https://www.python.org/downloads/
This version of the network security tool was built using python 3.9.1

To confirm you have python installed you should be able to type "python" into a Command prompt which would activate python, like shown below;

![Python in Command Line](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/Python_CMD.PNG?raw=true)

### Install Prerequisite Python Packages
Once Python is installed we can use ["Pip"](https://pypi.org/project/pip/) to install our Prerequisites. Open a Command Prompt and run the two commands below
```
pip install paramiko
pip install tqdm
pip install numpy==1.19.3
```

For Numpy, it will suggest a later Package however due to a [Windows Issue](https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html) a later package will error out.

It should look a lot like the picture below;

![Installing Numpy using Pip](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/pip_install.PNG?raw=true)

### Install and Run The Home Network Security tool
To install the Home Network Security tool visit this github and click the "Code" in the top right hand side of this page and click `Download ZIP` like shown below

![Downloading the ZIP File from Github](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/download_zip.PNG?raw=true)

Once downloaded, find the folder in your downloads and extract the Zip file using your favourite ZIP tool.
Once extracted take not of the files location, then open another Command Prompt and type `cd [Your/Files/Location]` like shown below;

![CMD where is file](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/files_location.PNG?raw=true)

Once there, type `python ./Security_Tool_WIN_PROD.py` to run the program :)
