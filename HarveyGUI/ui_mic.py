# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'miceQppuA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Load custom font from fonts directory
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "LexendDeca-VariableFont_wght.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.lexend_font_family = font_families[0]
                    print(f"Loaded font: {self.lexend_font_family}")
                else:
                    self.lexend_font_family = "Calibri"  # Fallback
                    print("Font loaded but no families found, using Calibri")
            else:
                self.lexend_font_family = "Calibri"  # Fallback
                print("Failed to load font, using Calibri")
        else:
            self.lexend_font_family = "Calibri"  # Fallback
            print(f"Font file not found at: {font_path}, using Calibri")

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        MainWindow.resize(1000, 600)
        self.centralwidget.setObjectName(u"centralwidget")
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(395, 200, 211, 211))  # Centered horizontally in 1000px window
        self.toolButton.setAutoFillBackground(False)
        self.toolButton.setStyleSheet(u"QToolButton {\n"
"    border-radius: 100px;   /* half of width/height \u2192 circle */\n"
"    border: none;\n"
"}\n"
"QToolButton:hover {\n"
"}\n"
"QToolButton:pressed {\n"
"}")
        icon = QIcon()
        icon.addFile(u"stars.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u"microphone.png", QSize(), QIcon.Normal, QIcon.On)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(200, 200))
        # Make the button checkable so it can toggle between On/Off states
        self.toolButton.setCheckable(True)
        self.toolButton.setChecked(False)  # Start in Off state

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 60, 900, 100))  # Much wider (50-950) and taller for wrapping
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)  # Enable text wrapping
        # Set Lexend Deca font for main label
        font = QFont()
        font.setFamily(self.lexend_font_family)
        font.setPointSize(14)
        self.label.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 2500, 22))  # Match window width
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toolButton.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"I'm Harvey, your personal digital assistant. How can I help you today?", None))
        self.label.setStyleSheet("color: #333333;"             
            "font-size: 24px;"
            "font-weight: bold;"
            "qproperty-alignment: AlignCenter;"
            "padding: 10px;")
