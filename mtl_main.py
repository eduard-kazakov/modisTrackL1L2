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
import processing


class MTLMainDlg(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = modisTrack_main_ui.Ui_Dialog()
        self.ui.setupUi(self)

        self.readyInterface()

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
            self.ui.layersComboBox.setEnabled(True)
        else:
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
        self.busyInterface()
        QApplication.processEvents()

        try:
            dirPath = os.path.dirname(os.path.abspath(__file__))
            spacetrack_opt = open(dirPath + '\\' +'spacetrack.dat','r')
            login = re.sub("^\s+|\n|\r|\s+$", '', spacetrack_opt.readline())
            password = re.sub("^\s+|\n|\r|\s+$", '', spacetrack_opt.readline())
        except:
            QtGui.QMessageBox.critical(None, "Error", 'Login and password are not set')
            self.readyInterface()
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
            self.readyInterface()
            return
        except (urllib2.HTTPError):
            QtGui.QMessageBox.critical(None, "Error", 'Invalid inputs. Check date.')
            self.readyInterface()
            return
        except:
            QtGui.QMessageBox.critical(None, "Error", 'Unable to recieve TLE')
            self.readyInterface()
            return

        self.ui.TLELine1.setText(tle1)
        self.ui.TLELine2.setText(tle2)
        self.readyInterface()


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
        self.busyInterface()
        QApplication.processEvents()

        if self.ui.satellitePositionOutputCheckBox.isChecked():

            try:
                trackLayer = mtl_track_generator.create_orbital_track_shapefile_for_day(userYear,userMonth,userDay,5,self.ui.TLELine1.text(),self.ui.TLELine2.text(),self.ui.satelliteComboBox.currentText())
            except (NameError):
                QtGui.QMessageBox.critical(None, "Error", 'Invalid TLE')
                self.readyInterface()
                return
            except (TypeError):
               QtGui.QMessageBox.critical(None, "Error", 'Invalid Inputs')
               self.readyInterface()
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
                self.readyInterface()
                return
            except (TypeError):
                QtGui.QMessageBox.critical(None, "Error", 'Invalid Inputs')
                self.readyInterface()
                return

            mtl_lib.saveVectorLayerToSHP(sceneExtentsLayer,self.ui.extentPolygonsOutputLine.text())
            if self.ui.addOutputsToProjectCheckBox.isChecked():
                extentLayerName = 'Scene\'s extents (' + self.ui.satelliteComboBox.currentText() + ': ' + str(userYear) + ':' + str(userMonth) + ':' + str(userDay) + ')'
                extentsLayer = QgsVectorLayer(self.ui.extentPolygonsOutputLine.text(),extentLayerName,'ogr')
                QgsMapLayerRegistry.instance().addMapLayer(extentsLayer)

        # OBJECTS
        if self.ui.checkoutForObjectsCheckBox.isChecked():
            userLayer = mtl_lib.getLayerByName(self.ui.layersComboBox.currentText())
            if userLayer.isValid() == False:
                QtGui.QMessageBox.critical(None, "Error", 'Invalid input vector layer')
                self.readyInterface()
                return

            if self.ui.extentPolygonsOutputCheckBox.isChecked() and self.ui.splitToMultuGeomCheckBox.isChecked():
                pass
            else:
                sceneExtentsLayer = mtl_extent_generator.generateScenesExtentLayerForDay(userYear,userMonth,userDay,self.ui.TLELine1.text(),self.ui.TLELine2.text(),self.ui.satelliteComboBox.currentText(),True)

            QgsMapLayerRegistry.instance().addMapLayer(sceneExtentsLayer)

            WGS84 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
            reproj = False
            if userLayer.crs() != WGS84:
                # Reproject userLayer to WGS84
                try:
                    userLayerReprojected = mtl_lib.reprojectVectorLayerToMemoryLayer(userLayer.crs(),WGS84,userLayer)
                    QgsMapLayerRegistry.instance().addMapLayer(userLayerReprojected)
                    reproj = True
                except:
                    pass

            # Intersects
            try:
                if reproj:
                    processing.runalg('qgis:selectbylocation',sceneExtentsLayer,userLayerReprojected,u'intersects',0)
                else:
                    processing.runalg('qgis:selectbylocation',sceneExtentsLayer,userLayer,u'intersects',0)
            except:
                QtGui.QMessageBox.critical(None, "Error", 'Processing must be enabled!')
                self.readyInterface()
                return

            features = sceneExtentsLayer.selectedFeatures()
            intersectsList = []
            for f in features:
                intersectsList.append(f[1])

            # Contains
            try:
                if reproj:
                    processing.runalg('qgis:selectbylocation',sceneExtentsLayer,userLayerReprojected,u'contains',0)
                else:
                    processing.runalg('qgis:selectbylocation',sceneExtentsLayer,userLayer,u'contains',0)
            except:
                QtGui.QMessageBox.critical(None, "Error", 'Processing must be enabled!')
                self.readyInterface()
                return

            features = sceneExtentsLayer.selectedFeatures()
            containsList = []
            for f in features:
                containsList.append(f[1])
            QgsMapLayerRegistry.instance().removeMapLayer(sceneExtentsLayer.id())
            if reproj:
                QgsMapLayerRegistry.instance().removeMapLayer(userLayerReprojected.id())

            resultText = 'Associated scenes: <br> '
            for sceneTime in intersectsList:
                resultText += sceneTime + '<br>'

            self.ui.checkoutTextBox.setText(resultText)

        self.readyInterface()

    def busyInterface(self):
        self.ui.progressBar.setVisible(True)
        self.ui.ftpGroupBox.setDisabled(True)
        self.ui.objectsGroupBox.setDisabled(True)
        self.ui.orbitGroupBox.setDisabled(True)
        self.ui.outputsGroupBox.setDisabled(True)

    def readyInterface(self):
        self.ui.progressBar.setVisible(False)
        self.ui.ftpGroupBox.setEnabled(True)
        self.ui.objectsGroupBox.setEnabled(True)
        self.ui.orbitGroupBox.setEnabled(True)
        self.ui.outputsGroupBox.setEnabled(True)

    # Close window by pressing "Cancel" button
    def cancel(self):
        self.close()