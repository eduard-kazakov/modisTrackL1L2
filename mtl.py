# -*- coding: utf-8 -*-
"""
/***************************************************************************
 modisTrackL1L2 mtl
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mtl_main import MTLMainDlg
from mtl_about import MTLAboutDlg
import os

class MTL:

    def __init__(self,iface):
        self.iface=iface
        self.dlg = MTLMainDlg()

    def initGui(self):

        dirPath = os.path.dirname(os.path.abspath(__file__))
        self.action = QAction(u"MODIS Track L1 L2", self.iface.mainWindow())
        self.action.setIcon(QIcon(dirPath + "/icon.png"))
        self.iface.addPluginToVectorMenu(u"MODIS Track L1 L2",self.action)
        self.action.setStatusTip(u"MODIS Track L1 L2")
        self.iface.addVectorToolBarIcon(self.action)
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        self.aboutAction = QAction(u"About", self.iface.mainWindow())
        QObject.connect(self.aboutAction, SIGNAL("triggered()"), self.about)
        self.iface.addPluginToVectorMenu(u"MODIS Track L1 L2", self.aboutAction)

    def unload(self):
        self.iface.removeVectorToolBarIcon(self.action)
        self.iface.removePluginVectorMenu(u"MODIS Track L1 L2",self.action)

        self.iface.removePluginVectorMenu(u"MODIS Track L1 L2",self.aboutAction)

    def run(self):
        self.MTLMainDlg = MTLMainDlg()
        self.MTLMainDlg.show()

    def about(self):
        self.MTLAboutDlg = MTLAboutDlg()
        self.MTLAboutDlg.show()