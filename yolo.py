# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yolo.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import cv2 as cv
import os

class Ui_MainWindow(object):

    def __init__(self):
        self.video_key = True
        self.video_detected = False

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(213, 358)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/1_bSLNlG7crv-p-m4LVYYk3Q.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.play_button = QtWidgets.QToolButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(20, 120, 71, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/29-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_button.setIcon(icon1)
        self.play_button.setObjectName("play_button")
        self.play_button.clicked.connect(self.play)

        self.stop_button = QtWidgets.QToolButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(110, 120, 71, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/download.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_button.setIcon(icon2)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop)

        self.start_detection = QtWidgets.QToolButton(self.centralwidget)
        self.start_detection.setGeometry(QtCore.QRect(30, 20, 141, 31))
        self.start_detection.setObjectName("start_detection")
        self.start_detection.clicked.connect(self.detect)

        self.start_video_stream = QtWidgets.QPushButton(self.centralwidget)
        self.start_video_stream.setGeometry(QtCore.QRect(30, 70, 141, 31))
        self.start_video_stream.setObjectName("start_video_stream")
        self.start_video_stream.clicked.connect(self.opcv_tread)

        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(0, 290, 211, 17))
        self.status_label.setObjectName("status_label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 213, 25))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionVideo = QtWidgets.QAction(MainWindow)
        self.actionVideo.setObjectName("actionVideo")
        self.actionVideo.triggered.connect(self.pick_video)

        self.actionWeight = QtWidgets.QAction(MainWindow)
        self.actionWeight.setObjectName("actionWeight")
        self.actionWeight.triggered.connect(self.pick_weight)

        self.menuFile.addAction(self.actionVideo)
        self.menuFile.addAction(self.actionWeight)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Car Detection"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.start_detection.setText(_translate("MainWindow", "Start Detection"))
        self.start_video_stream.setText(_translate("MainWindow", "Start video stream"))
        self.status_label.setText(_translate("MainWindow", ""))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionVideo.setText(_translate("MainWindow", "Video"))
        self.actionWeight.setText(_translate("MainWindow", "Weight"))


    def pick_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.video_file_name = QFileDialog.getOpenFileName(None, 'Open file', './')#setar filtros


    def pick_weight(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.weight_file_name = QFileDialog.getOpenFileName(None, 'Open file', './')#setar filtros

    def play(self):
        self.video_key = True

    def stop(self):
        self.video_key = False

    def detect(self):


        flag = os.system("cd darknet")
        if flag == 512:
            # mudar uma label na aplicaÃ§Ã£o informando que o diretorio nao foi encontrado
            print("darknet nÃ£o estÃ¡ no diretorio atual")
        else:

            video_pre = self.video_file_name[0]
            weight = self.weight_file_name[0]
            '''
            try:
                dot_data = input("darknet/cfg/coco.data")
                data = open(dot_data, 'r+')
                dot_names = input("darknet/cfg/yolov3.cfg")
                names = open(dot_names , 'r+')
            except FileNotFoundError:
                print("arquivo car.data nÃ£o encontrado")
                print("arquivo car.names nÃ£o encontrado")

            arquivo.close()
            '''

            os.system( "./darknet detector demo darknet/data/car.data darknet/cfg/yolov3.cfg "+ str(weight)+" "+ str(video_pre)+" -out_filename detect.avi -dont_show")#teste / funciona assim

            self.video_detected = "darknet/detect.avi"

            self.video_detected_flag()

    def video_detected_flag(self):
        video_detected = True

    def opcv_tread(self):

        if (not video_detected):
            cap = cv.VideoCapture(self.video_file_name[0])
        else:
            cap = cv.VideoCapture(self.video_detected)

        if cap.isOpened() == False:
            print("Error opening video file, try again")

        win = "Video Display"
        cv.namedWindow(win, cv.WINDOW_KEEPRATIO)
        cv.resizeWindow(win, 1058, 595)

        while True:
            ret, frame = cap.read()

            if (not ret):
                break

            if (not self.video_key):
                while True:

                    cv.imshow(win, frame)
                    cv.waitKey(10)
                    if (self.video_key):
                        break

            cv.imshow(win,frame)
            key = cv.waitKey(10) & 0xff
            if key == 27:
                break

        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
