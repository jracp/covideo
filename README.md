---
title: "covideo"
authors: "Javad Rahimipour Anaraki"
date: '14/04/20'
---

# Covideo [![DOI](https://zenodo.org/badge/252190187.svg)](https://zenodo.org/badge/latestdoi/252190187)
Covideo (see Figure 1) is an application designed to monitor inner canthus temperature actively, as instructed in [IEC 80601-2-59](https://www.iso.org/standard/69346.html), based on the thermal images captured using [FLIR Systems](https://www.flir.ca/) [ThermaCAM SC640](https://www.photonicsonline.com/doc/thermacam-sc640-0001) camera. For more info, please refer to **Covideo.pdf**. Both MATLAB and Python versions are available.

## Requirements
Here is a list of minimum requirements for MATLAB version:
 - MATLAB 2014
 - LabView 2010
 - ThermaCAM SC640 or similar
 
 Here is a list of minimum requirements for Python version:
 - Opencv [download](https://pypi.org/project/opencv-python/)
 - LabView 2010
 - ThermaCAM SC640 or similar

## Introduction
In the top position of the application, there are two numbers, one in red and the other one in blue, which represents the maximum and the average temperature of inner canthus, respectively. The white section in the middle shows the subject thermal image and the detected area when computing is done.  The green led at the button indicates that the subject has a normal temperature. In the case of detecting equal and higher than 38, the LED goes red, and a pop-up message will appear. When the application detects a subject and calculates max and average temperatures, the process holds the process for 10 seconds to let the information being recorded, if necessary, by the operator. The timeout is visualized using the gauge located at the bottom part of the application. The live button initiates the process and the stop button interrupts the process. 

![Figure 1](/images/Covideo.png)

*Figure 1: Covideo application*

To set up the hardware and software, please follow each step carefully. Otherwise, the accuracy and applicability of the application could be affected.

## Hardware setup 
 1. Fix the thermal camera on a tripod and adjust it at least 75cm from ground and 150cm from the subject
 2. Connect the thermal camera to an outlet
 3. Connect the FireWire cable to the back of the camera by removing the gray cap
 4.	Connect the other end of FireWire to the lower back of the PC
 5.	Turn on the thermal camera
 6.	Adjust the focus using the button located on the right side of the camera
 
## Software setup
 1. Download the code and copy that into a folder called **covideo** in C drive
 2.	Open the folder
 3.	Locate **Thermal.vi** file and open it (**Note**: The **Thermal.vi** can be edited to work with different thermal camera)
 4.	When LabView is opened, click on the *Run* button
 5.	Go back to **covideo** folder and double click on **Covideo.exe**
 6.	To start screening, click on the *Live* button as shown in Figure 2
 7.	After capturing the picture, the application starts processing and locating the inner canthus of the subject. When finished, the outcome is shown as illustrated in Figure 3
 
![Figure 2](/images/Initialized.png)

*Figure 2: Initialized thermal image*

![Figure 3](/images/Detected.png)

*Figure 3: Detected inner canthus and temperatures*
