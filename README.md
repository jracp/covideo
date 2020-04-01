# Covideo
Covideo is an application designed to monitor inner canthus temperature actively, as instructed in [IEC 80601-2-59](https://www.iso.org/standard/69346.html), based on the thermal images captured using [FLIR Systems](https://www.flir.ca/) [ThermaCAM SC640](https://www.photonicsonline.com/doc/thermacam-sc640-0001) camera.

## Requirements
Here is a list of minimum requirements:
 - MATLAB 2014
 - LabView 2010
 - ThermaCAM SC640 or similar

In the top position of the application, there are two numbers, one in red and the other one in blue, which represents the maximum and the average temperature of inner canthus, respectively. The white section in the middle shows the subject thermal image and the detected area when computing is done.  The green led at the button indicates that the subject has a normal temperature. In the case of detecting equal and higher than 38, the LED goes red, and a pop-up message will appear. When the application detects a subject and calculates max and average temperatures, the process holds the process for 10 seconds to let the information being recorded, if necessary, by the operator. The timeout is visualized using the gauge located at the bottom part of the application. The live button initiates the process and the stop button interrupts the process. 

![Covideo](/images/Covideo.png) Covideo application

## Step 0
Open terminal using either (Ctrl + Alt + t) or *Search* and type in **terminal** and then hit *Enter*

## Step 1
Copy-and-paste the following commands into **terminal**, one at a time, and then hit *Enter*
```
sudo apt-get install -y default-jre
sudo apt-get install -y default-jdk
sudo R CMD javareconf
```
 
## Step 2
Open RStudio or R and copy-and-paste the following command into console and hit *Enter*
```
install.packages("rJava")
```
 
## Step 3
Copy-and-paste the following command to check the current version of Java on your machine
```
java -version
```
 
If the output values are less the ones in the following, go to **Step 4**, otherwise, go to **Step 5** 
```
openjdk version "1.8.0_171"
OpenJDK Runtime Environment (build 1.8.0_171-8u171-b11-2~14.04-b11)
OpenJDK 64-Bit Server VM (build 25.171-b11, mixed mode)
```

## Step 4 
RWeka requires at least Java version 8, copy-and-paste the following commands into **terminal**, one at a time, to install the required version
```
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```
In order to let R use the correct version of Java, copy-and-paste the following commands into **terminal**, one at a time, and hit *Enter* to change the default version of Java
```
sudo update-alternatives --config java
sudo update-alternatives --config javac
```
**Note:** For both choose openjdk-8-jdk
 
## Step 5
Now the system is ready to install the last set of requirements through **terminal**. Copy-and-paste the following commands into **terminal**, one at a time, and hit *Enter*
```
sudo apt-get install r-cran-rjava
sudo apt-get install libgdal-dev libproj-dev
R CMD javareconf -e
``` 
**Note:** If the Java version is still outdated after running ```R CMD javareconf -e```, then run 
```sudo R CMD javareconf JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64``` and hit *Enter*

## Step 6
Now, go back to RStudio or R and copy-and-paste the following command into console and hit *Enter*
```
install.packages("RWeka")
```

# More info
Check the following references for further information
 - [Installing BLAS and LAPACK packages](https://askubuntu.com/questions/623578/installing-blas-and-lapack-packages)
 - [Installing OpenJDK on Debian-based systems](https://docs.datastax.com/en/cassandra/3.0/cassandra/install/installOpenJdkDeb.html)
 - [Installing R](https://www.ibm.com/support/knowledgecenter/en/SSPT3X_3.0.0/com.ibm.swg.im.infosphere.biginsights.install.doc/doc/install_install_r.html)
 - [Installing RJava (Ubuntu)](https://github.com/hannarud/r-best-practices/wiki/Installing-RJava-(Ubuntu))
 - [rJava is not picking up the correct Java version](https://stackoverflow.com/questions/28133360/rjava-is-not-picking-up-the-correct-java-version)
