import numpy as np
import json
from itertools import combinations
import random
import pyproj
from .logical_operations import add_transfer_connections

class transport_sys_group(object):
    """

    """
    def __init__(self, name, file_path, parent_met, max_transfers):
        self.name = name
        self.parent_met = parent_met
        self.direct_matrix = np.zeros([parent_met.zone_counter, parent_met.zone_counter], dtype=int)
        self.connection_matrix = np.zeros([parent_met.zone_counter, parent_met.zone_counter], dtype=int)
        self.public_routes = {}
        self.public_coverage = {}
        
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        if len(json_data['features']) > 31:
            raise AttributeError("The number of routes per transport system group can't exced 31")
        else:
            coder = 0
            for feature in json_data['features']:
                self.public_routes[coder] = public_route(feature, self, coder)
                self.direct_matrix = self.public_routes[coder].add2_group_connection(self.direct_matrix) #is this equality need?
                coder += 1
            self.connection_matrix = add_transfer_connections(self.direct_matrix, max_transfers)

    def decode_connection(self, orig_code, dest_code):
        str_route = []
        index_orig = self.parent_met.forward_mapping[orig_code]
        index_dest = self.parent_met.forward_mapping[dest_code]
        connection_coder = self.connection_matrix[index_orig, index_dest] 
        individual_routes = []
        for route_coder in self.public_routes:
            if 2**route_coder & connection_coder:
                individual_routes.append(route_coder)
        possible_stops = []
        
        transfer_combinations = list(combinations(individual_routes, 2))
        for zone_code in self.public_coverage:
            for transfer in transfer_combinations:
                if self.public_coverage[zone_code] & (2**transfer[0] | 2**transfer[1]) == (2**transfer[0] | 2**transfer[1]):
                    if zone_code not in possible_stops:
                        possible_stops.append(zone_code)
                        transfer_combinations.remove(transfer)
                        break

        route_dict = {}
        jump_origin_index = self.parent_met.forward_mapping[orig_code]
        for jump_n in range(len(possible_stops)+1):
            if (self.direct_matrix[jump_origin_index, index_dest]):
                route_dict[self.direct_matrix[jump_origin_index, index_dest]] = [orig_code, dest_code]
                break
            else:
                for stop_code in possible_stops:
                    stop_index = self.parent_met.forward_mapping[stop_code]
                    if (self.direct_matrix[jump_origin_index, stop_index]):
                        route_dict[self.direct_matrix[jump_origin_index, stop_index]] = [orig_code, stop_code]
                        possible_stops.remove(stop_code)
                        jump_origin_index = stop_index
                        orig_code = stop_code
                        break
        group_res_str = []
        group_res_coords = []
        for route_coder in route_dict:
            #the direct connection coder can contain several public routes that match the origin/destiny
            #we are picking le largest coder of the possible routes, consider changing it for future versions
            route_orig = route_dict[route_coder][0]
            route_dest = route_dict[route_coder][1]
            route_coder = int(np.log2(route_coder))
            route_name = self.public_routes[route_coder].name
            route_distance, route_duration, route_linestring = self.public_routes[route_coder].travel_info(route_orig, route_dest)
            group_res_str.append("{}:{}:{}".format(route_name, route_distance, route_duration))
            group_res_coords += route_linestring.tolist()

        return group_res_str, group_res_coords

class public_route(object):
    def __init__(self, geojson_feature, parent_group, coder):
            self.parent_group = parent_group
            self.coder = coder
            self.name = geojson_feature["properties"]["NOMBRE"]
            self.id = geojson_feature["properties"]["ID"]
            self.type = geojson_feature["properties"]["TIPO_SISTE"]
            self.avg_speed = geojson_feature["properties"]["VELOC_SISTE"] #Let this be a configurable parameter from a general conf file?
            self.coverage_radius = 200.0 #Let this be a configurable parameter from a general conf file?
            self.station_indexes = geojson_feature["properties"]["ESTACIONES"]
            self.reversible = bool(geojson_feature["properties"]["REVERSIBLE"])
            self.trace_coordinates = np.array(geojson_feature["geometry"]["coordinates"])
            self.zone_stations = self.stations_locations()

    def stations_locations(self):
        stations_zone_dict = {}
        for station_index in self.station_indexes:
            location = self.trace_coordinates[station_index]
            zona_codes = self.parent_group.parent_met.location_zone(location[0], location[1], self.coverage_radius)
            for zone_code in zona_codes:
                if not zone_code in stations_zone_dict:
                    stations_zone_dict[zone_code] = [station_index]
                else:
                    stations_zone_dict[zone_code].append(station_index)
        return stations_zone_dict

    def travel_info(self, orig_zone, dest_zone):
        """
        :return: distance [m], duration [sec], list of coordinates of the route trace [lon,lat]
        """
        if not orig_zone in self.zone_stations or not dest_zone in self.zone_stations:
            raise AttributeError("The origin zone and destiny aren't both cointained in the route")
        else:
            geod = pyproj.Geod(ellps='WGS84')
            est_orig = random.choice(self.zone_stations[orig_zone])
            dest_orig = random.choice(self.zone_stations[dest_zone])
            linestring = self.trace_coordinates[min([est_orig, dest_orig]):max([est_orig, dest_orig])+1]
            distance = geod.line_length(linestring[:,0], linestring[:,1])
            duration = 3.6 * distance / self.avg_speed
            return distance, duration, linestring
     
    def add2_group_connection(self, group_connection_matrix):
        N = self.parent_group.parent_met.zone_counter
        if (group_connection_matrix.shape[0] != N or
            group_connection_matrix.shape[1] != N ):
            raise AttributeError("Argument group_connection_matrix dimension doesn't match the parent MET zones")
        else:
            for code_orig in range(N):
                for code_dest in range(code_orig, N):
                        if code_orig in self.zone_stations and code_dest in self.zone_stations: # check this for NON reversible systems
                            index_orig = self.parent_group.parent_met.forward_mapping[code_orig]
                            index_dest = self.parent_group.parent_met.forward_mapping[code_dest]
                            group_connection_matrix[index_orig, index_dest] |=  2 ** self.coder
                            if self.reversible:
                                group_connection_matrix[index_dest, index_orig] |=  2 ** self.coder
                            if index_orig == index_dest:
                                self.parent_group.public_coverage[code_orig] = group_connection_matrix[index_orig, index_orig]
            return group_connection_matrix