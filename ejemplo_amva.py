from rutasit.metropolitan_area import met_area
import pickle

######################## CREATE A NEW MET_AREA ########################################
# AMVA = met_area('AMVA', '.\examples\AMVA\zonas_sit_amva.geojson', 'Nueva_Zona')
# AMVA.add_transport_system_group('METRO', '.\examples\AMVA\METRO.json', 4)
# AMVA.add_transport_system_group('SMM1', '.\examples\AMVA\BUSES_SMM1.json', 2)
# AMVA.add_transport_system_group('SMM2', '.\examples\AMVA\BUSES_SMM2.json', 2)
# AMVA.save_as("AMVA")

############# ADD MORE TRANSPORT SYSTEM GROUPS TO THE SAVED AREA #############
# AMVA.add_transport_system_group('AMVA1', '.\examples\AMVA\BUSES_AMVA1.json', 2)
# AMVA.add_transport_system_group('AMVA2', '.\examples\AMVA\BUSES_AMVA2.json', 2)
# AMVA.add_transport_system_group('AMVA3', '.\examples\AMVA\BUSES_AMVA3.json', 2)
# AMVA.add_transport_system_group('AMVA4', '.\examples\AMVA\BUSES_AMVA4.json', 2)
# # AMVA.save_as("AMVA")
#
# AMVA.add_transport_system_group('AMVA_NI1', '.\examples\AMVA\BUSES_AMVA_NO_INTEGRADAS_P1.json', 2)
# AMVA.add_transport_system_group('AMVA_NI2', '.\examples\AMVA\BUSES_AMVA_NO_INTEGRADAS_P2.json', 2)
# AMVA.add_transport_system_group('AMVA_NI3', '.\examples\AMVA\BUSES_AMVA_NO_INTEGRADAS_P3.json', 2)
# AMVA.add_transport_system_group('AMVA_NI4', '.\examples\AMVA\BUSES_AMVA_NO_INTEGRADAS_P4.json', 2)
# AMVA.add_transport_system_group('AMVA_NI5', '.\examples\AMVA\BUSES_AMVA_NO_INTEGRADAS_P5.json', 2)
#
# AMVA.add_transport_system_group('AMVA_SMM_NI1', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P1.json', 2)
# AMVA.add_transport_system_group('AMVA_SMM_NI2', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P2.json', 2)
# AMVA.add_transport_system_group('AMVA_SMM_NI3', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P3.json', 2)
# AMVA.add_transport_system_group('AMVA_SMM_NI4', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P4.json', 2)
# AMVA.add_transport_system_group('AMVA_SMM_NI5', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P5.json', 2)
# AMVA.add_transport_system_group('AMVA_SMM_NI6', '.\examples\AMVA\BUSES_SMM_NO_INTEGRADAS_P6.json', 2)
#
# AMVA.save_as("AMVA_happy")

#################### LOAD A SAVED MET_AREA CLASS #####################################
AMVA = pickle.load(open('.\examples\AMVA\AMVA_18.pickle', 'rb'))

################# GET A ROUTE FROM ORIGIN ZONE TO A DESTINY ZONE #####################
#AMVA.location_zone(lon,lat,0) #get zone_code by lon, lat, radius=0
#print(AMVA.get_route(234, 359, True))
#print(AMVA.get_route(358, 404, True))
#print(AMVA.get_route(202, 44, True))
#print(AMVA.get_route(404, 363, True))
#print(AMVA.get_route(467, 417, True))
#print(AMVA.get_route(404, 258, True))
#print(AMVA.get_route(447, 398, True))
#print(AMVA.get_route(404, 237, True))
#print(AMVA.get_route(398, 131, True))
print(AMVA.get_route(459, 130, True))
########## GET A ROUTE FROM ORIGIN ZONE TO A DESTINY ZONE AND PLOT ###################
#AMVA.get_route(272, 298, True)
