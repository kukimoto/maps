#!/usr/bin/env python
import os
import sys
import simplekml
from datetime import datetime

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

def read_lines(f):
    kml = simplekml.Kml()
    i = 0
    pre_gps = {'latitude':'0.000000', 'longitude':'0.000000', 'altitude':'0.000000'}
    for line in f:
        #print (line)
        index =  line.find('gpsData')
        if index != -1:
            gpsdata = line[(index + len('gpsData')):-1]
            # print(gpsdata)
            latitude = get_latitude(gpsdata)
            longitude = get_longitude(gpsdata)
            altitude = get_altitude(gpsdata)
            # if latitude is not None and longitude is not None and altitude is not None:
            if latitude != '0.000000' and longitude != '0.000000':
                if pre_gps['latitude'] != latitude or pre_gps['longitude'] != longitude or pre_gps['altitude'] != altitude:
                    print (latitude,longitude,altitude)
                    areas = line.split()
                    timestamp = areas[1] + ' ' + areas[2]
                    kml.newpoint(name=timestamp, coords=[(float(longitude), float(latitude), float(altitude))])
                    pre_gps['latitude'] = latitude
                    pre_gps['longitude'] = longitude
                    pre_gps['altitude'] = altitude
                    i += 1
    kname = datetime.now().strftime("%Y%m%d%H%M%S") + '.kml'
    kml.save(kname)

def read_file(arg):
    with open(arg, 'r') as f:
        return read_lines(f)

argvs = sys.argv  # command line argument
argc = len(argvs) # number of argument
if(argc != 2):
    print ('Please set file name as argument')
    print ('python test.py tested.dlt')
    quit()

read_file(argvs[1])
