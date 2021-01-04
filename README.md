# home-network-security-tool
This is a easy to use quick security tool to check the hosts on your network for obvious vulnerabilities

# Windows
### Install Python 3
To download on windows machines, make sure you have python3 installed, you can download python from here https://www.python.org/downloads/
This version of the network security tool was built using python 3.9.1

To confirm you have python installed you should be able to type "python" into a Command prompt which would activate python, like shown below;

![alt text](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/Python_CMD.PNG?raw=true)

### Install Prerequisite Python Packages
Once Python is installed we can use ["Pip"](https://pypi.org/project/pip/) to install our Prerequisites. Open a Command Prompt and run the two commands below
```
pip install paramiko
pip install numpy==1.19.3
```

For Numpy, it will suggest a later Package however due to a [Windows Issue](https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html) a later package will error out.

It should look a lot like the picture below

![alt text](https://github.com/Releasedcookie/home-network-security-tool/blob/main/Images/pip_install.PNG?raw=true

### Install The Home Network Security tool
