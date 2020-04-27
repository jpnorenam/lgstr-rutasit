import rutasit
import pickle

######################## CREATE A NEW MET_AREA ########################################
#AMVA = rsmet.met_area('AMVA', '.\examples\AMVA\zonas_sit_amva.geojson', 'Nueva_Zona')
#AMVA.add_transport_system_group('METRO', '.\examples\AMVA\METRO.json', 4)
#AMVA.add_transport_system_group('SMM1', '.\examples\AMVA\BUSES_SMM1.json', 2)
#AMVA.add_transport_system_group('SMM2', '.\examples\AMVA\BUSES_SMM2.json', 2)
#AMVA.save_as("AMVA")

#################### LOAD A SAVED MET_AREA CLASS #####################################
AMVA = pickle.load(open('.\examples\AMVA\AMVA_2004262021.pickle', 'rb'))

############# ADD MORE TRANSPORT SYSTEM GROUPS TO THE SAVED AREA #############
#AMVA.add_transport_system_group('AMVA2', '.\examples\AMVA\BUSES_AMVA1.json', 2)
#AMVA.add_transport_system_group('AMVA2', '.\examples\AMVA\BUSES_AMVA2.json', 2)
#AMVA.add_transport_system_group('AMVA2', '.\examples\AMVA\BUSES_AMVA3.json', 2)
#AMVA.add_transport_system_group('AMVA2', '.\examples\AMVA\BUSES_AMVA4.json', 2)
#AMVA.save_as("AMVA")

#################### LOAD A SAVED MET_AREA CLASS #####################################
AMVA = pickle.load(open('.\examples\AMVA\AMVA_2004271717.pickle', 'rb'))

################# GET A ROUTE FROM ORIGIN ZONE TO A DESTINY ZONE #####################
#AMVA.location_zone(lon,lat,0) #get zone_code by lon, lat, radius=0
print(AMVA.get_route(234, 359, True))
print(AMVA.get_route(234, 91, True))
print(AMVA.get_route(202, 44, True))
print(AMVA.get_route(404, 363, True))


########## GET A ROUTE FROM ORIGIN ZONE TO A DESTINY ZONE AND PLOT ###################
#AMVA.get_route(272, 298, True)
