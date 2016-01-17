# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modisTrack_about_ui.ui'
#
# Created: Sat Jan 16 05:12:28 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(291, 300)
        Dialog.setMinimumSize(QtCore.QSize(291, 300))
        Dialog.setMaximumSize(QtCore.QSize(554, 383))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/modisTrackL1L2/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 271, 236))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.label.setText(_translate("Dialog", "MODIS Track L1 L2", None))
        self.label_2.setText(_translate("Dialog", "ver. 1.0", None))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:9pt;\">Modis Track L1 L2 Plugin</span></p><p>This module allows to create Terra/Aqua track at selected date as shapefile;\n"
"                   to create extents of scenes for all track points at day as shapefile;\n"
"                   to define needed scenes for user\'s vector layer.\n"
"Space-track.org can be used for TLE retrieving</p><p><span style=\" font-size:9pt;\">You can send your suggestions on silenteddie@gmail.com</span></p><p><span style=\" font-size:9pt;\">Modis Track L1 L2 - Licence GNU GPL 2</span></p><p><span style=\" font-size:9pt;\">Written in 2016 by Eduard Kazakov (</span><a href=\"http://www.ekazakov.info\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">ekazakov.info</span></a><span style=\" font-size:9pt;\">)</span></p></body></html>", None))
