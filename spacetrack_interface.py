"""
/***************************************************************************
 modisTrackL1L2 spacetrack_interface
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

from urllib import urlencode
from datetime import datetime, timedelta
from urllib2 import HTTPError, urlopen

import sys

def get_spacetrack_tle_for_id_date (satId, year, month, day, user, password):
    date1 = datetime(year,month,day).strftime('%Y-%m-%d')
    date2 = datetime(year,month,day) + timedelta(days=1)

    my_query = 'class/tle/NORAD_CAT_ID/' + str(satId) + '/EPOCH/' + str(date1) + '--' + str(date2) + '/orderby/EPOCH asc/format/tle'
    try:
        res = query(my_query, user, password)
    except:
        raise HTTPError
    try:
        tle1 = res.split('\n')[0]
        tle2 = res.split('\n')[1]
    except:
        raise NameError # invalid inputs

    return tle1, tle2

class DownloadError(Exception):
    pass

def downloadResource(url, fn, data=None, unifyErrors=True, timeout=None):
    retry = False
    try:
        return _downloadResource(url, fn, data=data, timeout=timeout)
    except HTTPError as e:
        if e.code == 404:
            if unifyErrors:
                raise DownloadError(e)
            else:
                raise
        else:
            retry = True
    except IOError as e:
        if unifyErrors:
            raise DownloadError(e)
        else:
            raise
    except Exception as e:
        retry = True

    if retry:
        try:
            return _downloadResource(url, fn, data=data, timeout=timeout)
        except:
            if unifyErrors:
                _, e, tb = sys.exc_info()
                new_exc = DownloadError('{}: {}'.format(e.__class__.__name__, e))
            else:
                raise

def _downloadResource(url, fn, data=None, timeout=None):
    if timeout is None:
        timeout = 60
    try:
        req = urlopen(url, data=data, timeout=timeout)
        res = fn(req)
        return res
    except Exception as e:
        raise

def query(query, user, password):
    baseUrl = 'https://www.space-track.org/'
    authUrl = baseUrl + 'ajaxauth/login'
    queryPrefix = 'basicspacedata/query/'

    queryUrl = baseUrl + queryPrefix + query
    data = urlencode({'identity': user, 'password': password, 'query': queryUrl})
    res = downloadResource(authUrl, lambda r: r.read(), data=data)
    return res