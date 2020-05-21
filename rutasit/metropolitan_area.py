import os
import json
import pickle
from .transport_systems import transport_sys_group
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from datetime import datetime
import shapely.ops as ops
import pyproj
import random
import numpy as np


class met_area(object):
    """

    """
    def __init__(self, name, file_path, zone_code_property_str):
        self.name = name
        self.wd = os.path.dirname(file_path)
        self.polygons_dict = {}
        self.forward_mapping = {}
        self.inverse_mapping = {}
        self.zone_counter = 0
        self.transport_sys = []
        self.tsg_connections = {}
        self.__get_geojson_info(file_path, zone_code_property_str)

    def __get_geojson_info(self, file_path, zone_code_property_str):
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        for feature in json_data['features']:
            zone_code = feature['properties'][zone_code_property_str]
            zone_polygon = Polygon(feature['geometry']['coordinates'][0])
            self.polygons_dict[zone_code] = zone_polygon
            self.forward_mapping[zone_code] = self.zone_counter
            self.inverse_mapping[self.zone_counter] = zone_code
            self.zone_counter += 1

    def __update_tsg_connections(self):
        N = len(self.transport_sys)
        self.tsg_connections = {}
        for sys_i in range(N):
            list1_ = [[]*N]*N
            for sys_j in range(N):
                if sys_i != sys_j:
                    list1_[sys_j] = [code_j for code_j in list(self.transport_sys[sys_j].public_coverage) if code_j in self.transport_sys[sys_i].public_coverage]
            self.tsg_connections[sys_i] = list1_

    def add_transport_system_group(self, name, file_path, max_transfers):
        self.transport_sys.append(transport_sys_group(name, file_path, self, max_transfers))
        self.__update_tsg_connections()
    
    def save_as(self, name):
        with open(os.path.join(self.wd, "{}_{}.pickle".format(self.name, datetime.now().strftime("%y%m%d%H%M"))), 'wb') as pickle_save:
            pickle.dump(self, pickle_save)

    def location_zone(self, lon, lat, radius):
        """
        :param lon: location longitude
        :param lat: location latitude 
        :param radius: radius of impact for the location (lon, lat) point in meters
        :return: 
        """
        wgs84_step = radius * 0.003 / 250.0
        check_points = [Point(lon, lat), Point(lon+wgs84_step, lat), Point(lon-wgs84_step, lat), Point(lon, lat+wgs84_step), Point(lon, lat-wgs84_step)]
        zone_codes = []
        for zone_code in self.polygons_dict:
            [zone_codes.append(zone_code) for point in check_points if self.polygons_dict[zone_code].contains(point)]
            if (len(zone_codes) == 5):
                return np.unique(zone_codes)
    

    def zone_area(self, zone_code):
        """
        :return: area of the polygon [m]
        """
        polyg_areaM = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),
                pyproj.Proj(
                    proj='aea',
                    lat_1=self.polygons_dict[zone_code].bounds[1],
                    lat_2=self.polygons_dict[zone_code].bounds[3])),
            self.polygons_dict[zone_code]) * 1e-6
        return polyg_areaM

    def zone_centroid(self, zone_code):
        """
        :return: longitude of the centroid, latitude of the centroid
        """
        polyg_centX = self.polygons_dict[zone_code].centroid.x
        polyg_centY = self.polygons_dict[zone_code].centroid.y
        return polyg_centX, polyg_centY

    def closest_zone(self, zone_code_origin, options_zone_codes):
        """
        :param zone_code_origin: zone code of interest
        :param options_zone_code: array of zone code options
        :return: closest zone of options_zone_code to zone_code_origin
        """
        geod = pyproj.Geod(ellps='WGS84')
        orig_lon, orig_lat = self.zone_centroid(zone_code_origin)
        clost_code = -1
        clost_dist = 1E20
        for zone_code in options_zone_codes:
            clost_lon, clost_lat = self.zone_centroid(zone_code)
            azimuth1, azimuth2, distance = geod.inv(orig_lon, orig_lat, clost_lon, clost_lat)
            if (distance < clost_dist):
                clost_dist = distance
                clost_code = zone_code
        return clost_code

    def get_route(self, origin_zone, destiny_zone, plot=False):
        nTS = len(self.transport_sys)
        oBelong = [ True if origin_zone in sys.public_coverage else False for sys in self.transport_sys ]
        dBelong = [ True if destiny_zone in sys.public_coverage else False for sys in self.transport_sys ]
        try:
            oSys = np.where(np.array(oBelong) == True)[0][0]
            dSys = np.where(np.array(dBelong) == True)[0][0]
        except:
            return "NOT POSIBLE"

        if oSys == dSys:
            bSys = np.where(np.logical_and(oBelong, dBelong) == True)[0][0]
            info, trace = self.transport_sys[bSys].decode_connection(origin_zone, destiny_zone)
            if plot:
                plt.plot(*self.polygons_dict[origin_zone].exterior.xy)
                plt.plot(*self.polygons_dict[destiny_zone].exterior.xy)
                plt.plot(*LineString(trace).xy)
                plt.xlim((-75.68, -75.48))
                plt.ylim((6.14, 6.34))
                plt.show()
            return info
            
        elif len(self.tsg_connections[oSys][dSys]) != 0:
            inter_group_destiny = self.closest_zone(origin_zone, list(self.tsg_connections[oSys][dSys]))
            info1, trace1 = self.transport_sys[oSys].decode_connection(origin_zone, inter_group_destiny)
            info2, trace2 = self.transport_sys[dSys].decode_connection(inter_group_destiny, destiny_zone)
            if len(trace1)*len(trace2):
                if plot:
                    plt.plot(*self.polygons_dict[origin_zone].exterior.xy)
                    plt.plot(*self.polygons_dict[destiny_zone].exterior.xy)
                    plt.plot(*LineString(trace1 + trace2).xy)
                    plt.xlim((-75.7, -75.4))
                    plt.ylim((6.1, 6.4))
                    plt.show()
                return info1 + info2
            else:
                inter_jump1 = self.closest_zone(origin_zone, list(self.transport_sys[0].public_coverage))
                inter_jump2 = self.closest_zone(destiny_zone, list(self.transport_sys[0].public_coverage))
                info1, trace1 = self.transport_sys[oSys].decode_connection(origin_zone, inter_jump1)
                infoM, traceM = self.transport_sys[0].decode_connection(inter_jump1, inter_jump2)
                info2, trace2 = self.transport_sys[dSys].decode_connection(inter_jump2, destiny_zone)
                if len(trace1)*len(trace2)*len(traceM):
                    if plot:
                        plt.plot(*self.polygons_dict[origin_zone].exterior.xy)
                        plt.plot(*self.polygons_dict[destiny_zone].exterior.xy)
                        plt.plot(*LineString(trace1 + traceM + trace2).xy)
                        plt.xlim((-75.7, -75.4))
                        plt.ylim((6.1, 6.4))
                        plt.show()
                    return info1 + infoM + info2
                else:
                    return "NOT POSIBLE"
        
        
        else:
            label .force_metro
            inter_jump1 = self.closest_zone(origin_zone, list(self.transport_sys[0].public_coverage))
            inter_jump2 = self.closest_zone(destiny_zone, list(self.transport_sys[0].public_coverage))
            info1, trace1 = self.transport_sys[oSys].decode_connection(origin_zone, inter_jump1)
            infoM, traceM = self.transport_sys[0].decode_connection(inter_jump1, inter_jump2)
            info2, trace2 = self.transport_sys[dSys].decode_connection(inter_jump2, destiny_zone)
            if len(trace1)*len(trace2)*len(traceM):
                if plot:
                    plt.plot(*self.polygons_dict[origin_zone].exterior.xy)
                    plt.plot(*self.polygons_dict[destiny_zone].exterior.xy)
                    plt.plot(*LineString(trace1 + traceM + trace2).xy)
                    plt.xlim((-75.7, -75.4))
                    plt.ylim((6.1, 6.4))
                    plt.show()
                return info1 + infoM + info2
            else:
                return "NOT POSIBLE"
            
