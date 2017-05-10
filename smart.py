import math

# __________________
#
# Catchment model * c_ *
# _ Hydrology
# ___ Inputs
# _____ c_in_rain              precipitation as rain [mm/time step]
# _____ c_in_peva              potential evapotranspiration [mm/time step]
# ___ States
# _____ c_s_v_h2o_ove       volume of water in overland store [m3]
# _____ c_s_v_h2o_dra       volume of water in drain store [m3]
# _____ c_s_v_h2o_int       volume of water in inter store [m3]
# _____ c_s_v_h2o_sgw       volume of water in shallow groundwater store [m3]
# _____ c_s_v_h2o_dgw       volume of water in deep groundwater store [m3]
# _____ c_s_v_h2o_ly1       volume of water in first soil layer store [m3]
# _____ c_s_v_h2o_ly2       volume of water in second soil layer store [m3]
# _____ c_s_v_h2o_ly3       volume of water in third soil layer store [m3]
# _____ c_s_v_h2o_ly4       volume of water in fourth soil layer store [m3]
# _____ c_s_v_h2o_ly5       volume of water in fifth soil layer store [m3]
# _____ c_s_v_h2o_ly6       volume of water in sixth soil layer store [m3]
# ___ Parameters
# _____ c_p_t               T: rainfall aerial correction coefficient
# _____ c_p_c               C: evaporation decay parameter
# _____ c_p_h               H: quick runoff coefficient
# _____ c_p_s               S: drain flow parameter - fraction of saturation excess diverted to drain flow
# _____ c_p_d               D: soil outflow coefficient
# _____ c_p_z               Z: effective soil depth [mm]
# _____ c_p_sk              SK: surface routing parameter [hours]
# _____ c_p_fk              FK: inter flow routing parameter [hours]
# _____ c_p_gk              GK: groundwater routing parameter [hours]
# _____ c_p_rk              RK: river routing parameter [hours]
# ___ Outputs
# _____ c_out_aeva          actual evapotranspiration [mm]
# _____ c_out_q_h2o_ove     overland flow [m3/s]
# _____ c_out_q_h2o_dra     drain flow [m3/s]
# _____ c_out_q_h2o_int     inter flow [m3/s]
# _____ c_out_q_h2o_sgw     shallow groundwater flow [m3/s]
# _____ c_out_q_h2o_dgw     deep groundwater flow [m3/s]
# _____ c_out_q_h2o         total outflow [m3/s]
# _ Water Quality
# ___ Inputs
# _____ c_in_l_no3          nitrate loading on land [kg/ha/time step]
# _____ c_in_l_nh4          ammonia loading on land [kg/ha/time step]
# _____ c_in_l_dph          dissolved phosphorus loading on land [kg/ha/time step]
# _____ c_in_l_pph          particulate phosphorus loading on land [kg/ha/time step]
# _____ c_in_l_sed          sediment movable from land [kg/ha/time step]
# _____ c_in_temp           water temperature [degree celsius]
# ___ States
# _____ c_s_c_no3_ove       concentration of nitrate in overland store [kg/m3]
# _____ c_s_c_no3_dra       concentration of nitrate in drain store [kg/m3]
# _____ c_s_c_no3_int       concentration of nitrate in inter store [kg/m3]
# _____ c_s_c_no3_sgw       concentration of nitrate in shallow groundwater store [kg/m3]
# _____ c_s_c_no3_dgw       concentration of nitrate in deep groundwater store [kg/m3]
# _____ c_s_c_no3_soil      concentration of nitrate in whole soil column [kg/m3]
# _____ c_s_c_nh4_ove       concentration of ammonia in overland store [kg/m3]
# _____ c_s_c_nh4_dra       concentration of ammonia in drain store [kg/m3]
# _____ c_s_c_nh4_int       concentration of ammonia in inter store [kg/m3]
# _____ c_s_c_nh4_sgw       concentration of ammonia in shallow groundwater store [kg/m3]
# _____ c_s_c_nh4_dgw       concentration of ammonia in deep groundwater store [kg/m3]
# _____ c_s_c_nh4_soil      concentration of ammonia in whole soil column [kg/m3]
# _____ c_s_c_dph_ove       concentration of dissolved phosphorus in overland store [kg/m3]
# _____ c_s_c_dph_dra       concentration of dissolved phosphorus in drain store [kg/m3]
# _____ c_s_c_dph_int       concentration of dissolved phosphorus in inter store [kg/m3]
# _____ c_s_c_dph_sgw       concentration of dissolved phosphorus in shallow groundwater store [kg/m3]
# _____ c_s_c_dph_dgw       concentration of dissolved phosphorus in deep groundwater store [kg/m3]
# _____ c_s_c_dph_soil      concentration of dissolved phosphorus in whole soil column [kg/m3]
# _____ c_s_m_pph_ove       quantity of particulate phosphorus in overland store [kg]
# _____ c_s_m_pph_dra       quantity of particulate phosphorus in drain store [kg]
# _____ c_s_m_pph_int       quantity of particulate phosphorus in inter store [kg]
# _____ c_s_m_pph_sgw       quantity of particulate phosphorus in shallow groundwater store [kg]
# _____ c_s_m_pph_dgw       quantity of particulate phosphorus in deep groundwater store [kg]
# _____ c_s_m_pph_soil      quantity of particulate phosphorus in whole soil column [kg]
# _____ c_s_m_sed_ove       quantity of sediment in overland store [kg]
# _____ c_s_m_sed_dra       quantity of sediment in drain store [kg]
# _____ c_s_m_sed_int       quantity of sediment in inter store [kg]
# _____ c_s_m_sed_sgw       quantity of sediment in shallow groundwater store [kg]
# _____ c_s_m_sed_dgw       quantity of sediment in deep groundwater store [kg]
# _____ c_s_m_sed_soil      quantity of sediment in whole soil column [kg]
# ___ Parameters
# _____ c_p_att_no3         daily attenuation factor for nitrate
# _____ c_p_att_nh4         daily attenuation factor for ammonia
# _____ c_p_att_dph         daily attenuation factor for dissolved phosphorus
# _____ c_p_att_pph         daily attenuation factor for particulate phosphorus
# _____ c_p_att_sed         daily attenuation factor for sediment
# ___ Outputs
# _____ c_out_c_no3         nitrate concentration in outflow [kg/m3]
# _____ c_out_c_nh4         ammonia concentration in outflow [kg/m3]
# _____ c_out_c_dph         dissolved phosphorus in outflow [kg/m3]
# _____ c_out_c_pph         particulate phosphorus in outflow [kg/m3]
# _____ c_out_c_sed         sediment concentration in outflow [kg/m3]
# __________________
#

nb_soil_layers = 6.0  # number of layers in soil column
max_capacity_layer = 25.0  # maximum capacity of each layer (except the lowest)
area = 100.0  # catchment area in m2
time_step_min = 1440  # in minutes
time_step_sec = time_step_min * 60  # in seconds
time_factor = time_step_sec / 86400.0

volume_tolerance = 1.0E-8
flow_threshold_for_erosion = {
    'ove': 0.005,
    'dra': 0.05
}

stores = ['ove', 'dra', 'int', 'sgw', 'dgw', 'soil']
stores_contaminants = ['no3', 'nh4', 'dph', 'pph', 'sed']
soil_layers = ['ly1', 'ly2', 'ly3', 'ly4', 'ly5']
contaminants = ['no3', 'nh4', 'p_ino', 'p_ino_fb', 'p_org', 'p_org_fb', 'sed']

daily_sediment_threshold = 1.0
sediment_threshold = daily_sediment_threshold * time_factor
sediment_k = 1.0
sediment_p = 1.0
soil_test_p = 1.0

day_growing_season = 152.0
day_of_year = 1.0

# dictionaries to be used for 6 soil layers
dict_z_lyr = dict()
dict_lvl_lyr = dict()

# other dictionaries
dict_mass_applied = dict()
dict_att_factors = {
    'ove': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'dra': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'int': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'sgw': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'dgw': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0}
}
dict_mob_factors = {
    'ove': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'dra': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'int': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'sgw': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0},
    'dgw': {'no3': 1.0, 'nh4': 1.0, 'dph': 1.0, 'pph': 1.0, 'sed': 1.0}
}

# # 1. Hydrology
# # 1.1. Collect inputs, states, and parameters
c_in_rain = 1.0
c_in_peva = 1.0

c_s_v_h2o_ove = 1.0
c_s_v_h2o_dra = 1.0
c_s_v_h2o_int = 1.0
c_s_v_h2o_sgw = 1.0
c_s_v_h2o_dgw = 1.0

c_s_v_h2o_ly1 = 1.0
c_s_v_h2o_ly2 = 1.0
c_s_v_h2o_ly3 = 1.0
c_s_v_h2o_ly4 = 1.0
c_s_v_h2o_ly5 = 1.0
c_s_v_h2o_ly6 = 1.0

c_p_t = 1.0
c_p_c = 1.0
c_p_h = 1.0
c_p_s = 1.0
c_p_d = 1.0
c_p_z = 1.0
c_p_sk = 1.0
c_p_fk = 1.0
c_p_gk = 1.0
c_p_rk = 1.0

# # 1.2. Hydrological calculations

# all calculations in mm equivalent until further notice

# calculate capacity Z and level LVL of each layer (assumed equal) from effective soil depth
for i in [1, 2, 3, 4, 5, 6]:
    dict_z_lyr[i] = c_p_z / nb_soil_layers

dict_lvl_lyr[1] = c_s_v_h2o_ly1 / area * 1000  # factor 1000 to convert m in mm
dict_lvl_lyr[2] = c_s_v_h2o_ly2 / area * 1000  # factor 1000 to convert m in mm
dict_lvl_lyr[3] = c_s_v_h2o_ly3 / area * 1000  # factor 1000 to convert m in mm
dict_lvl_lyr[4] = c_s_v_h2o_ly4 / area * 1000  # factor 1000 to convert m in mm
dict_lvl_lyr[5] = c_s_v_h2o_ly5 / area * 1000  # factor 1000 to convert m in mm
dict_lvl_lyr[6] = c_s_v_h2o_ly6 / area * 1000  # factor 1000 to convert m in mm

# calculate cumulative level of rain in all soil layers at beginning of time step
lvl_total_start = 0.0
for i in [1, 2, 3, 4, 5, 6]:
    lvl_total_start += dict_lvl_lyr[i]

# apply parameter T to rainfall data
c_in_rain = c_in_rain * c_p_t
# calculate rainfall excess
excess_rain = c_in_rain - c_in_peva
# initialise actual evapotranspiration variable
c_out_aeva = 0.0

if excess_rain >= 0.0:  # excess rainfall available for runoff and infiltration
    # actual evapotranspiration = potential evapotranspiration
    c_out_aeva += c_in_peva
    # calculate surface runoff using H and Y parameters
    h_prime = c_p_h * (lvl_total_start / c_p_z)
    overland_flow = h_prime * excess_rain  # surface runoff
    excess_rain = excess_rain - overland_flow  # remainder that infiltrates
    # calculate percolation through soil layers
    for i in [1, 2, 3, 4, 5, 6]:
        space_in_lyr = dict_z_lyr[i] - dict_lvl_lyr[i]
        if space_in_lyr <= excess_rain:
            dict_lvl_lyr[i] += excess_rain
        else:
            dict_lvl_lyr[i] = dict_z_lyr[i]
            excess_rain -= space_in_lyr
    # calculate saturation excess from remaining excess rainfall after filling layers
    drain_flow = c_p_s * excess_rain
    inter_flow = (1.0 - c_p_s) * excess_rain
    # calculate leak from soil layers
    d_prime = c_p_d * (lvl_total_start / c_p_z)
    # leak to interflow
    for i in [1, 2, 3, 4, 5, 6]:
        leak_interflow = dict_lvl_lyr[i] * (d_prime ** i)
        if leak_interflow < dict_lvl_lyr[i]:
            inter_flow += leak_interflow
            dict_lvl_lyr[i] -= leak_interflow
    # leak to shallow groundwater flow
    shallow_flow = 0.0
    for i in [1, 2, 3, 4, 5, 6]:
        leak_shallow_flow = dict_lvl_lyr[i] * (d_prime / i)
        if leak_shallow_flow < dict_lvl_lyr[i]:
            shallow_flow += leak_shallow_flow
            dict_lvl_lyr[i] -= leak_shallow_flow
    # leak to deep groundwater flow
    power = 0.0
    deep_flow = 0.0
    for i in [6, 5, 4, 3, 2, 1]:
        power += 1.0
        leak_deep_flow = dict_lvl_lyr[i] * (d_prime ** power)
        if leak_deep_flow < dict_lvl_lyr[i]:
            deep_flow += leak_deep_flow
            dict_lvl_lyr[i] -= leak_deep_flow
else:  # no excess rainfall
    overland_flow = 0.0  # no quick overland flow
    drain_flow = 0.0  # no quick drain flow
    inter_flow = 0.0  # no quick + leak interflow
    shallow_flow = 0.0  # no shallow groundwater flow
    deep_flow = 0.0

    deficit_rain = - excess_rain
    c_out_aeva += c_in_rain
    for i in [1, 2, 3, 4, 5, 6]:
        if dict_lvl_lyr[i] >= deficit_rain:
            dict_lvl_lyr[i] -= deficit_rain
            c_out_aeva += deficit_rain
            deficit_rain = 0.0
        else:
            c_out_aeva += dict_lvl_lyr[i]
            deficit_rain = c_p_c * (deficit_rain - dict_lvl_lyr[i])
            dict_lvl_lyr[i] = 0.0

# calculate cumulative level of rain in all soil layers at end of time step
lvl_total_end = 0.0
for i in [1, 2, 3, 4, 5, 6]:
    lvl_total_end += dict_lvl_lyr[i]

# all calculations in S.I. units now

# route overland flow (direct runoff)
c_out_q_h2o_ove = c_s_v_h2o_ove / c_p_sk  # [m3/s]
c_s_v_h2o_ove_old = c_s_v_h2o_ove
c_s_v_h2o_ove += (overland_flow / 1000 * area) - (c_out_q_h2o_ove * time_step_sec)  # [m3] - [m3]
if c_s_v_h2o_ove < 0.0:
    c_s_v_h2o_ove = 0.0
# route drain flow
c_out_q_h2o_dra = c_s_v_h2o_dra / c_p_sk  # [m3/s]
c_s_v_h2o_dra_old = c_s_v_h2o_dra
c_s_v_h2o_dra += (drain_flow / 1000 * area) - (c_out_q_h2o_dra * time_step_sec)  # [m3] - [m3]
if c_s_v_h2o_dra < 0.0:
    c_s_v_h2o_dra = 0.0
# route interflow
c_out_q_h2o_int = c_s_v_h2o_int / c_p_fk  # [m3/s]
c_s_v_h2o_int_old = c_s_v_h2o_int
c_s_v_h2o_int += (inter_flow / 1000 * area) - (c_out_q_h2o_int * time_step_sec)  # [m3] - [m3]
if c_s_v_h2o_int < 0.0:
    c_s_v_h2o_int = 0.0
# route shallow groundwater flow
c_out_q_h2o_sgw = c_s_v_h2o_sgw / c_p_gk  # [m3/s]
c_s_v_h2o_sgw_old = c_s_v_h2o_sgw
c_s_v_h2o_sgw += (inter_flow / 1000 * area) - (c_out_q_h2o_sgw * time_step_sec)  # [m3] - [m3]
if c_s_v_h2o_sgw < 0.0:
    c_s_v_h2o_sgw = 0.0
# route deep groundwater flow
c_out_q_h2o_dgw = c_s_v_h2o_dgw / c_p_gk  # [m3/s]
c_s_v_h2o_dgw_old = c_s_v_h2o_dgw
c_s_v_h2o_dgw += (inter_flow / 1000 * area) - (c_out_q_h2o_dgw * time_step_sec)  # [m3] - [m3]
if c_s_v_h2o_dgw < 0.0:
    c_s_v_h2o_dgw = 0.0
# calculate total outflow
c_out_q_h2o = c_out_q_h2o_ove + c_out_q_h2o_dra + c_out_q_h2o_int + c_out_q_h2o_sgw + c_out_q_h2o_dgw  # [m3/s]

# convert moisture of soil layers from mm into m3
c_s_v_h2o_ly1 = dict_lvl_lyr[1] / 1000 * area
c_s_v_h2o_ly2 = dict_lvl_lyr[2] / 1000 * area
c_s_v_h2o_ly3 = dict_lvl_lyr[3] / 1000 * area
c_s_v_h2o_ly4 = dict_lvl_lyr[4] / 1000 * area
c_s_v_h2o_ly5 = dict_lvl_lyr[5] / 1000 * area

# store states and outputs in dictionaries for use in water quality calculations
dict_states_old_hd = {
    'ove': c_s_v_h2o_ove_old,
    'dra': c_s_v_h2o_dra_old,
    'int': c_s_v_h2o_int_old,
    'sgw': c_s_v_h2o_sgw_old,
    'dgw': c_s_v_h2o_dgw_old
}

dict_states_hd = {
    'ove': c_s_v_h2o_ove,
    'dra': c_s_v_h2o_dra,
    'int': c_s_v_h2o_int,
    'sgw': c_s_v_h2o_sgw,
    'dgw': c_s_v_h2o_dgw
}

dict_flows_mm_hd = {
    'ove': overland_flow,
    'dra': drain_flow,
    'int': inter_flow,
    'sgw': shallow_flow,
    'dgw': deep_flow
}

dict_outputs_hd = {
    'ove': c_out_q_h2o_ove,
    'dra': c_out_q_h2o_dra,
    'int': c_out_q_h2o_int,
    'sgw': c_out_q_h2o_sgw,
    'dgw': c_out_q_h2o_dgw
}

# # 2. Water quality calculations
# # 2.1. Collect inputs, states, and parameters

c_in_l_no3 = 1.0
c_in_l_nh4 = 1.0
c_in_l_dph = 1.0
c_in_l_pph = 1.0
c_in_l_sed = 1.0
dict_mass_applied['no3'] = c_in_l_no3 * area * 1.0e-4  # area in m2 converted into ha
dict_mass_applied['nh4'] = c_in_l_nh4 * area * 1.0e-4  # area in m2 converted into ha
dict_mass_applied['dph'] = c_in_l_dph * area * 1.0e-4  # area in m2 converted into ha
dict_mass_applied['pph'] = c_in_l_pph * area * 1.0e-4  # area in m2 converted into ha
dict_mass_applied['sed'] = c_in_l_sed * area * 1.0e-4  # area in m2 converted into ha
c_in_temp = 1.0

dict_states_wq = dict()
dict_c_outflow = dict()
for store in stores:
    my_dict = dict()
    my_dict_2 = dict()
    for contaminant in stores_contaminants:
        my_dict[contaminant] = 1.0
        my_dict_2[contaminant] = 0.0
    dict_states_wq[store] = my_dict[:]
    dict_c_outflow[store] = my_dict_2[:]

c_p_att_no3 = 1.0
c_p_att_nh4 = 1.0
c_p_att_dph = 1.0
c_p_att_pph = 1.0
c_p_att_sed = 1.0
# adapt daily attenuation factors to actual time step
if time_factor < 0.005:
    time_factor = 0.005
dict_att_factors['no3'] = c_p_att_no3 * time_factor
dict_att_factors['nh4'] = c_p_att_nh4 * time_factor
dict_att_factors['dph'] = c_p_att_dph * time_factor
dict_att_factors['ddp'] = c_p_att_pph * time_factor
dict_att_factors['sed'] = c_p_att_sed * time_factor

# # 2.2. Water quality calculations
# # 2.2.1. Overland flow contamination & drain flow contamination
for store in ['ove', 'dra']:
    # nitrate, ammonia, dissolved phosphorus (dissolved pollutants)
    for contaminant in ['no3', 'nh4', 'dph']:
        c_store = dict_states_wq[store][contaminant]
        m_store = c_store * dict_states_old_hd[store]
        dict_c_outflow[store][contaminant] = c_store
        attenuation = dict_att_factors[store][contaminant]
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_store_att = m_store * attenuation
        mobilisation = dict_mob_factors[store][contaminant]
        if (mobilisation < 0.0) or (mobilisation > 1.0):
            mobilisation = 1.0
        m_mobilised = (dict_flows_mm_hd[store] / 1000 * area) * dict_states_wq['soil'][contaminant] * mobilisation
        m_store = m_store_att + m_mobilised - dict_outputs_hd[store] * c_store
        if (m_store < 0.0) or (dict_states_hd[store] < volume_tolerance):
            dict_states_wq[store][contaminant] = 0.0
        else:
            dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]

    # sediment
    contaminant = 'sed'
    m_store = dict_states_wq[store][contaminant]
    attenuation = dict_att_factors[store][contaminant]
    if attenuation > 1.0:
        attenuation = 1.0
    elif attenuation < 0.0:
        attenuation = 0.0
    m_store_att = m_store * attenuation
    m_sediment_per_area = float()
    m_sediment = float()
    if (dict_flows_mm_hd[store] < sediment_threshold) or (dict_flows_mm_hd[store] < flow_threshold_for_erosion[store]):
        m_sediment = 0.0
        dict_c_outflow[store][contaminant] = 0.0
    else:
        m_sediment_per_area = (sediment_k * dict_flows_mm_hd[store] ** sediment_p) * time_factor
        m_sediment = m_sediment_per_area * area
        dict_c_outflow[store][contaminant] = m_sediment / (dict_flows_mm_hd[store] / 1000 * area)
    if store == 'ove':
        dict_states_wq[store][contaminant] = 0.0  # all sediment assumed gone
    else:  # 'dra' store
        m_store = m_store_att + m_sediment - dict_outputs_hd[store] * dict_c_outflow[store][contaminant]
        if (m_store < 0.0) or (dict_states_hd[store] < volume_tolerance):
            dict_states_wq[store][contaminant] = 0.0
        else:
            dict_states_wq[store][contaminant] = m_store

    # particulate phosphorus (firmly bound phosphorus)
    contaminant = 'pph'
    c_store = dict_states_wq[store][contaminant]
    m_store = c_store * dict_states_old_hd[store]
    attenuation = dict_att_factors[store][contaminant]
    if attenuation > 1.0:
        attenuation = 1.0
    elif attenuation < 0.0:
        attenuation = 0.0
    m_store_att = m_store * attenuation
    m_particulate_p = float()
    if (overland_flow < sediment_threshold) or (dict_flows_mm_hd[store] < 0.005):
        m_particulate_p = 0.0
        dict_c_outflow[store][contaminant] = 0.0
    else:
        soil_loss = m_sediment_per_area * 1e4  # [kg/ha]
        p_enrichment_ratio = math.exp(2.48 - 0.27 * math.log1p(soil_loss))  # [-]
        if p_enrichment_ratio < 0.1:
            p_enrichment_ratio = 0.1
        elif p_enrichment_ratio > 6.0:
            p_enrichment_ratio = 6.0
        m_particulate_p = soil_test_p * m_sediment * p_enrichment_ratio  # [kg]
        m_particulate_p_missing = float()  # [kg]
        if m_particulate_p < dict_states_wq['soil'][contaminant]:
            dict_states_wq['soil'][contaminant] -= m_particulate_p
            m_particulate_p_missing = 0.0
        else:
            m_particulate_p_missing = m_particulate_p - dict_states_wq['soil'][contaminant]
            dict_states_wq['soil'][contaminant] = 0.0
        m_particulate_p -= m_particulate_p_missing
        dict_c_outflow[store][contaminant] = m_particulate_p / (dict_flows_mm_hd[store] / 1000 * area)
    m_store = m_store_att + m_particulate_p - dict_outputs_hd[store] * c_store
    if (m_store < 0.0) or (dict_states_hd[store] < volume_tolerance):
        dict_states_wq[store][contaminant] = 0.0
    else:
        dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]

# # 2.2.2. Interflow contamination
for store in ['int', 'sgw', 'dgw']:
    for contaminant in stores_contaminants:
        c_store = dict_states_wq[store][contaminant]
        m_store = c_store * dict_states_old_hd[store]
        dict_c_outflow[store][contaminant] = c_store
        attenuation = dict_att_factors[store][contaminant]
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_store_att = m_store * attenuation
        mobilisation = dict_mob_factors[store][contaminant]
        if (mobilisation < 0.0) or (mobilisation > 1.0):
            mobilisation = 1.0
        m_mobilised = (dict_flows_mm_hd[store] / 1000 * area) * dict_states_wq['soil'][contaminant] * mobilisation
        m_store = m_store_att + m_mobilised - dict_outputs_hd[store] * c_store
        if (m_store < 0.0) or (dict_states_hd[store] < volume_tolerance):
            dict_states_wq[store][contaminant] = 0.0
        else:
            dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]

# # 2.2.3. Soil store contamination

# soil constants
cst_c1n = 1.0
cst_c3n = 1.0
cst_c4n = 1.0
cst_c5n = 1.0
cst_c6n = 1.0
cst_c7n = 1.0
cst_c1p = 1.0
cst_c2p = 1.0
cst_c3p = 1.0
cst_c4p = 1.0
cst_c5p = 1.0
cst_c6p = 1.0
cst_c7p = 1.0
cst_c8p = 1.0

# nitrate
# s1: soil moisture factor
s1 = lvl_total_end / (c_p_z * 0.275)
# assuming field capacity = 110 mm/m depth & soil porosity = 0.4 => 0.11 * 0.4 = 0.275 (SMD max assumed by Met Eireann)
if s1 > 1.0:
    s1 = 1.0
elif s1 < 0.0:
    s1 = 0.0
# s2: seasonal plant growth index
s2 = 0.66 + 0.34 * math.sin(2 * math.pi * (day_of_year - day_growing_season) / 365)
# pu: plant uptake
c3 = cst_c3n * (1.047 ** (c_in_temp - 20.0))
pu_no3 = c3 * s1 * s2
# dn: denitrification / ni: nitrification / fx: fixation
c1 = cst_c1n * (1.047 ** (c_in_temp - 20.0))
c4 = cst_c4n * (1.047 ** (c_in_temp - 20.0))
if c_in_temp < 0.0:
    dn = 0.0  # no denitrification
    ni = 0.0  # no nitrification
    fx = 0.0  # no fixation
else:
    dn = c1 * s1
    ni = c4 * s1 * 1.0
