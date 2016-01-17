# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modisTrack_settings_ui.ui'
#
# Created: Sat Jan 16 05:16:33 2016
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
        Dialog.resize(232, 114)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/modisTrackL1L2/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.loginLine = QtGui.QLineEdit(Dialog)
        self.loginLine.setObjectName(_fromUtf8("loginLine"))
        self.gridLayout.addWidget(self.loginLine, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.passwordLine = QtGui.QLineEdit(Dialog)
        self.passwordLine.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.passwordLine.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLine.setObjectName(_fromUtf8("passwordLine"))
        self.gridLayout.addWidget(self.passwordLine, 2, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.settingsCancelButton = QtGui.QPushButton(Dialog)
        self.settingsCancelButton.setObjectName(_fromUtf8("settingsCancelButton"))
        self.horizontalLayout.addWidget(self.settingsCancelButton)
        self.settingsApplyButton = QtGui.QPushButton(Dialog)
        self.settingsApplyButton.setObjectName(_fromUtf8("settingsApplyButton"))
        self.horizontalLayout.addWidget(self.settingsApplyButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Spacetrack settings", None))
        self.label_3.setText(_translate("Dialog", "<a href=\"https://www.space-track.org/auth/createAccount\">Register on space-track.org</a>", None))
        self.label.setText(_translate("Dialog", "Login:", None))
        self.label_2.setText(_translate("Dialog", "Password:", None))
        self.settingsCancelButton.setText(_translate("Dialog", "Cancel", None))
        self.settingsApplyButton.setText(_translate("Dialog", "Apply", None))
