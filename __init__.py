# -*- coding: utf-8 -*-

"""
/***************************************************************************
 modisTrackL1L2 init
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

def classFactory(iface):
    from mtl import MTL
    return MTL(iface)
