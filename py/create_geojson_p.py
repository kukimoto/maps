#!/usr/bin/env python
import os
import sys
import json
from geojson import Point, Feature, FeatureCollection

def get_geo_value(gpsdata, item, delimiter):
    si = gpsdata.find(item)
    value = '0.000000'
    if si != -1:
        si += len(item)
        ei = gpsdata.find(delimiter, si)
        if ei != -1:
            value = gpsdata[si:ei]
    return value

def get_altitude(gpsdata):
    return get_geo_value(gpsdata, 'Alt:', '}')

def get_latitude(gpsdata):
    return get_geo_value(gpsdata, 'Lat:', ',')

def get_longitude(gpsdata):
    return get_geo_value(gpsdata, 'Long:', ',')

def write_geojsone_file(fname, feature_collection):
    # open a file with write mode
    with open(fname, 'w') as gjfile:
        # Output GeoJson file
        gjfile.write(json.dumps(feature_collection,indent=2))

def read_lines(f):
    my_features = []
    i = 0
    pre_lat = '0.000000'
    pre_lon = '0.000000'
    pre_alt = '0.000000'
    for line in f:
        # print (line)
        index =  line.find('gpsData')
        if index != -1:
            gpsdata = line[(index + len('gpsData')):-1]
            # print(gpsdata)
            latitude = get_latitude(gpsdata)
            longitude = get_longitude(gpsdata)
            altitude = get_altitude(gpsdata)
            if latitude != '0.000000' and longitude != '0.000000':
                if pre_lat != latitude or pre_lon != longitude or pre_alt != altitude:
                    areas = line.split()
                    timestamp = areas[1] + ' ' + areas[2]
                    eventtype = "NULL"
                    print (latitude,longitude,altitude)
                    my_point=Point((float(longitude), float(latitude), float(altitude)))
                    my_features.append(Feature(geometry=my_point, id=i, properties={"time": timestamp, "event": eventtype}))
                    pre_lat = latitude
                    pre_lon = longitude
                    pre_alt = altitude
                    i += 1
    feature_collection = FeatureCollection(my_features)
    return feature_collection

def read_file(arg):
    with open(arg, 'r') as f:
        return read_lines(f)

argvs = sys.argv  # command line argument
argc = len(argvs) # number of argument
if(argc != 2):
    print ('Please set file name as argument. An example is below.')
    print ('python this.py test.log')
    quit()
# Get output file name from argment(file path)
path, ext = os.path.splitext( argvs[1] )
fname = path + '.geojson'
# read input file to get geo data
feature_collection = read_file(argvs[1])
# Output GeoJson file
write_geojsone_file(fname, feature_collection)
