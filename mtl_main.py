# -*- coding: utf-8 -*-
"""
/***************************************************************************
 modisTrackL1L2 mtl_main
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

from PyQt4.QtGui import QApplication

from ui import modisTrack_main_ui, modisTrack_settings_ui
import mtl_settings
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QVariant
from qgis.core import *
from qgis.core import QgsMapLayerRegistry
import resources
import spacetrack_interface
import urllib2
import os, re
import mtl_track_generator
import mtl_extent_generator
import mtl_lib
import datetime

class MTLMainDlg(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = modisTrack_main_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # Button's handlers
        self.connect(self.ui.closeButton, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(self.ui.TLESettingsButton, QtCore.SIGNAL("clicked()"), self.TLESettingsOpen)
        self.connect(self.ui.autoTLEButton, QtCore.SIGNAL("clicked()"), self.TLEAuto)
        self.connect(self.ui.satellitePositionOutputBrowseButton, QtCore.SIGNAL("clicked()"), self.satellitePositionOutputBrowse)
        self.connect(self.ui.extentPolygonsOutputBrowseButton, QtCore.SIGNAL("clicked()"), self.extentOutputBrowse)

        #Fill products
        try:
            dirPath = os.path.dirname(os.path.abspath(__file__))
            products_file = open(dirPath + '\\' +'products.txt','r')
            for line in products_file:
                self.ui.MODISProductComboBox.addItem(re.sub("^\s+|\n|\r|\s+$", '', line))
        except:
            pass

        #Date changing listener
        self.ui.orbitDate.dateChanged.connect(self.orbitDateChanged)

        #Product changing listener
        self.connect(self.ui.MODISProductComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.ProductChanged)

        #Checkbox listeners
        self.connect(self.ui.checkoutForObjectsCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.checkoutForObjectsStateChanged)
        self.connect(self.ui.satellitePositionOutputCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.satellitePositionOutputStateChanged)
        self.connect(self.ui.extentPolygonsOutputCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.extentOutputStateChanged)

        # Date to today-1

        self.ui.orbitDate.setDate(QtCore.QDate.currentDate().addDays(-1))

        #Fill layers combobox
        vectorLayers = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values() if
                          (layer.type() == QgsMapLayer.VectorLayer)]
        self.ui.layersComboBox.addItems(vectorLayers)


    def satellitePositionOutputBrowse(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', '*.shp')
        if filename:
            self.ui.satellitePositionOutputLine.setText(filename)
        pass

    def extentOutputBrowse(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', '*.shp')
        if filename:
            self.ui.extentPolygonsOutputLine.setText(filename)
        pass

    def orbitDateChanged (self):
        userDate = self.ui.orbitDate.date()
        userYear = userDate.year()
        userDayOfYear = str(userDate.dayOfYear())
        userDayOfYear = '0'*(3-len(userDayOfYear)) + userDayOfYear
        self.ui.MODISProductLinkLabel.setText("<a href = \'ftp://ladsweb.nascom.nasa.gov/allData/6/" + self.ui.MODISProductComboBox.currentText() + "/" + str(userYear) + "/" + str(userDayOfYear)+"/\'>Product link</a>")
        self.ui.MODISGeorefLinkLabel.setText("<a href = \'ftp://ladsweb.nascom.nasa.gov/allData/6/MOD03/" + str(userYear) + "/" + str(userDayOfYear)+"/\'>Georeferencing files link</a>")

    def ProductChanged (self):
        userDate = self.ui.orbitDate.date()
        userYear = userDate.year()
        userDayOfYear = str(userDate.dayOfYear())
        userDayOfYear = '0'*(3-len(userDayOfYear)) + userDayOfYear
        self.ui.MODISProductLinkLabel.setText("<a href = \'ftp://ladsweb.nascom.nasa.gov/allData/6/" + self.ui.MODISProductComboBox.currentText() + "/" + str(userYear) + "/" + str(userDayOfYear)+"/\'>Product link</a>")
        self.ui.MODISGeorefLinkLabel.setText("<a href = \'ftp://ladsweb.nascom.nasa.gov/allData/6/MOD03/" + str(userYear) + "/" + str(userDayOfYear)+"/\'>Georeferencing files link</a>")

    def checkoutForObjectsStateChanged (self):
        if self.ui.checkoutForObjectsCheckBox.isChecked():
            self.ui.onlySelectedCheckBox.setEnabled(True)
            self.ui.layersComboBox.setEnabled(True)
        else:
            self.ui.onlySelectedCheckBox.setDisabled(True)
            self.ui.layersComboBox.setDisabled(True)


    def satellitePositionOutputStateChanged(self):
        if self.ui.satellitePositionOutputCheckBox.isChecked():
            self.ui.satellitePositionOutputLine.setEnabled(True)
            self.ui.satellitePositionOutputBrowseButton.setEnabled(True)
            self.ui.addOutputsToProjectCheckBox.setEnabled(True)
        else:
            self.ui.satellitePositionOutputLine.setDisabled(True)
            self.ui.satellitePositionOutputBrowseButton.setDisabled(True)
            if not self.ui.extentPolygonsOutputCheckBox.isChecked():
                self.ui.addOutputsToProjectCheckBox.setChecked(False)
                self.ui.addOutputsToProjectCheckBox.setDisabled(True)

    def extentOutputStateChanged(self):
        if self.ui.extentPolygonsOutputCheckBox.isChecked():
            self.ui.extentPolygonsOutputLine.setEnabled(True)
            self.ui.extentPolygonsOutputBrowseButton.setEnabled(True)
            self.ui.addOutputsToProjectCheckBox.setEnabled(True)
            self.ui.splitToMultuGeomCheckBox.setEnabled(True)
        else:
            self.ui.extentPolygonsOutputLine.setDisabled(True)
            self.ui.extentPolygonsOutputBrowseButton.setDisabled(True)
            self.ui.splitToMultuGeomCheckBox.setDisabled(True)
            if not self.ui.satellitePositionOutputCheckBox.isChecked():
                self.ui.addOutputsToProjectCheckBox.setChecked(False)
                self.ui.addOutputsToProjectCheckBox.setDisabled(True)

    def TLESettingsOpen (self):
        self.MTLSettingsDlg = mtl_settings.MTLSettingsDlg()
        self.MTLSettingsDlg.show()

    def TLEAuto(self):

        try:
            dirPath = os.path.dirname(os.path.abspath(__file__))
            spacetrack_opt = open(dirPath + '\\' +'spacetrack.dat','r')
            login = re.sub("^\s+|\n|\r|\s+$", '', spacetrack_opt.readline())
            password = re.sub("^\s+|\n|\r|\s+$", '', spacetrack_opt.readline())
        except:
            QtGui.QMessageBox.critical(None, "Error", 'Login and password are not set')
            return

        userDate = self.ui.orbitDate.date()
        userYear = userDate.year()
        userMonth = userDate.month()
        userDay = userDate.day()
        if self.ui.satelliteComboBox.currentText() == 'Terra':
            satId = 25994
        elif self.ui.satelliteComboBox.currentText() == 'Aqua':
            satId = 27424

        try:
            tle1, tle2 = spacetrack_interface.get_spacetrack_tle_for_id_date(satId,userYear,userMonth,userDay,login,password)
        except (NameError):
            QtGui.QMessageBox.critical(None, "Error", 'Server is unavailable')
            return
        except (urllib2.HTTPError):
            QtGui.QMessageBox.critical(None, "Error", 'Invalid inputs. Check date.')
            return
        except:
            QtGui.QMessageBox.critical(None, "Error", 'Unable to recieve TLE')
            return

        self.ui.TLELine1.setText(tle1)
        self.ui.TLELine2.setText(tle2)


    # If "run" was pressed
    def run(self):

        if self.ui.satellitePositionOutputCheckBox.isChecked():
            if not self.ui.satellitePositionOutputLine.text():
                QtGui.QMessageBox.critical(None, "Error", 'Output file name not set')
                return
        if self.ui.extentPolygonsOutputCheckBox.isChecked():
            if not self.ui.extentPolygonsOutputLine.text():
                QtGui.QMessageBox.critical(None, "Error", 'Output file name not set')
                return
        if self.ui.checkoutForObjectsCheckBox.isChecked():
            if not self.ui.layersComboBox.currentText():
                QtGui.QMessageBox.critical(None, "Error", 'Layer is not selected')
                return
        ### End check inputs

        userDate = self.ui.orbitDate.date()
        userYear = userDate.year()
        userMonth = userDate.month()
        userDay = userDate.day()

        # TRACK
        if self.ui.satellitePositionOutputCheckBox.isChecked():

            try:
                trackLayer = mtl_track_generator.create_orbital_track_shapefile_for_day(userYear,userMonth,userDay,5,self.ui.TLELine1.text(),self.ui.TLELine2.text(),self.ui.satelliteComboBox.currentText())
            except (NameError):
                QtGui.QMessageBox.critical(None, "Error", 'Invalid TLE')
                return
            except (TypeError):
               QtGui.QMessageBox.critical(None, "Error", 'Invalid Inputs')
               return

            mtl_lib.saveVectorLayerToSHP(trackLayer,self.ui.satellitePositionOutputLine.text())
            if self.ui.addOutputsToProjectCheckBox.isChecked():
                QgsMapLayerRegistry.instance().addMapLayer(trackLayer)

        # EXTENTS
        if self.ui.extentPolygonsOutputCheckBox.isChecked():
            try:
                sceneExtentsLayer = mtl_extent_generator.generateScenesExtentLayerForDay(userYear,userMonth,userDay,self.ui.TLELine1.text(),self.ui.TLELine2.text(),self.ui.satelliteComboBox.currentText(),self.ui.splitToMultuGeomCheckBox.isChecked())
            except (NameError):
                QtGui.QMessageBox.critical(None, "Error", 'Invalid TLE')
                return
            except (TypeError):
                QtGui.QMessageBox.critical(None, "Error", 'Invalid Inputs')
                return

            mtl_lib.saveVectorLayerToSHP(sceneExtentsLayer,self.ui.extentPolygonsOutputLine.text())
            if self.ui.addOutputsToProjectCheckBox.isChecked():
                QgsMapLayerRegistry.instance().addMapLayer(sceneExtentsLayer)


    # Close window by pressing "Cancel" button
    def cancel(self):
        self.close()