# # Programmed by Javad Rahimipour Anaraki on 2020.04.14
# # Postdoctoral Fellow
# # PRISM Lab, Bloorview Research Institute
# # Holland Bloorview Kids Rehabilitation Hospital
# # jrahimipour [AT] hollandbloorview [DOT] ca | http://individual.utoronto.ca/jrahimipour/
#
# """
# from typing import Union

import constants
import sys
from PySide2.QtWidgets import (QLabel, QPushButton, QApplication,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QMainWindow, QComboBox, QDialog, QMessageBox)
from PySide2 import QtGui, QtCore, Qt
from PySide2.QtGui import QPixmap
import threading
import cv2
import csv
import numpy


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Stop flag
        self.stopFlag = False

        # Load the GUI
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle(constants.title)
        # self.setFixedWidth(471)
        # self.setFixedHeight(460)
        # self.setFixedWidth(680)
        # self.setFixedHeight(680)

        # Temperature
        self.temp = QLabel("Temperatures")
        Palette = QtGui.QPalette()

        Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.red)
        self.maxTempLabel = QLabel("Max Temperature")
        self.maxTemp = QLineEdit("00.00")
        self.maxTemp.setEnabled(False)
        self.maxTemp.setPalette(Palette)

        Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.darkGreen)
        self.avgTempLabel = QLabel("Average Temperature")
        self.avgTemp = QLineEdit("00.00")
        self.avgTemp.setEnabled(False)
        self.avgTemp.setPalette(Palette)

        # Image
        self.image = QLabel()
        # self.image.setFixedWidth(391)
        # self.image.setFixedHeight(305)

        # Live / Stop
        self.live = QPushButton("Live")
        self.live.setFixedWidth(200)
        self.live.setFixedHeight(45)
        self.live.clicked.connect(lambda: self.__live())

        self.stop = QPushButton("Stop")
        self.stop.setFixedWidth(200)
        self.stop.setFixedHeight(45)
        self.stop.setEnabled(False)
        self.stop.clicked.connect(lambda: self.__stop())


        # # Create layout and add widgets
        parentLayout = QVBoxLayout()

        #Temp layout
        tempWidget = QWidget()
        tempLayout = QHBoxLayout()
        tempWidget.setLayout(tempLayout)

        maxTempWidget = QWidget()
        maxTempLayout = QHBoxLayout()
        maxTempLayout.addWidget(self.maxTempLabel)
        maxTempLayout.addWidget(self.maxTemp)
        maxTempWidget.setLayout(maxTempLayout)
        tempLayout.addWidget(maxTempWidget)

        avgTempWidget = QWidget()
        avgTempLayout = QHBoxLayout()
        avgTempLayout.addWidget(self.avgTempLabel)
        avgTempLayout.addWidget(self.avgTemp)
        avgTempWidget.setLayout(avgTempLayout)
        tempLayout.addWidget(avgTempWidget)
        parentLayout.addWidget(tempWidget)

        # Image
        imageWidget = QWidget()
        imageLayout = QHBoxLayout()
        imageLayout.addWidget(self.image)
        imageWidget.setLayout(imageLayout)
        parentLayout.addWidget(imageWidget)

        # Buttons
        startWidget = QWidget()
        startLayout = QHBoxLayout()
        startLayout.addWidget(self.live)
        startLayout.addWidget(self.stop)
        startWidget.setLayout(startLayout)
        parentLayout.addWidget(startWidget)

        # Set dialog layout
        widget = QWidget()
        widget.setLayout(parentLayout)
        self.setCentralWidget(widget)
        self.show()

    def __live(self):
        self.live.setEnabled(False)
        self.stop.setEnabled(True)

        self.liveStart = threading.Thread(target=self.__goLive)
        self.liveStart.start()

    def __goLive(self):

        # Load face classifier
        face_cascade = cv2.CascadeClassifier(constants.path)

        if constants.source == "file":
            while True:
                if self.stopFlag:
                    break
                else:

                    with open(constants.tempFileName, 'r') as f:
                        THRImage = list(csv.reader(f, delimiter=','))
                    temp = numpy.float_(THRImage) - 273.15
                    THRImage = numpy.asarray(numpy.float_(THRImage))

                    if THRImage.shape[0] < 480:
                        continue

                    gray = numpy.uint8(numpy.absolute(self.__mat2gray(THRImage) * 255))
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    if len(faces) == 0:
                        continue
                    x, y, w, h = faces[0]

                    xCentre = int(x + (w / 2))
                    yCentre = int(y + (h / 2))
                    canthus = (xCentre - constants.canthusX + constants.offsetX, yCentre - constants.canthusY + constants.offsetY, constants.canthusW, constants.canthusH)
                    x, y, w, h = canthus
                    cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    canthusTemp = temp[x:(x + w), y:(y + h)]
                    self.maxTemp.setText(str(constants.floatFormat.format(numpy.amax(canthusTemp))))
                    self.avgTemp.setText(str(constants.floatFormat.format(numpy.sum(canthusTemp) / (w * h))))

                    image = QtGui.QImage(gray, gray.shape[1], gray.shape[0], QtGui.QImage.Format_Grayscale8)
                    self.image.setPixmap(QPixmap.fromImage(image))
        else:
            # Initialize cameras
            self.RGBCam = cv2.VideoCapture(0)
            # self.THRCam = cv2.VideoCapture(1)

            while True:
                if self.stopFlag:
                    self.RGBCam.release()
                    # self.THRCam.release()
                    break
                else:
                    RGBImage = self.RGBCam.read()
                    gray = cv2.cvtColor(RGBImage[1], cv2.COLOR_RGB2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    if len(faces) == 0:
                        continue
                    x, y, w, h = faces[0]

                    xCentre = int(x + (w / 2))
                    yCentre = int(y + (h / 2))
                    canthus = (xCentre - constants.canthusX, yCentre - constants.canthusY, constants.canthusW, constants.canthusH)
                    x, y, w, h = canthus
                    cv2.rectangle(RGBImage[1], (x, y), (x + w, y + h), (255, 0, 0), 2)
                    canthusTemp = RGBImage[1]
                    canthusTemp = canthusTemp[x:(x + w), y:(y + h)]
                    self.maxTemp.setText(str(constants.floatFormat.format(numpy.amax(canthusTemp))))
                    self.avgTemp.setText(str(constants.floatFormat.format(numpy.sum(canthusTemp) / (w * h))))

                    image = QtGui.QImage(RGBImage[1], RGBImage[1].shape[1], RGBImage[1].shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                    image = image.mirrored(True, False)
                    self.image.setPixmap(QPixmap.fromImage(image))


        self.stopFlag = False

    def __stop(self):
        self.live.setEnabled(True)
        self.stop.setEnabled(False)
        self.stopFlag = True

    def __mat2gray(self, image):
        A = numpy.double(image)
        out = numpy.zeros(A.shape, numpy.double)
        normalized = cv2.normalize(A, out, 1.0, 0.0, cv2.NORM_MINMAX)
        return normalized

    # Messagebox
    def __message(self, type, value):
        msg = QMessageBox()
        msg.setIcon(type)
        msg.setText(value)
        msg.setWindowTitle(constants.title)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    window = MainWindow()

    # Run the main Qt loop
    sys.exit(app.exec_())