from qgis.core import *
def getLayerByName(vectorLayerName):
    layer = None
    for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
        if lyr.name() == vectorLayerName:
            layer = lyr
            break

    return layer

def saveVectorLayerToSHP(vectorLayer, shpFullPath):
    error = QgsVectorFileWriter.writeAsVectorFormat(vectorLayer, shpFullPath, "UTF-8", None, "ESRI Shapefile")
    return error

def getFeaturesAsList (vectorLayer):
    features = vectorLayer.getFeatures()
    featuresList = []
    for feature in features:
        featuresList.append(feature)

    return featuresList