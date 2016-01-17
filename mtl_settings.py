# -*- coding: utf-8 -*-
"""
/***************************************************************************
 modisTrackL1L2 mtl_settings
                                 A QGIS plugin
This module allows to create Terra/Aqua track at selected date as shapefile;
                   to create extents of scenes for all track points at day as shapefile;
                   to define needed scenes for user's vector layer.
Space-track.org can be used for TLE retrieving

                              -------------------
        begin                : 2016-01-16
        copyright            : (C) 2016 by Eduard Kazakov
        email                : silenteddie@gmail.com
        homepage             : http://ekazakov.info
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from ui import modisTrack_settings_ui
from PyQt4 import QtGui, QtCore
import os
import re

class MTLSettingsDlg(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = modisTrack_settings_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # Button's handlers
        self.connect(self.ui.settingsCancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.settingsApplyButton, QtCore.SIGNAL("clicked()"), self.apply)

        #Refresh from file
        try:
            dirPath = os.path.dirname(os.path.abspath(__file__))
            spacetrack_opt = open(dirPath + '\\' +'spacetrack.dat','r')
            login = spacetrack_opt.readline()
            password = spacetrack_opt.readline()
            self.ui.loginLine.setText(re.sub("^\s+|\n|\r|\s+$", '', login))
            self.ui.passwordLine.setText(re.sub("^\s+|\n|\r|\s+$", '', password))
        except:
            pass

    def apply(self):
        if not self.ui.loginLine.text() or not self.ui.passwordLine.text():
            QtGui.QMessageBox.critical(None, "Error", 'Empty login or password!')
            return

        dirPath = os.path.dirname(os.path.abspath(__file__))
        spacetrack_opt = open(dirPath + '\\' +'spacetrack.dat','w')
        spacetrack_opt.write(self.ui.loginLine.text())
        spacetrack_opt.write('\n')
        spacetrack_opt.write(self.ui.passwordLine.text())
        spacetrack_opt.close()

        self.close()

    def cancel(self):
        self.close()