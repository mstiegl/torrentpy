# -*- coding: utf-8 -*-

# This file is part of TORRENTpy - An open-source tool for TranspORt thRough the catchmEnt NeTwork
# Copyright (C) 2018  Thibault Hallouin (1), Eva Mockler (1,2), Michael Bruen (1)
#
# (1) Dooge Centre for Water Resources Research, University College Dublin, Ireland
# (2) Environmental Protection Agency, Ireland
#
# TORRENTpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TORRENTpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TORRENTpy. If not, see <http://www.gnu.org/licenses/>.

from math import exp, log, sin, pi
from datetime import timedelta
from calendar import isleap
import os
import csv

from ..model import Model
from ...inout import open_csv_wb, open_csv_ab


class INCAc(Model):
    def __init__(self, category, identifier):
        Model.__init__(self, category, identifier)
        # set model variables names
        self.inputs_names = ['c_in_temp', 'c_in_m_no3', 'c_in_m_nh4', 'c_in_m_p_ino', 'c_in_m_o_org']
        self.parameters_names = ['c_p_att_no3_ove', 'c_p_att_nh4_ove', 'c_p_att_dph_ove', 'c_p_att_pph_ove',
                                 'c_p_att_sed_ove', 'c_p_att_no3_dra', 'c_p_att_nh4_dra', 'c_p_att_dph_dra',
                                 'c_p_att_pph_dra', 'c_p_att_sed_dra', 'c_p_att_no3_int', 'c_p_att_nh4_int',
                                 'c_p_att_dph_int', 'c_p_att_pph_int', 'c_p_att_sed_int', 'c_p_att_no3_sgw',
                                 'c_p_att_nh4_sgw', 'c_p_att_dph_sgw', 'c_p_att_pph_sgw', 'c_p_att_sed_sgw',
                                 'c_p_att_no3_dgw', 'c_p_att_nh4_dgw', 'c_p_att_dph_dgw', 'c_p_att_pph_dgw',
                                 'c_p_att_sed_dgw', 'c_p_att_no3_soil', 'c_p_att_nh4_soil', 'c_p_att_p_org_ra_soil',
                                 'c_p_att_p_ino_ra_soil', 'c_p_att_p_org_fb_soil', 'c_p_att_p_ino_fb_soil',
                                 'c_p_att_sed_soil']
        self.states_names = ['c_s_c_no3_ove', 'c_s_c_no3_dra', 'c_s_c_no3_int', 'c_s_c_no3_sgw', 'c_s_c_no3_dgw',
                             'c_s_c_nh4_ove', 'c_s_c_nh4_dra', 'c_s_c_nh4_int', 'c_s_c_nh4_sgw', 'c_s_c_nh4_dgw',
                             'c_s_c_dph_ove', 'c_s_c_dph_dra', 'c_s_c_dph_int', 'c_s_c_dph_sgw', 'c_s_c_dph_dgw',
                             'c_s_c_pph_ove', 'c_s_c_pph_dra', 'c_s_c_pph_int', 'c_s_c_pph_sgw', 'c_s_c_pph_dgw',
                             'c_s_c_sed_ove', 'c_s_c_sed_dra', 'c_s_c_sed_int', 'c_s_c_sed_sgw', 'c_s_c_sed_dgw',
                             'c_s_c_no3_soil', 'c_s_c_nh4_soil', 'c_s_c_p_org_ra_soil', 'c_s_c_p_ino_ra_soil',
                             'c_s_m_p_org_fb_soil', 'c_s_m_p_ino_fb_soil', 'c_s_m_sed_soil']
        self.constants_names = ['c_cst_mob_no3_ove', 'c_cst_mob_no3_dra', 'c_cst_mob_no3_int', 'c_cst_mob_no3_sgw',
                                'c_cst_mob_no3_dgw', 'c_cst_mob_nh4_ove', 'c_cst_mob_nh4_dra', 'c_cst_mob_nh4_int',
                                'c_cst_mob_nh4_sgw', 'c_cst_mob_nh4_dgw', 'c_cst_mob_dph_ove', 'c_cst_mob_dph_dra',
                                'c_cst_mob_dph_int', 'c_cst_mob_dph_sgw', 'c_cst_mob_dph_dgw', 'c_cst_mob_pph_ove',
                                'c_cst_mob_pph_dra', 'c_cst_mob_pph_int', 'c_cst_mob_pph_sgw', 'c_cst_mob_pph_dgw',
                                'c_cst_mob_sed_ove', 'c_cst_mob_sed_dra', 'c_cst_mob_sed_int', 'c_cst_mob_sed_sgw',
                                'c_cst_mob_sed_dgw', 'c_cst_sed_daily_thr', 'c_cst_sed_k', 'c_cst_sed_p',
                                'c_cst_soil_test_p', 'c_cst_soil_c1n', 'c_cst_soil_c3n', 'c_cst_soil_c4n',
                                'c_cst_soil_c5n', 'c_cst_soil_c6n', 'c_cst_soil_c7n', 'c_cst_soil_c1p',
                                'c_cst_soil_c2p', 'c_cst_soil_c3p', 'c_cst_soil_c4p', 'c_cst_soil_c5p',
                                'c_cst_soil_c6p', 'c_cst_soil_c7p', 'c_cst_soil_c8p', 'c_cst_day_grow',
                                'c_cst_flow_tolerance', 'c_cst_vol_tolerance', 'c_cst_flow_thr_mm_for_ero_ove',
                                'c_cst_flow_thr_mm_for_ero_dra']
        self.outputs_names = ['c_out_c_no3_ove', 'c_out_c_nh4_ove', 'c_out_c_dph_ove', 'c_out_c_pph_ove',
                              'c_out_c_sed_ove', 'c_out_c_no3_dra', 'c_out_c_nh4_dra', 'c_out_c_dph_dra',
                              'c_out_c_pph_dra', 'c_out_c_sed_dra', 'c_out_c_no3_int', 'c_out_c_nh4_int',
                              'c_out_c_dph_int', 'c_out_c_pph_int', 'c_out_c_sed_int', 'c_out_c_no3_sgw',
                              'c_out_c_nh4_sgw', 'c_out_c_dph_sgw', 'c_out_c_pph_sgw', 'c_out_c_sed_sgw',
                              'c_out_c_no3_dgw', 'c_out_c_nh4_dgw', 'c_out_c_dph_dgw', 'c_out_c_pph_dgw',
                              'c_out_c_sed_dgw', 'c_out_c_no3', 'c_out_c_nh4', 'c_out_c_dph', 'c_out_c_pph',
                              'c_out_c_sed']

    def set_constants(self, input_folder):
        self._set_constants_with_file(input_folder)

    def set_parameters(self, link, catchment, outlet, input_folder, output_folder):
        if os.path.isfile("{}{}_{}.{}{}.parameters".format(
                input_folder, catchment, outlet, self.identifier, self.category)):
            self._set_parameters_with_file(link, catchment, outlet, input_folder)
        else:
            self._infer_parameters(link, catchment, outlet, output_folder)

    def _infer_parameters(self, link, catchment, outlet, output_folder):

        dict_for_file = self._infer_parameters_from_descriptors(link.descriptors)

        my_dict = dict(dict_for_file)
        dict_for_file["WaterBody"] = link.name

        if os.path.isfile('{}{}_{}.{}{}.parameters'.format(output_folder, catchment, outlet,
                                                           self.identifier, self.category)):
            with open_csv_ab('{}{}_{}.{}{}.parameters'.format(output_folder, catchment, outlet,
                                                              self.identifier, self.category)) as my_file:
                header = ["WaterBody"] + self.parameters_names
                my_writer = csv.DictWriter(my_file, fieldnames=header)
                my_writer.writerow(dict_for_file)
        else:
            with open_csv_wb('{}{}_{}.{}{}.parameters'.format(output_folder, catchment, outlet,
                                                              self.identifier, self.category)) as my_file:
                header = ["WaterBody"] + self.parameters_names
                my_writer = csv.DictWriter(my_file, fieldnames=header)
                my_writer.writeheader()
                my_writer.writerow(dict_for_file)

        self.parameters = my_dict
        link.models_parameters.update(my_dict)

    def initialise(self, link):

        return self._initialise_states()

    def simulate(self, db, tf, step, link, logger):

        self._simulate(link.name, link.descriptors,
                       step, tf.simu_gap,
                       link.models_parameters, self.constants,
                       db.simulation, db.meteo, db.contamination,
                       logger)

    def _simulate(self, waterbody, dict_desc,
                  datetime_time_step, time_gap,
                  dict_param, dict_const,
                  dict_data_frame, dict_meteo, dict_loads,
                  logger):

        inca_in = self._get_in(waterbody, datetime_time_step, time_gap,
                               dict_data_frame, dict_desc, dict_param, dict_meteo, dict_loads, dict_const)

        inca_out = self._run(waterbody, datetime_time_step, logger, *inca_in)

        self._get_out(waterbody, datetime_time_step, dict_data_frame, *inca_out)

    @staticmethod
    def _run(waterbody, datetime_time_step, logger,
             area_m2, time_gap_sec,
             c_in_temp, c_in_m_no3, c_in_m_nh4, c_in_m_p_ino, c_in_m_p_org,
             c_p_att_no3_ove, c_p_att_nh4_ove, c_p_att_dph_ove, c_p_att_pph_ove, c_p_att_sed_ove,
             c_p_att_no3_dra, c_p_att_nh4_dra, c_p_att_dph_dra, c_p_att_pph_dra, c_p_att_sed_dra,
             c_p_att_no3_int, c_p_att_nh4_int, c_p_att_dph_int, c_p_att_pph_int, c_p_att_sed_int,
             c_p_att_no3_sgw, c_p_att_nh4_sgw, c_p_att_dph_sgw, c_p_att_pph_sgw, c_p_att_sed_sgw,
             c_p_att_no3_dgw, c_p_att_nh4_dgw, c_p_att_dph_dgw, c_p_att_pph_dgw, c_p_att_sed_dgw,
             c_p_att_no3_soil, c_p_att_nh4_soil, c_p_att_p_org_ra_soil, c_p_att_p_ino_ra_soil,
             c_p_att_p_org_fb_soil, c_p_att_p_ino_fb_soil, c_p_att_sed_soil,
             c_s_c_no3_ove, c_s_c_nh4_ove, c_s_c_dph_ove, c_s_c_pph_ove, c_s_c_sed_ove,
             c_s_c_no3_dra, c_s_c_nh4_dra, c_s_c_dph_dra, c_s_c_pph_dra, c_s_c_sed_dra,
             c_s_c_no3_int, c_s_c_nh4_int, c_s_c_dph_int, c_s_c_pph_int, c_s_c_sed_int,
             c_s_c_no3_sgw, c_s_c_nh4_sgw, c_s_c_dph_sgw, c_s_c_pph_sgw, c_s_c_sed_sgw,
             c_s_c_no3_dgw, c_s_c_nh4_dgw, c_s_c_dph_dgw, c_s_c_pph_dgw, c_s_c_sed_dgw,
             c_s_c_no3_soil, c_s_c_nh4_soil, c_s_c_p_org_ra_soil, c_s_c_p_ino_ra_soil,
             c_s_m_p_org_fb_soil, c_s_m_p_ino_fb_soil, c_s_m_sed_soil,
             c_cst_mob_no3_ove, c_cst_mob_nh4_ove, c_cst_mob_dph_ove, c_cst_mob_pph_ove, c_cst_mob_sed_ove,
             c_cst_mob_no3_dra, c_cst_mob_nh4_dra, c_cst_mob_dph_dra, c_cst_mob_pph_dra, c_cst_mob_sed_dra,
             c_cst_mob_no3_int, c_cst_mob_nh4_int, c_cst_mob_dph_int, c_cst_mob_pph_int, c_cst_mob_sed_int,
             c_cst_mob_no3_sgw, c_cst_mob_nh4_sgw, c_cst_mob_dph_sgw, c_cst_mob_pph_sgw, c_cst_mob_sed_sgw,
             c_cst_mob_no3_dgw, c_cst_mob_nh4_dgw, c_cst_mob_dph_dgw, c_cst_mob_pph_dgw, c_cst_mob_sed_dgw,
             c_cst_sed_daily_thr, c_cst_sed_k, c_cst_sed_p, c_cst_soil_test_p,
             c_cst_soil_c1n, c_cst_soil_c3n, c_cst_soil_c4n, c_cst_soil_c5n, c_cst_soil_c6n, c_cst_soil_c7n,
             c_cst_soil_c1p, c_cst_soil_c2p, c_cst_soil_c3p, c_cst_soil_c4p, c_cst_soil_c5p, c_cst_soil_c6p,
             c_cst_soil_c7p, c_cst_soil_c8p, c_cst_day_grow, c_cst_flow_tolerance, c_cst_vol_tolerance,
             c_cst_flow_thr_mm_for_ero_ove, c_cst_flow_thr_mm_for_ero_dra,
             # inheritance from hydrological model
             c_p_z, c_out_q_h2o_ove, c_out_q_h2o_dra, c_out_q_h2o_int, c_out_q_h2o_sgw, c_out_q_h2o_dgw,
             c_s_v_h2o_ove_old, c_s_v_h2o_dra_old, c_s_v_h2o_int_old, c_s_v_h2o_sgw_old, c_s_v_h2o_dgw_old,
             c_s_v_h2o_ove, c_s_v_h2o_dra, c_s_v_h2o_int, c_s_v_h2o_sgw, c_s_v_h2o_dgw,
             lvl_total_start, lvl_total_end,
             c_pr_eff_rain_to_ove, c_pr_eff_rain_to_dra, c_pr_eff_rain_to_int,
             c_pr_eff_rain_to_sgw, c_pr_eff_rain_to_dgw):
        """
        This function was written by Thibault Hallouin but is largely inspired by the work of Eva Mockler and
        Michael Bruen, namely for the work published in: Mockler, E., Bruen, M., Desta, M., Misstear, B., Environmental
        Protection Agency, Ireland, 2014. Pathways Project Final Report Volume 4: Catchment Modelling Tool
        (STRIVE Report). Dublin.

        The INCA model was developed by researchers at the Department of Geography and Environmental Science of the
        University of Reading, United Kingdom: http://www.reading.ac.uk/geographyandenvironmentalscience/research/INCA/

        Wade, A.J., Durand, P., Beaujouan, V., Wessel, W.W., Raat, K.J., Whitehead, P.G., Butterfield, D., Rankinen, K.
        and Lepisto, A. (2002) A nitrogen model for European catchments: INCA, new model structure and equations,
        Hydrology and Earth System Sciences, 6, 559-582.

        Wade, A. J., Whitehead, P. G. and Butterfield, D. (2002) The Integrated Catchments model of Phosphorus dynamics
        (INCA-P), a new approach for multiple source assessment in heterogeneous river systems: model structure and
        equations, Hydrology and Earth Systems Sciences, 6, 583-606.

        Catchment Constants
        _ area_m2                   catchment area [m2]
        _ time_gap_sec              time gap between two simulation time steps [seconds]

        Catchment Model * c_ *
        _ Water Quality
        ___ Inputs * in_ *
        _____ c_in_temp             soil temperature [degree celsius]
        _____ c_in_m_no3            nitrate loading on land [kg/time step]
        _____ c_in_m_nh4            ammonia loading on land [kg/time step]
        _____ c_in_m_p_ino          inorganic phosphorus loading on land [kg/time step]
        _____ c_in_m_p_org          organic phosphorus loading on land [kg/time step]
        ___ Parameters * p_ *
        _____ c_p_att_no3_ove       daily attenuation factor for nitrate in overland flow [-]
        _____ c_p_att_nh4_ove       daily attenuation factor for ammonia in overland flow [-]
        _____ c_p_att_dph_ove       daily attenuation factor for dissolved phosphorus in overland flow [-]
        _____ c_p_att_pph_ove       daily attenuation factor for particulate phosphorus in overland flow [-]
        _____ c_p_att_sed_ove       daily attenuation factor for sediment in overland flow [-]
        _____ c_p_att_no3_dra       daily attenuation factor for nitrate in drain flow [-]
        _____ c_p_att_nh4_dra       daily attenuation factor for ammonia in drain flow [-]
        _____ c_p_att_dph_dra       daily attenuation factor for dissolved phosphorus in drain flow [-]
        _____ c_p_att_pph_dra       daily attenuation factor for particulate phosphorus in drain flow [-]
        _____ c_p_att_sed_dra       daily attenuation factor for sediment in drain flow [-]
        _____ c_p_att_no3_int       daily attenuation factor for nitrate in inter flow [-]
        _____ c_p_att_nh4_int       daily attenuation factor for ammonia in inter flow [-]
        _____ c_p_att_dph_int       daily attenuation factor for dissolved phosphorus in inter flow [-]
        _____ c_p_att_pph_int       daily attenuation factor for particulate phosphorus in inter flow [-]
        _____ c_p_att_sed_int       daily attenuation factor for sediment in inter flow [-]
        _____ c_p_att_no3_sgw       daily attenuation factor for nitrate in shallow groundwater flow [-]
        _____ c_p_att_nh4_sgw       daily attenuation factor for ammonia in shallow groundwater flow [-]
        _____ c_p_att_dph_sgw       daily attenuation factor for dissolved phosphorus in shallow groundwater flow [-]
        _____ c_p_att_pph_sgw       daily attenuation factor for particulate phosphorus in shallow groundwater flow [-]
        _____ c_p_att_sed_sgw       daily attenuation factor for sediment in shallow groundwater flow [-]
        _____ c_p_att_no3_dgw       daily attenuation factor for nitrate in deep groundwater flow [-]
        _____ c_p_att_nh4_dgw       daily attenuation factor for ammonia in deep groundwater flow [-]
        _____ c_p_att_dph_dgw       daily attenuation factor for dissolved phosphorus in deep groundwater flow [-]
        _____ c_p_att_pph_dgw       daily attenuation factor for particulate phosphorus in deep groundwater flow [-]
        _____ c_p_att_sed_dgw       daily attenuation factor for sediment in deep groundwater flow [-]
        _____ c_p_att_no3_soil      daily attenuation factor for nitrate in soil column [-]
        _____ c_p_att_nh4_soil      daily attenuation factor for ammonia in soil column [-]
        _____ c_p_att_p_org_ra_soil daily attenuation factor for readily available organic phosphorus in soil column [-]
        _____ c_p_att_p_ino_ra_soil daily attenuation factor for readily available inorg. phosphorus in soil column [-]
        _____ c_p_att_p_org_fb_soil daily attenuation factor for firmly bound organic phosphorus in soil column [-]
        _____ c_p_att_p_ino_fb_soil daily attenuation factor for firmly bound inorganic phosphorus in soil column [-]
        _____ c_p_att_sed_soil      daily attenuation factor for sediment in soil column [-]
        ___ States * s_ *
        _____ c_s_c_no3_ove         concentration of nitrate in overland store [kg/m3]
        _____ c_s_c_nh4_ove         concentration of ammonia in overland store [kg/m3]
        _____ c_s_c_dph_ove         concentration of dissolved phosphorus in overland store [kg/m3]
        _____ c_s_c_pph_ove         concentration of particulate phosphorus in overland store [kg/m3]
        _____ c_s_c_sed_ove         concentration of sediment in overland store [kg/m3]
        _____ c_s_c_no3_dra         concentration of nitrate in drain store [kg/m3]
        _____ c_s_c_nh4_dra         concentration of ammonia in drain store [kg/m3]
        _____ c_s_c_dph_dra         concentration of dissolved phosphorus in drain store [kg/m3]
        _____ c_s_c_pph_dra         concentration of particulate phosphorus in drain store [kg/m3]
        _____ c_s_c_sed_dra         concentration of sediment in drain store [kg/m3]
        _____ c_s_c_no3_int         concentration of nitrate in inter store [kg/m3]
        _____ c_s_c_nh4_int         concentration of ammonia in inter store [kg/m3]
        _____ c_s_c_dph_int         concentration of dissolved phosphorus in inter store [kg/m3]
        _____ c_s_c_pph_int         concentration of particulate phosphorus in inter store [kg/m3]
        _____ c_s_c_sed_int         concentration of sediment in inter store [kg/m3]
        _____ c_s_c_no3_sgw         concentration of nitrate in shallow groundwater store [kg/m3]
        _____ c_s_c_nh4_sgw         concentration of ammonia in shallow groundwater store [kg/m3]
        _____ c_s_c_dph_sgw         concentration of dissolved phosphorus in shallow groundwater store [kg/m3]
        _____ c_s_c_pph_sgw         concentration of particulate phosphorus in shallow groundwater store [kg/m3]
        _____ c_s_c_sed_sgw         concentration of sediment in shallow groundwater store [kg/m3]
        _____ c_s_c_no3_dgw         concentration of nitrate in deep groundwater store [kg/m3]
        _____ c_s_c_nh4_dgw         concentration of ammonia in deep groundwater store [kg/m3]
        _____ c_s_c_dph_dgw         concentration of dissolved phosphorus in deep groundwater store [kg/m3]
        _____ c_s_c_pph_dgw         concentration of particulate phosphorus in deep groundwater store [kg/m3]
        _____ c_s_c_sed_dgw         concentration of sediment in deep groundwater store [kg/m3]
        _____ c_s_c_no3_soil        concentration of nitrate in soil column [kg/m3]
        _____ c_s_c_nh4_soil        concentration of ammonia in soil column [kg/m3]
        _____ c_s_c_p_org_ra_soil   concentration of readily available organic phosphorus in soil column [kg/m3]
        _____ c_s_c_p_ino_ra_soil   concentration of readily available inorganic phosphorus in soil column [kg/m3]
        _____ c_s_m_p_org_fb_soil   mass of firmly bound organic phosphorus in soil column [kg]
        _____ c_s_m_p_ino_fb_soil   mass of firmly bound inorganic phosphorus in soil column [kg]
        _____ c_s_m_sed_soil        mass of sediment in soil column [kg]

        ___ Constants * cst_ *
        _____ c_cst_mob_no3_ove     mobilisation factor for nitrate to overland flow [-]
        _____ c_cst_mob_nh4_ove     mobilisation factor for ammonia to overland flow [-]
        _____ c_cst_mob_dph_ove     mobilisation factor for dissolved phosphorus to overland flow [-]
        _____ c_cst_mob_pph_ove     mobilisation factor for particulate phosphorus to overland flow [-]
        _____ c_cst_mob_sed_ove     mobilisation factor for sediment to overland flow [-]
        _____ c_cst_mob_no3_dra     mobilisation factor for nitrate to drain flow [-]
        _____ c_cst_mob_nh4_dra     mobilisation factor for ammonia to drain flow [-]
        _____ c_cst_mob_dph_dra     mobilisation factor for dissolved phosphorus to drain flow [-]
        _____ c_cst_mob_pph_dra     mobilisation factor for particulate phosphorus to drain flow [-]
        _____ c_cst_mob_sed_dra     mobilisation factor for sediment to drain flow [-]
        _____ c_cst_mob_no3_int     mobilisation factor for nitrate to inter flow [-]
        _____ c_cst_mob_nh4_int     mobilisation factor for ammonia to inter flow [-]
        _____ c_cst_mob_dph_int     mobilisation factor for dissolved phosphorus to inter flow [-]
        _____ c_cst_mob_pph_int     mobilisation factor for particulate phosphorus to inter flow [-]
        _____ c_cst_mob_sed_int     mobilisation factor for sediment to inter flow [-]
        _____ c_cst_mob_no3_sgw     mobilisation factor for nitrate to shallow groundwater flow [-]
        _____ c_cst_mob_nh4_sgw     mobilisation factor for ammonia to shallow groundwater flow [-]
        _____ c_cst_mob_dph_sgw     mobilisation factor for dissolved phosphorus to shallow groundwater flow [-]
        _____ c_cst_mob_pph_sgw     mobilisation factor for particulate phosphorus to shallow groundwater flow [-]
        _____ c_cst_mob_sed_sgw     mobilisation factor for sediment to shallow groundwater flow [-]
        _____ c_cst_mob_no3_dgw     mobilisation factor for nitrate to deep groundwater flow [-]
        _____ c_cst_mob_nh4_dgw     mobilisation factor for ammonia to deep groundwater flow [-]
        _____ c_cst_mob_dph_dgw     mobilisation factor for dissolved phosphorus to deep groundwater flow [-]
        _____ c_cst_mob_pph_dgw     mobilisation factor for particulate phosphorus to deep groundwater flow [-]
        _____ c_cst_mob_sed_dgw     mobilisation factor for sediment to deep groundwater flow [-]
        _____ c_cst_sed_daily_thr   daily flow threshold for sediment mobilisation [mm/day]
        _____ c_cst_sed_k           factor combining the effects of erodibility, topogr., cover and support practice [?]
        _____ c_cst_sed_p           required power of flow for sediment MUSLE equation [-]
        _____ c_cst_soil_test_p     soil test P [kg/kg]
        _____ c_cst_soil_c1n        rate coefficient for denitrification [m/day]
        _____ c_cst_soil_c3n        rate coefficient for NO3 plant uptake [m/day]
        _____ c_cst_soil_c4n        rate coefficient for nitrification [m/day]
        _____ c_cst_soil_c5n        rate coefficient for N mineralisation [m/day]
        _____ c_cst_soil_c6n        rate coefficient for N immobilisation [m/day]
        _____ c_cst_soil_c7n        rate coefficient for NH4 plant uptake [m/day]
        _____ c_cst_soil_c1p        rate coefficient for organic P plant uptake [m/day]
        _____ c_cst_soil_c2p        rate coefficient for P immobilisation [m/day]
        _____ c_cst_soil_c3p        rate coefficient for P mineralisation [m/day]
        _____ c_cst_soil_c4p        conversion rate of readily available organic P into firmly bound organic P [-]
        _____ c_cst_soil_c5p        conversion rate of firmly bound organic P into readily available organic P [-]
        _____ c_cst_soil_c6p        rate coefficient for inorganic P plant uptake [m/day]
        _____ c_cst_soil_c7p        conversion rate of readily available inorganic P into firmly bound inorganic P [-]
        _____ c_cst_soil_c8p        conversion rate of firmly bound inorganic P into readily available inorganic P [-]
        _____ c_cst_day_grow        index of the starting day for the growing season in the year [-]
        _____ c_cst_flow_tolerance              minimum flow to consider equal to no flow [m3/s]
        _____ c_cst_vol_tolerance               minimum volume to consider equal to empty [m3]
        _____ c_cst_flow_thr_mm_for_ero_ove     minimum overland flow required to trigger erosion [mm]
        _____ c_cst_flow_thr_mm_for_ero_dra     minimum drain flow required to trigger erosion [mm]
        ___ Outputs * out_ *
        _____ c_out_c_no3_ove       nitrate concentration in overland flow [kg/m3]
        _____ c_out_c_nh4_ove       ammonia concentration in overland flow [kg/m3]
        _____ c_out_c_dph_ove       dissolved phosphorus in overland flow [kg/m3]
        _____ c_out_c_pph_ove       particulate phosphorus in overland flow [kg/m3]
        _____ c_out_c_sed_ove       sediment concentration in overland flow [kg/m3]
        _____ c_out_c_no3_dra       nitrate concentration in drain flow [kg/m3]
        _____ c_out_c_nh4_dra       ammonia concentration in drain flow [kg/m3]
        _____ c_out_c_dph_dra       dissolved phosphorus in drain flow [kg/m3]
        _____ c_out_c_pph_dra       particulate phosphorus in drain flow [kg/m3]
        _____ c_out_c_sed_dra       sediment concentration in drain flow [kg/m3]
        _____ c_out_c_no3_int       nitrate concentration in inter flow [kg/m3]
        _____ c_out_c_nh4_int       ammonia concentration in inter flow [kg/m3]
        _____ c_out_c_dph_int       dissolved phosphorus in inter flow [kg/m3]
        _____ c_out_c_pph_int       particulate phosphorus in inter flow [kg/m3]
        _____ c_out_c_sed_int       sediment concentration in inter flow [kg/m3]
        _____ c_out_c_no3_sgw       nitrate concentration in shallow groundwater flow [kg/m3]
        _____ c_out_c_nh4_sgw       ammonia concentration in shallow groundwater flow [kg/m3]
        _____ c_out_c_dph_sgw       dissolved phosphorus in shallow groundwater flow [kg/m3]
        _____ c_out_c_pph_sgw       particulate phosphorus in shallow groundwater flow [kg/m3]
        _____ c_out_c_sed_sgw       sediment concentration in shallow groundwater flow [kg/m3]
        _____ c_out_c_no3_dgw       nitrate concentration in deep groundwater flow [kg/m3]
        _____ c_out_c_nh4_dgw       ammonia concentration in deep groundwater flow [kg/m3]
        _____ c_out_c_dph_dgw       dissolved phosphorus in deep groundwater flow [kg/m3]
        _____ c_out_c_pph_dgw       particulate phosphorus in deep groundwater flow [kg/m3]
        _____ c_out_c_sed_dgw       sediment concentration in deep groundwater flow [kg/m3]
        _____ c_out_c_no3           nitrate concentration in total outflow [kg/m3]
        _____ c_out_c_nh4           ammonia concentration in total outflow [kg/m3]
        _____ c_out_c_dph           dissolved phosphorus in total outflow [kg/m3]
        _____ c_out_c_pph           particulate phosphorus in total outflow [kg/m3]
        _____ c_out_c_sed           sediment concentration in total outflow [kg/m3]
        """

        # # 2. Water Quality
        # # 2.0. Convert units and store internal constants
        time_factor = time_gap_sec / 86400.0
        if time_factor < 0.005:
            time_factor = 0.005

        sediment_threshold = c_cst_sed_daily_thr * time_factor

        day_of_year = float(datetime_time_step.timetuple().tm_yday)
        if isleap(datetime_time_step.timetuple().tm_year):
            days_in_year = 366.0
        else:
            days_in_year = 365.0

        flow_threshold_for_erosion = {
            'ove': c_cst_flow_thr_mm_for_ero_ove,  # [mm]
            'dra': c_cst_flow_thr_mm_for_ero_dra  # [mm]
        }

        # # 2.1. Store hydrology states, processes, and outputs in internal dictionaries
        dict_states_old_hd = {
            'ove': c_s_v_h2o_ove_old,
            'dra': c_s_v_h2o_dra_old,
            'int': c_s_v_h2o_int_old,
            'sgw': c_s_v_h2o_sgw_old,
            'dgw': c_s_v_h2o_dgw_old
        }  # volumes in stores at the beginning of time step [m3]

        dict_states_hd = {
            'ove': c_s_v_h2o_ove,
            'dra': c_s_v_h2o_dra,
            'int': c_s_v_h2o_int,
            'sgw': c_s_v_h2o_sgw,
            'dgw': c_s_v_h2o_dgw
        }  # volumes in stores at the end of time step [m3]

        dict_outputs_hd = {
            'ove': c_out_q_h2o_ove,
            'dra': c_out_q_h2o_dra,
            'int': c_out_q_h2o_int,
            'sgw': c_out_q_h2o_sgw,
            'dgw': c_out_q_h2o_dgw
        }  # flows leaving the different stores during time step [m3/s]
        c_out_q_h2o = c_out_q_h2o_ove + c_out_q_h2o_dra + c_out_q_h2o_int + c_out_q_h2o_sgw + c_out_q_h2o_dgw

        dict_flows_mm_hd = {
            'ove': c_pr_eff_rain_to_ove,
            'dra': c_pr_eff_rain_to_dra,
            'int': c_pr_eff_rain_to_int,
            'sgw': c_pr_eff_rain_to_sgw,
            'dgw': c_pr_eff_rain_to_dgw
        }  # effective rainfall contributing to the different stores during time step [mm]

        # # 2.2. Store water quality inputs, states, parameters, and constants in internal dictionaries
        stores = ['ove', 'dra', 'int', 'sgw', 'dgw']
        stores_contaminants = ['no3', 'nh4', 'dph', 'pph', 'sed']

        dict_mass_applied = dict()
        dict_states_wq = dict()  # for states of the stores + soil
        dict_att_factors = dict()  # for attenuation factors in stores
        dict_mob_factors = dict()  # for mobilisation factors in stores
        dict_c_outflow = dict()  # for outflow concentrations from stores

        for store in stores + ['soil']:
            dict_states_wq[store] = dict()
            dict_att_factors[store] = dict()

        for store in stores:
            dict_mob_factors[store] = dict()
            dict_c_outflow[store] = dict()
            for contaminant in stores_contaminants:
                dict_c_outflow[store][contaminant] = 0.0  # initialisation only

        dict_mass_applied['no3'] = c_in_m_no3
        dict_mass_applied['nh4'] = c_in_m_nh4
        dict_mass_applied['p_ino'] = c_in_m_p_ino
        dict_mass_applied['p_org'] = c_in_m_p_org

        dict_states_wq['ove']['no3'] = c_s_c_no3_ove
        dict_states_wq['ove']['nh4'] = c_s_c_nh4_ove
        dict_states_wq['ove']['dph'] = c_s_c_dph_ove
        dict_states_wq['ove']['pph'] = c_s_c_pph_ove
        dict_states_wq['ove']['sed'] = c_s_c_sed_ove
        dict_states_wq['dra']['no3'] = c_s_c_no3_dra
        dict_states_wq['dra']['nh4'] = c_s_c_nh4_dra
        dict_states_wq['dra']['dph'] = c_s_c_dph_dra
        dict_states_wq['dra']['pph'] = c_s_c_pph_dra
        dict_states_wq['dra']['sed'] = c_s_c_sed_dra
        dict_states_wq['int']['no3'] = c_s_c_no3_int
        dict_states_wq['int']['nh4'] = c_s_c_nh4_int
        dict_states_wq['int']['dph'] = c_s_c_dph_int
        dict_states_wq['int']['pph'] = c_s_c_pph_int
        dict_states_wq['int']['sed'] = c_s_c_sed_int
        dict_states_wq['sgw']['no3'] = c_s_c_no3_sgw
        dict_states_wq['sgw']['nh4'] = c_s_c_nh4_sgw
        dict_states_wq['sgw']['dph'] = c_s_c_dph_sgw
        dict_states_wq['sgw']['pph'] = c_s_c_pph_sgw
        dict_states_wq['sgw']['sed'] = c_s_c_sed_sgw
        dict_states_wq['dgw']['no3'] = c_s_c_no3_dgw
        dict_states_wq['dgw']['nh4'] = c_s_c_nh4_dgw
        dict_states_wq['dgw']['dph'] = c_s_c_dph_dgw
        dict_states_wq['dgw']['pph'] = c_s_c_pph_dgw
        dict_states_wq['dgw']['sed'] = c_s_c_sed_dgw
        dict_states_wq['soil']['no3'] = c_s_c_no3_soil
        dict_states_wq['soil']['nh4'] = c_s_c_nh4_soil
        dict_states_wq['soil']['p_org_ra'] = c_s_c_p_org_ra_soil
        dict_states_wq['soil']['p_ino_ra'] = c_s_c_p_ino_ra_soil
        dict_states_wq['soil']['p_org_fb'] = c_s_m_p_org_fb_soil
        dict_states_wq['soil']['p_ino_fb'] = c_s_m_p_ino_fb_soil
        dict_states_wq['soil']['sed'] = c_s_m_sed_soil
        dict_states_wq['soil']['dph'] = dict_states_wq['soil']['p_org_ra'] + dict_states_wq['soil']['p_ino_ra']
        dict_states_wq['soil']['pph'] = dict_states_wq['soil']['p_org_fb'] + dict_states_wq['soil']['p_ino_fb']

        dict_att_factors['ove']['no3'] = c_p_att_no3_ove ** time_factor
        dict_att_factors['ove']['nh4'] = c_p_att_nh4_ove ** time_factor
        dict_att_factors['ove']['dph'] = c_p_att_dph_ove ** time_factor
        dict_att_factors['ove']['pph'] = c_p_att_pph_ove ** time_factor
        dict_att_factors['ove']['sed'] = c_p_att_sed_ove ** time_factor
        dict_att_factors['dra']['no3'] = c_p_att_no3_dra ** time_factor
        dict_att_factors['dra']['nh4'] = c_p_att_nh4_dra ** time_factor
        dict_att_factors['dra']['dph'] = c_p_att_dph_dra ** time_factor
        dict_att_factors['dra']['pph'] = c_p_att_pph_dra ** time_factor
        dict_att_factors['dra']['sed'] = c_p_att_sed_dra ** time_factor
        dict_att_factors['int']['no3'] = c_p_att_no3_int ** time_factor
        dict_att_factors['int']['nh4'] = c_p_att_nh4_int ** time_factor
        dict_att_factors['int']['dph'] = c_p_att_dph_int ** time_factor
        dict_att_factors['int']['pph'] = c_p_att_pph_int ** time_factor
        dict_att_factors['int']['sed'] = c_p_att_sed_int ** time_factor
        dict_att_factors['sgw']['no3'] = c_p_att_no3_sgw ** time_factor
        dict_att_factors['sgw']['nh4'] = c_p_att_nh4_sgw ** time_factor
        dict_att_factors['sgw']['dph'] = c_p_att_dph_sgw ** time_factor
        dict_att_factors['sgw']['pph'] = c_p_att_pph_sgw ** time_factor
        dict_att_factors['sgw']['sed'] = c_p_att_sed_sgw ** time_factor
        dict_att_factors['dgw']['no3'] = c_p_att_no3_dgw ** time_factor
        dict_att_factors['dgw']['nh4'] = c_p_att_nh4_dgw ** time_factor
        dict_att_factors['dgw']['dph'] = c_p_att_dph_dgw ** time_factor
        dict_att_factors['dgw']['pph'] = c_p_att_pph_dgw ** time_factor
        dict_att_factors['dgw']['sed'] = c_p_att_sed_dgw ** time_factor
        dict_att_factors['soil']['no3'] = c_p_att_no3_soil ** time_factor
        dict_att_factors['soil']['nh4'] = c_p_att_nh4_soil ** time_factor
        dict_att_factors['soil']['p_org_ra'] = c_p_att_p_org_ra_soil ** time_factor
        dict_att_factors['soil']['p_ino_ra'] = c_p_att_p_ino_ra_soil ** time_factor
        dict_att_factors['soil']['p_org_fb'] = c_p_att_p_org_fb_soil ** time_factor
        dict_att_factors['soil']['p_ino_fb'] = c_p_att_p_ino_fb_soil ** time_factor
        dict_att_factors['soil']['sed'] = c_p_att_sed_soil ** time_factor

        dict_mob_factors['ove']['no3'] = c_cst_mob_no3_ove
        dict_mob_factors['ove']['nh4'] = c_cst_mob_nh4_ove
        dict_mob_factors['ove']['dph'] = c_cst_mob_dph_ove
        dict_mob_factors['ove']['pph'] = c_cst_mob_pph_ove
        dict_mob_factors['ove']['sed'] = c_cst_mob_sed_ove
        dict_mob_factors['dra']['no3'] = c_cst_mob_no3_dra
        dict_mob_factors['dra']['nh4'] = c_cst_mob_nh4_dra
        dict_mob_factors['dra']['dph'] = c_cst_mob_dph_dra
        dict_mob_factors['dra']['pph'] = c_cst_mob_pph_dra
        dict_mob_factors['dra']['sed'] = c_cst_mob_sed_dra
        dict_mob_factors['int']['no3'] = c_cst_mob_no3_int
        dict_mob_factors['int']['nh4'] = c_cst_mob_nh4_int
        dict_mob_factors['int']['dph'] = c_cst_mob_dph_int
        dict_mob_factors['int']['pph'] = c_cst_mob_pph_int
        dict_mob_factors['int']['sed'] = c_cst_mob_sed_int
        dict_mob_factors['sgw']['no3'] = c_cst_mob_no3_sgw
        dict_mob_factors['sgw']['nh4'] = c_cst_mob_nh4_sgw
        dict_mob_factors['sgw']['dph'] = c_cst_mob_dph_sgw
        dict_mob_factors['sgw']['pph'] = c_cst_mob_pph_sgw
        dict_mob_factors['sgw']['sed'] = c_cst_mob_sed_sgw
        dict_mob_factors['dgw']['no3'] = c_cst_mob_no3_dgw
        dict_mob_factors['dgw']['nh4'] = c_cst_mob_nh4_dgw
        dict_mob_factors['dgw']['dph'] = c_cst_mob_dph_dgw
        dict_mob_factors['dgw']['pph'] = c_cst_mob_pph_dgw
        dict_mob_factors['dgw']['sed'] = c_cst_mob_sed_dgw

        # # 2.3. Water quality calculations
        # # 2.3.1. Overland flow contamination & drain flow contamination
        dict_m_mobilised = {'no3': 0.0, 'nh4': 0.0, 'dph': 0.0, 'pph': 0.0, 'sed': 0.0}
        for store in ['ove', 'dra']:
            # dissolved contaminants: nitrate, ammonia, dissolved (= readily available) phosphorus
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
                m_mobilised = \
                    (dict_flows_mm_hd[store] / 1e3 * area_m2) * dict_states_wq['soil'][contaminant] * mobilisation
                m_store = m_store_att + m_mobilised - dict_outputs_hd[store] * time_gap_sec * c_store
                if (m_store < 0.0) or (dict_states_hd[store] < c_cst_vol_tolerance):
                    logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                          ' - ', contaminant.upper(), ' Quantity in ', store.upper(),
                                          ' Store has gone negative, quantity reset to zero']))
                    dict_states_wq[store][contaminant] = 0.0
                else:
                    dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]
                dict_m_mobilised[contaminant] += m_mobilised

            # sediment
            contaminant = 'sed'
            c_store = dict_states_wq[store][contaminant]
            m_store = c_store * dict_states_old_hd[store]
            attenuation = dict_att_factors[store][contaminant]
            if attenuation > 1.0:
                attenuation = 1.0
            elif attenuation < 0.0:
                attenuation = 0.0
            m_store_att = m_store * attenuation
            if (dict_flows_mm_hd[store] < sediment_threshold) or \
                    (dict_flows_mm_hd[store] < flow_threshold_for_erosion[store]):
                m_sediment_per_area = 0.0
                m_sediment = 0.0
                dict_c_outflow[store][contaminant] = 0.0
            else:
                m_sediment_per_area = (c_cst_sed_k * dict_flows_mm_hd[store] ** c_cst_sed_p) * time_factor
                m_sediment = m_sediment_per_area * area_m2
                dict_c_outflow[store][contaminant] = m_sediment / (dict_flows_mm_hd[store] / 1e3 * area_m2)
            if store == 'ove':  # no mass balance, all sediment assumed gone
                dict_states_wq[store][contaminant] = 0.0
            elif store == 'dra':  # mass balance
                m_store = \
                    m_store_att + m_sediment - \
                    dict_outputs_hd[store] * time_gap_sec * dict_c_outflow[store][contaminant]
                if (m_store < 0.0) or (dict_states_hd[store] < c_cst_vol_tolerance):
                    logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                          ' - ', contaminant.upper(), ' Quantity in ', store.upper(),
                                          ' Store has gone negative, quantity reset to zero']))
                    dict_states_wq[store][contaminant] = 0.0
                else:
                    dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]
            dict_m_mobilised[contaminant] += m_sediment
            dict_states_wq[store][contaminant] = 0.0

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
            if (dict_flows_mm_hd[store] < sediment_threshold) or \
                    (dict_flows_mm_hd[store] < flow_threshold_for_erosion[store]):
                m_particulate_p = 0.0
                dict_c_outflow[store][contaminant] = 0.0
            else:
                soil_loss = m_sediment_per_area * 1e4 * 3.1536e7 / time_gap_sec  # [kg/ha/yr]
                p_enrichment_ratio = exp(2.48 - 0.27 * log(soil_loss))  # [-]  # soil loss cannot be equal to 0
                if p_enrichment_ratio < 0.1:
                    p_enrichment_ratio = 0.1
                elif p_enrichment_ratio > 6.0:
                    p_enrichment_ratio = 6.0
                m_particulate_p = c_cst_soil_test_p * m_sediment * p_enrichment_ratio  # [kg]
                # try to find the PPH 'demand' from the soil firmly bound P
                if m_particulate_p <= dict_states_wq['soil']['p_ino_fb']:  # P removed from inorganic P firmly in soil
                    dict_states_wq['soil']['p_ino_fb'] -= m_particulate_p
                    m_particulate_p_missing = 0.0  # [kg]
                else:  # P is also removed from organic firmly bound after inorganic firmly bound
                    m_particulate_p_missing = m_particulate_p - dict_states_wq['soil']['p_ino_fb']
                    dict_states_wq['soil']['p_ino_fb'] = 0.0
                    if m_particulate_p_missing <= dict_states_wq['soil']['p_org_fb']:
                        dict_states_wq['soil']['p_org_fb'] -= m_particulate_p_missing
                        m_particulate_p_missing = 0.0  # [kg]
                    else:
                        m_particulate_p_missing -= dict_states_wq['soil']['p_org_fb']
                        dict_states_wq['soil']['p_org_fb'] = 0.0
                dict_states_wq['soil'][contaminant] = dict_states_wq['soil']['p_org_fb'] + \
                    dict_states_wq['soil']['p_ino_fb']
                m_particulate_p -= m_particulate_p_missing  # remove part of demand that could not be satisfied by soil
                dict_c_outflow[store][contaminant] = m_particulate_p / (dict_flows_mm_hd[store] / 1e3 * area_m2)
            m_store = \
                m_store_att + m_particulate_p - \
                dict_outputs_hd[store] * time_gap_sec * dict_c_outflow[store][contaminant]
            if (m_store < 0.0) or (dict_states_hd[store] < c_cst_vol_tolerance):
                logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                      ' - ', contaminant.upper(), ' Quantity in ', store.upper(),
                                      ' Store has gone negative, quantity reset to zero']))
                dict_states_wq[store][contaminant] = 0.0
            else:
                dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]
            dict_m_mobilised[contaminant] += m_particulate_p

        # # 2.3.2. Interflow contamination, Shallow groundwater flow contamination, & Deep groundwat. flow contamination
        for store in ['int', 'sgw', 'dgw']:
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
                m_mobilised = \
                    (dict_flows_mm_hd[store] / 1e3 * area_m2) * dict_states_wq['soil'][contaminant] * mobilisation
                m_store = m_store_att + m_mobilised - dict_outputs_hd[store] * time_gap_sec * c_store
                if (m_store < 0.0) or (dict_states_hd[store] < c_cst_vol_tolerance):
                    logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                          ' - ', contaminant.upper(), ' Quantity in ', store.upper(),
                                          ' Store has gone negative, quantity reset to zero']))
                    dict_states_wq[store][contaminant] = 0.0
                else:
                    dict_states_wq[store][contaminant] = m_store / dict_states_hd[store]
                dict_m_mobilised[contaminant] += m_mobilised

        # # 2.3.3. Soil store contamination
        # nitrate
        s1 = lvl_total_end / (c_p_z * 0.275)  # soil moisture factor
        # assuming field capacity = 110 mm/m depth & soil porosity = 0.4 => 0.11 * 0.4 = 0.275
        # (SMD max assumed by Met Eireann)
        if s1 > 1.0:
            s1 = 1.0
        elif s1 < 0.0:
            s1 = 0.0
        s2 = 0.66 + 0.34 * sin(2.0 * pi * (day_of_year - c_cst_day_grow) / days_in_year)  # seasonal plant growth
        c3_no3 = c_cst_soil_c3n * (1.047 ** (c_in_temp - 20.0))
        pu_no3 = c3_no3 * s1 * s2  # plant uptake [-/day]
        c1 = c_cst_soil_c1n * (1.047 ** (c_in_temp - 20.0))
        c4 = c_cst_soil_c4n * (1.047 ** (c_in_temp - 20.0))
        if c_in_temp < 0.0:
            dn = 0.0  # no denitrification
            ni = 0.0  # no nitrification
            fx = 0.0  # no fixation
        else:
            dn = c1 * s1  # denitrification [-/day]
            ni = c4 * s1 * dict_states_wq['soil']['nh4'] * (lvl_total_start / 1e3 * area_m2)  # nitrification [kg]
            fx = 0.0  # fixation
        processes_attenuation = 1.0 - pu_no3 - dn + fx  # attenuation due to processes in soil system
        external_attenuation = dict_att_factors['soil']['no3']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_soil = dict_states_wq['soil']['no3'] * (lvl_total_start / 1e3 * area_m2)  # mass in soil at beg. of time step
        m_soil_new = m_soil * attenuation + ni * time_factor + dict_mass_applied['no3'] - dict_m_mobilised['no3']
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - NO3 Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['no3'] = 0.0
        else:
            dict_states_wq['soil']['no3'] = m_soil_new / (lvl_total_end / 1e3 * area_m2)

        # ammonia
        c3_nh4 = c_cst_soil_c7n * (1.047 ** (c_in_temp - 20.0))
        pu_nh4 = c3_nh4 * s1 * s2  # plant uptake [-/day]
        if c_in_temp < 0.0:
            im = 0.0  # no immobilisation
            mi = 0.0  # no mineralisation
        else:
            im = c_cst_soil_c6n * (1.047 ** (c_in_temp - 20.0)) * s1  # immobilisation [-/day]
            mi = c_cst_soil_c5n * (1.047 ** (c_in_temp - 20.0)) * s1 * area_m2 / 1e4  # mineralisation [kg]
        processes_attenuation = 1.0 - pu_nh4 - im
        external_attenuation = dict_att_factors['soil']['nh4']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_soil = dict_states_wq['soil']['nh4'] * (lvl_total_start / 1e3 * area_m2)
        m_soil_new = m_soil * attenuation + dict_mass_applied['nh4'] - (mi + ni) * time_factor - dict_m_mobilised['nh4']
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - NH4 Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['nh4'] = 0.0
        else:
            dict_states_wq['soil']['nh4'] = m_soil_new / (lvl_total_end / 1e3 * area_m2)

        # readily available inorganic phosphorus
        c3_p_ino_ra = c_cst_soil_c6p * (1.047 ** (c_in_temp - 20.0))
        pu_p_ino_ra = c3_p_ino_ra * s1 * s2  # plant uptake [-/day]
        pmi = c_cst_soil_c3p * (1.047 ** (c_in_temp - 20.0)) * s1 * dict_states_wq['soil']['p_org_ra'] * \
            (lvl_total_start / 1e3 * area_m2)  # mineralisation [kg]
        pim = c_cst_soil_c2p * (1.047 ** (c_in_temp - 20.0)) * s1 * dict_states_wq['soil']['p_ino_ra'] * \
            (lvl_total_start / 1e3 * area_m2)  # immobilisation [kg]
        processes_attenuation = 1.0 - pu_p_ino_ra
        external_attenuation = dict_att_factors['soil']['p_ino_ra']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        conversion_p_ino_fb_into_ra = \
            (c_cst_soil_c8p * dict_states_wq['soil']['p_ino_fb'])  # state for FB was already in kg
        conversion_p_ino_ra_into_fb = \
            (c_cst_soil_c7p * dict_states_wq['soil']['p_ino_ra'] * (lvl_total_start / 1e3 * area_m2))
        # state for RA was in kg/m3, needed conversion in kg
        m_soil = dict_states_wq['soil']['p_ino_ra'] * (lvl_total_start / 1e3 * area_m2)
        m_soil_new = m_soil * attenuation + dict_mass_applied['p_ino'] - 0.5 * dict_m_mobilised['dph'] + \
            (pmi - pim + conversion_p_ino_fb_into_ra - conversion_p_ino_ra_into_fb) * time_factor
        # assumed that all p_ino applied is in the readily available form
        # assumed that half of the dph mobilised from soil is inorganic
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - P_INO_RA Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['p_ino_ra'] = 0.0
        else:
            dict_states_wq['soil']['p_ino_ra'] = m_soil_new / (lvl_total_end / 1e3 * area_m2)

        # firmly bound inorganic phosphorus
        processes_attenuation = 1.0  # no processes consume firmly bound P
        external_attenuation = dict_att_factors['soil']['p_ino_fb']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_soil = dict_states_wq['soil']['p_ino_fb']  # state for FB is already in kg
        m_soil_new = m_soil * attenuation - 0.5 * dict_m_mobilised['pph'] + \
            (conversion_p_ino_ra_into_fb - conversion_p_ino_fb_into_ra) * time_factor
        # assumed that half of the pph mobilised from soil is inorganic
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - P_INO_FB Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['p_ino_fb'] = 0.0
        else:
            dict_states_wq['soil']['p_ino_fb'] = m_soil_new  # store state in kg

        # readily available organic phosphorus
        c3_p_org_ra = c_cst_soil_c1p * (1.047 ** (c_in_temp - 20.0))
        pu_p_org_ra = c3_p_org_ra * s1 * s2  # plant uptake
        processes_attenuation = 1.0 - pu_p_org_ra
        external_attenuation = dict_att_factors['soil']['p_org_ra']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        conversion_p_org_fb_into_ra = \
            (c_cst_soil_c5p * dict_states_wq['soil']['p_org_fb'])  # state for FB was already in kg
        conversion_p_org_ra_into_fb = \
            (c_cst_soil_c4p * dict_states_wq['soil']['p_org_ra'] * (lvl_total_start / 1e3 * area_m2))
        # state for RA was in kg/m3, needed conversion in kg
        m_soil = dict_states_wq['soil']['p_org_ra'] * (lvl_total_start / 1e3 * area_m2)
        m_soil_new = m_soil * attenuation + dict_mass_applied['p_org'] - 0.5 * dict_m_mobilised['dph'] + \
            (pim - pmi + conversion_p_org_fb_into_ra - conversion_p_org_ra_into_fb) * time_factor
        # assumed that all p_org applied is in the readily available form
        # assumed that half of the dph mobilised from soil is organic
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - P_ORG_RA Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['p_org_ra'] = 0.0
        else:
            dict_states_wq['soil']['p_org_ra'] = m_soil_new / (lvl_total_end / 1e3 * area_m2)

        # firmly bound organic phosphorus
        processes_attenuation = 1.0  # no processes consume firmly bound P
        external_attenuation = dict_att_factors['soil']['p_org_fb']
        attenuation = (processes_attenuation * external_attenuation) ** time_factor
        if attenuation > 1.0:
            attenuation = 1.0
        elif attenuation < 0.0:
            attenuation = 0.0
        m_soil = dict_states_wq['soil']['p_org_fb']  # state for FB is already in kg
        m_soil_new = m_soil * attenuation - 0.5 * dict_m_mobilised['pph'] + \
            (conversion_p_org_ra_into_fb - conversion_p_org_fb_into_ra) * time_factor
        # assumed that half of the pph mobilised from soil is organic
        if (m_soil_new < 0.0) or ((lvl_total_end / 1e3 * area_m2) < c_cst_vol_tolerance):
            logger.debug(''.join(['INCAL # ', waterbody, ': ', datetime_time_step.strftime('%d/%m/%Y %H:%M:%S'),
                                  ' - P_ORG_FB Quantity in SOIL Store has gone negative, quantity reset to zero.']))
            dict_states_wq['soil']['p_org_fb'] = 0.0
        else:
            dict_states_wq['soil']['p_org_fb'] = m_soil_new  # store state in kg

        # sediment: no calculation, unlimited availability assumed

        # # 2.4. Return water quality outputs and updated states
        dict_c_outflow['all'] = dict()
        for contaminant in stores_contaminants:
            m_outflow = 0.0
            for store in stores:
                if dict_outputs_hd[store] >= c_cst_flow_tolerance:
                    m_outflow += dict_c_outflow[store][contaminant] * dict_outputs_hd[store]
            if c_out_q_h2o > 0.0:
                c_outflow = m_outflow / c_out_q_h2o
            else:
                c_outflow = 0.0
            dict_c_outflow['all'][contaminant] = c_outflow

        return \
            dict_c_outflow['ove']['no3'], dict_c_outflow['ove']['nh4'], dict_c_outflow['ove']['dph'], \
            dict_c_outflow['ove']['pph'], dict_c_outflow['ove']['sed'], \
            dict_c_outflow['dra']['no3'], dict_c_outflow['dra']['nh4'], dict_c_outflow['dra']['dph'], \
            dict_c_outflow['dra']['pph'], dict_c_outflow['dra']['sed'], \
            dict_c_outflow['int']['no3'], dict_c_outflow['int']['nh4'], dict_c_outflow['int']['dph'], \
            dict_c_outflow['int']['pph'], dict_c_outflow['int']['sed'], \
            dict_c_outflow['sgw']['no3'], dict_c_outflow['sgw']['nh4'], dict_c_outflow['sgw']['dph'], \
            dict_c_outflow['sgw']['pph'], dict_c_outflow['sgw']['sed'], \
            dict_c_outflow['dgw']['no3'], dict_c_outflow['dgw']['nh4'], dict_c_outflow['dgw']['dph'], \
            dict_c_outflow['dgw']['pph'], dict_c_outflow['dgw']['sed'], \
            dict_c_outflow['all']['no3'], dict_c_outflow['all']['nh4'], dict_c_outflow['all']['dph'], \
            dict_c_outflow['all']['pph'], dict_c_outflow['all']['sed'], \
            dict_states_wq['ove']['no3'], dict_states_wq['ove']['nh4'], dict_states_wq['ove']['dph'], \
            dict_states_wq['ove']['pph'], dict_states_wq['ove']['sed'], \
            dict_states_wq['dra']['no3'], dict_states_wq['dra']['nh4'], dict_states_wq['dra']['dph'], \
            dict_states_wq['dra']['pph'], dict_states_wq['dra']['sed'], \
            dict_states_wq['int']['no3'], dict_states_wq['int']['nh4'], dict_states_wq['int']['dph'], \
            dict_states_wq['int']['pph'], dict_states_wq['int']['sed'], \
            dict_states_wq['sgw']['no3'], dict_states_wq['sgw']['nh4'], dict_states_wq['sgw']['dph'], \
            dict_states_wq['sgw']['pph'], dict_states_wq['sgw']['sed'], \
            dict_states_wq['dgw']['no3'], dict_states_wq['dgw']['nh4'], dict_states_wq['dgw']['dph'], \
            dict_states_wq['dgw']['pph'], dict_states_wq['dgw']['sed'], \
            dict_states_wq['soil']['no3'], dict_states_wq['soil']['nh4'], dict_states_wq['soil']['p_org_ra'], \
            dict_states_wq['soil']['p_ino_ra'], dict_states_wq['soil']['p_org_fb'], \
            dict_states_wq['soil']['p_ino_fb'], dict_states_wq['soil']['sed']

    @staticmethod
    def _get_in(waterbody, datetime_time_step, time_gap_min,
                dict_data_frame, dict_desc, dict_param, dict_meteo, dict_loads, dict_const):
        """
        This function is the interface between the data models of the simulator and the model.
        It provides the inputs, parameters, processes, and states to the model.
        It also saves the inputs into the data frame.
        It can only return a tuple of scalar variables.
        """
        # bring in catchment constants
        area_m2 = dict_desc['area']
        time_gap_sec = time_gap_min * 60.0

        # bring in water quality model inputs
        c_in_temp = dict_meteo[waterbody]["soit"][datetime_time_step]
        c_in_m_no3 = dict_loads[waterbody]['m_no3'][datetime_time_step]
        c_in_m_nh4 = dict_loads[waterbody]['m_nh4'][datetime_time_step]
        c_in_m_p_ino = dict_loads[waterbody]['m_p_ino'][datetime_time_step]
        c_in_m_p_org = dict_loads[waterbody]['m_p_org'][datetime_time_step]

        # store water quality model input in data frame
        dict_data_frame[waterbody][datetime_time_step]['c_in_temp'] = c_in_temp
        dict_data_frame[waterbody][datetime_time_step]['c_in_m_no3'] = c_in_m_no3
        dict_data_frame[waterbody][datetime_time_step]['c_in_m_nh4'] = c_in_m_nh4
        dict_data_frame[waterbody][datetime_time_step]['c_in_m_p_ino'] = c_in_m_p_ino
        dict_data_frame[waterbody][datetime_time_step]['c_in_m_p_org'] = c_in_m_p_org

        # bring in water quality model parameters
        c_p_att_no3_ove = dict_param['c_p_att_no3_ove']
        c_p_att_nh4_ove = dict_param['c_p_att_nh4_ove']
        c_p_att_dph_ove = dict_param['c_p_att_dph_ove']
        c_p_att_pph_ove = dict_param['c_p_att_pph_ove']
        c_p_att_sed_ove = dict_param['c_p_att_sed_ove']
        c_p_att_no3_dra = dict_param['c_p_att_no3_dra']
        c_p_att_nh4_dra = dict_param['c_p_att_nh4_dra']
        c_p_att_dph_dra = dict_param['c_p_att_dph_dra']
        c_p_att_pph_dra = dict_param['c_p_att_pph_dra']
        c_p_att_sed_dra = dict_param['c_p_att_sed_dra']
        c_p_att_no3_int = dict_param['c_p_att_no3_int']
        c_p_att_nh4_int = dict_param['c_p_att_nh4_int']
        c_p_att_dph_int = dict_param['c_p_att_dph_int']
        c_p_att_pph_int = dict_param['c_p_att_pph_int']
        c_p_att_sed_int = dict_param['c_p_att_sed_int']
        c_p_att_no3_sgw = dict_param['c_p_att_no3_sgw']
        c_p_att_nh4_sgw = dict_param['c_p_att_nh4_sgw']
        c_p_att_dph_sgw = dict_param['c_p_att_dph_sgw']
        c_p_att_pph_sgw = dict_param['c_p_att_pph_sgw']
        c_p_att_sed_sgw = dict_param['c_p_att_sed_sgw']
        c_p_att_no3_dgw = dict_param['c_p_att_no3_dgw']
        c_p_att_nh4_dgw = dict_param['c_p_att_nh4_dgw']
        c_p_att_dph_dgw = dict_param['c_p_att_dph_dgw']
        c_p_att_pph_dgw = dict_param['c_p_att_pph_dgw']
        c_p_att_sed_dgw = dict_param['c_p_att_sed_dgw']
        c_p_att_no3_soil = dict_param['c_p_att_no3_soil']
        c_p_att_nh4_soil = dict_param['c_p_att_nh4_soil']
        c_p_att_p_org_ra_soil = dict_param['c_p_att_p_org_ra_soil']
        c_p_att_p_ino_ra_soil = dict_param['c_p_att_p_ino_ra_soil']
        c_p_att_p_org_fb_soil = dict_param['c_p_att_p_org_fb_soil']
        c_p_att_p_ino_fb_soil = dict_param['c_p_att_p_ino_fb_soil']
        c_p_att_sed_soil = dict_param['c_p_att_sed_soil']

        # bring in water quality model states
        c_s_c_no3_ove = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_ove']
        c_s_c_nh4_ove = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_ove']
        c_s_c_dph_ove = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_dph_ove']
        c_s_c_pph_ove = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_pph_ove']
        c_s_c_sed_ove = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_sed_ove']
        c_s_c_no3_dra = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_dra']
        c_s_c_nh4_dra = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_dra']
        c_s_c_dph_dra = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_dph_dra']
        c_s_c_pph_dra = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_pph_dra']
        c_s_c_sed_dra = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_sed_dra']
        c_s_c_no3_int = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_int']
        c_s_c_nh4_int = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_int']
        c_s_c_dph_int = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_dph_int']
        c_s_c_pph_int = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_pph_int']
        c_s_c_sed_int = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_sed_int']
        c_s_c_no3_sgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_sgw']
        c_s_c_nh4_sgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_sgw']
        c_s_c_dph_sgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_dph_sgw']
        c_s_c_pph_sgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_pph_sgw']
        c_s_c_sed_sgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_sed_sgw']
        c_s_c_no3_dgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_dgw']
        c_s_c_nh4_dgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_dgw']
        c_s_c_dph_dgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_dph_dgw']
        c_s_c_pph_dgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_pph_dgw']
        c_s_c_sed_dgw = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_sed_dgw']
        c_s_c_no3_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_no3_soil']
        c_s_c_nh4_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_nh4_soil']
        c_s_c_p_org_ra_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_p_org_ra_soil']
        c_s_c_p_ino_ra_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_c_p_ino_ra_soil']
        c_s_m_p_org_fb_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_m_p_org_fb_soil']
        c_s_m_p_ino_fb_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_m_p_ino_fb_soil']
        c_s_m_sed_soil = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_m_sed_soil']

        # bring in water quality model constants
        c_cst_mob_no3_ove = dict_const['c_cst_mob_no3_ove']
        c_cst_mob_nh4_ove = dict_const['c_cst_mob_nh4_ove']
        c_cst_mob_dph_ove = dict_const['c_cst_mob_dph_ove']
        c_cst_mob_pph_ove = dict_const['c_cst_mob_pph_ove']
        c_cst_mob_sed_ove = dict_const['c_cst_mob_sed_ove']
        c_cst_mob_no3_dra = dict_const['c_cst_mob_no3_dra']
        c_cst_mob_nh4_dra = dict_const['c_cst_mob_nh4_dra']
        c_cst_mob_dph_dra = dict_const['c_cst_mob_dph_dra']
        c_cst_mob_pph_dra = dict_const['c_cst_mob_pph_dra']
        c_cst_mob_sed_dra = dict_const['c_cst_mob_sed_dra']
        c_cst_mob_no3_int = dict_const['c_cst_mob_no3_int']
        c_cst_mob_nh4_int = dict_const['c_cst_mob_nh4_int']
        c_cst_mob_dph_int = dict_const['c_cst_mob_dph_int']
        c_cst_mob_pph_int = dict_const['c_cst_mob_pph_int']
        c_cst_mob_sed_int = dict_const['c_cst_mob_sed_int']
        c_cst_mob_no3_sgw = dict_const['c_cst_mob_no3_sgw']
        c_cst_mob_nh4_sgw = dict_const['c_cst_mob_nh4_sgw']
        c_cst_mob_dph_sgw = dict_const['c_cst_mob_dph_sgw']
        c_cst_mob_pph_sgw = dict_const['c_cst_mob_pph_sgw']
        c_cst_mob_sed_sgw = dict_const['c_cst_mob_sed_sgw']
        c_cst_mob_no3_dgw = dict_const['c_cst_mob_no3_dgw']
        c_cst_mob_nh4_dgw = dict_const['c_cst_mob_nh4_dgw']
        c_cst_mob_dph_dgw = dict_const['c_cst_mob_dph_dgw']
        c_cst_mob_pph_dgw = dict_const['c_cst_mob_pph_dgw']
        c_cst_mob_sed_dgw = dict_const['c_cst_mob_sed_dgw']
        c_cst_sed_daily_thr = dict_const['c_cst_sed_daily_thr']
        c_cst_sed_k = dict_const['c_cst_sed_k']
        c_cst_sed_p = dict_const['c_cst_sed_p']
        c_cst_soil_test_p = dict_const['c_cst_soil_test_p']
        c_cst_soil_c1n = dict_const['c_cst_soil_c1n']
        c_cst_soil_c3n = dict_const['c_cst_soil_c3n']
        c_cst_soil_c4n = dict_const['c_cst_soil_c4n']
        c_cst_soil_c5n = dict_const['c_cst_soil_c5n']
        c_cst_soil_c6n = dict_const['c_cst_soil_c6n']
        c_cst_soil_c7n = dict_const['c_cst_soil_c7n']
        c_cst_soil_c1p = dict_const['c_cst_soil_c1p']
        c_cst_soil_c2p = dict_const['c_cst_soil_c2p']
        c_cst_soil_c3p = dict_const['c_cst_soil_c3p']
        c_cst_soil_c4p = dict_const['c_cst_soil_c4p']
        c_cst_soil_c5p = dict_const['c_cst_soil_c5p']
        c_cst_soil_c6p = dict_const['c_cst_soil_c6p']
        c_cst_soil_c7p = dict_const['c_cst_soil_c7p']
        c_cst_soil_c8p = dict_const['c_cst_soil_c8p']
        c_cst_day_grow = dict_const['c_cst_day_grow']
        c_cst_flow_tolerance = dict_const['c_cst_flow_tolerance']
        c_cst_vol_tolerance = dict_const['c_cst_vol_tolerance']
        c_cst_flow_thr_mm_for_ero_ove = dict_const['c_cst_flow_thr_mm_for_ero_ove']
        c_cst_flow_thr_mm_for_ero_dra = dict_const['c_cst_flow_thr_mm_for_ero_dra']

        # bring in hydrology parameters, states, and outputs necessary for water quality model
        c_p_z = dict_param['c_p_z']

        # # level in the whole soil column at the beginning of time step [mm]
        lvl_total_start = (
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly1'] +
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly2'] +
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly3'] +
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly4'] +
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly5'] +
                                  dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)][
                                      'c_s_v_h2o_ly6']
                          ) / area_m2 * 1e3

        # # level in the whole soil column at the end of time step [mm]
        lvl_total_end = (
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly1'] +
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly2'] +
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly3'] +
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly4'] +
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly5'] +
                                dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ly6']
                        ) / area_m2 * 1e3

        # # volumes in stores at the beginning of time step [m3]
        c_s_v_h2o_ove_old = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_v_h2o_ove']
        c_s_v_h2o_dra_old = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_v_h2o_dra']
        c_s_v_h2o_int_old = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_v_h2o_int']
        c_s_v_h2o_sgw_old = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_v_h2o_sgw']
        c_s_v_h2o_dgw_old = \
            dict_data_frame[waterbody][datetime_time_step + timedelta(minutes=-time_gap_min)]['c_s_v_h2o_dgw']

        # # volumes in stores at the end of time step [m3]
        c_s_v_h2o_ove = dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_ove']
        c_s_v_h2o_dra = dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_dra']
        c_s_v_h2o_int = dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_int']
        c_s_v_h2o_sgw = dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_sgw']
        c_s_v_h2o_dgw = dict_data_frame[waterbody][datetime_time_step]['c_s_v_h2o_dgw']

        # # flows leaving the different stores during time step [m3/s]
        c_out_q_h2o_ove = dict_data_frame[waterbody][datetime_time_step]['c_out_q_h2o_ove']
        c_out_q_h2o_dra = dict_data_frame[waterbody][datetime_time_step]['c_out_q_h2o_dra']
        c_out_q_h2o_int = dict_data_frame[waterbody][datetime_time_step]['c_out_q_h2o_int']
        c_out_q_h2o_sgw = dict_data_frame[waterbody][datetime_time_step]['c_out_q_h2o_sgw']
        c_out_q_h2o_dgw = dict_data_frame[waterbody][datetime_time_step]['c_out_q_h2o_dgw']

        # # effective rainfall contributing to the different stores during time step [mm]
        c_pr_eff_rain_to_ove = dict_data_frame[waterbody][datetime_time_step]['c_pr_eff_rain_to_ove']
        c_pr_eff_rain_to_dra = dict_data_frame[waterbody][datetime_time_step]['c_pr_eff_rain_to_dra']
        c_pr_eff_rain_to_int = dict_data_frame[waterbody][datetime_time_step]['c_pr_eff_rain_to_int']
        c_pr_eff_rain_to_sgw = dict_data_frame[waterbody][datetime_time_step]['c_pr_eff_rain_to_sgw']
        c_pr_eff_rain_to_dgw = dict_data_frame[waterbody][datetime_time_step]['c_pr_eff_rain_to_dgw']

        # return constants, model inputs, model parameter values, model states, model constants + hydrology inheritance
        return \
            area_m2, time_gap_sec, \
            c_in_temp, c_in_m_no3, c_in_m_nh4, c_in_m_p_ino, c_in_m_p_org, \
            c_p_att_no3_ove, c_p_att_nh4_ove, c_p_att_dph_ove, c_p_att_pph_ove, c_p_att_sed_ove, \
            c_p_att_no3_dra, c_p_att_nh4_dra, c_p_att_dph_dra, c_p_att_pph_dra, c_p_att_sed_dra, \
            c_p_att_no3_int, c_p_att_nh4_int, c_p_att_dph_int, c_p_att_pph_int, c_p_att_sed_int, \
            c_p_att_no3_sgw, c_p_att_nh4_sgw, c_p_att_dph_sgw, c_p_att_pph_sgw, c_p_att_sed_sgw, \
            c_p_att_no3_dgw, c_p_att_nh4_dgw, c_p_att_dph_dgw, c_p_att_pph_dgw, c_p_att_sed_dgw, \
            c_p_att_no3_soil, c_p_att_nh4_soil, c_p_att_p_org_ra_soil, c_p_att_p_ino_ra_soil, \
            c_p_att_p_org_fb_soil, c_p_att_p_ino_fb_soil, c_p_att_sed_soil, \
            c_s_c_no3_ove, c_s_c_nh4_ove, c_s_c_dph_ove, c_s_c_pph_ove, c_s_c_sed_ove, \
            c_s_c_no3_dra, c_s_c_nh4_dra, c_s_c_dph_dra, c_s_c_pph_dra, c_s_c_sed_dra, \
            c_s_c_no3_int, c_s_c_nh4_int, c_s_c_dph_int, c_s_c_pph_int, c_s_c_sed_int, \
            c_s_c_no3_sgw, c_s_c_nh4_sgw, c_s_c_dph_sgw, c_s_c_pph_sgw, c_s_c_sed_sgw, \
            c_s_c_no3_dgw, c_s_c_nh4_dgw, c_s_c_dph_dgw, c_s_c_pph_dgw, c_s_c_sed_dgw, \
            c_s_c_no3_soil, c_s_c_nh4_soil, c_s_c_p_org_ra_soil, c_s_c_p_ino_ra_soil, \
            c_s_m_p_org_fb_soil, c_s_m_p_ino_fb_soil, c_s_m_sed_soil, \
            c_cst_mob_no3_ove, c_cst_mob_nh4_ove, c_cst_mob_dph_ove, c_cst_mob_pph_ove, c_cst_mob_sed_ove, \
            c_cst_mob_no3_dra, c_cst_mob_nh4_dra, c_cst_mob_dph_dra, c_cst_mob_pph_dra, c_cst_mob_sed_dra, \
            c_cst_mob_no3_int, c_cst_mob_nh4_int, c_cst_mob_dph_int, c_cst_mob_pph_int, c_cst_mob_sed_int, \
            c_cst_mob_no3_sgw, c_cst_mob_nh4_sgw, c_cst_mob_dph_sgw, c_cst_mob_pph_sgw, c_cst_mob_sed_sgw, \
            c_cst_mob_no3_dgw, c_cst_mob_nh4_dgw, c_cst_mob_dph_dgw, c_cst_mob_pph_dgw, c_cst_mob_sed_dgw, \
            c_cst_sed_daily_thr, c_cst_sed_k, c_cst_sed_p, c_cst_soil_test_p, \
            c_cst_soil_c1n, c_cst_soil_c3n, c_cst_soil_c4n, c_cst_soil_c5n, c_cst_soil_c6n, c_cst_soil_c7n, \
            c_cst_soil_c1p, c_cst_soil_c2p, c_cst_soil_c3p, c_cst_soil_c4p, c_cst_soil_c5p, c_cst_soil_c6p, \
            c_cst_soil_c7p, c_cst_soil_c8p, c_cst_day_grow, c_cst_flow_tolerance, c_cst_vol_tolerance, \
            c_cst_flow_thr_mm_for_ero_ove, c_cst_flow_thr_mm_for_ero_dra, \
            c_p_z, c_out_q_h2o_ove, c_out_q_h2o_dra, c_out_q_h2o_int, c_out_q_h2o_sgw, c_out_q_h2o_dgw, \
            c_s_v_h2o_ove_old, c_s_v_h2o_dra_old, c_s_v_h2o_int_old, c_s_v_h2o_sgw_old, c_s_v_h2o_dgw_old, \
            c_s_v_h2o_ove, c_s_v_h2o_dra, c_s_v_h2o_int, c_s_v_h2o_sgw, c_s_v_h2o_dgw, \
            lvl_total_start, lvl_total_end, \
            c_pr_eff_rain_to_ove, c_pr_eff_rain_to_dra, c_pr_eff_rain_to_int, c_pr_eff_rain_to_sgw, c_pr_eff_rain_to_dgw

    @staticmethod
    def _get_out(waterbody, datetime_time_step, dict_data_frame,
                 c_out_c_no3_ove, c_out_c_nh4_ove, c_out_c_dph_ove, c_out_c_pph_ove, c_out_c_sed_ove,
                 c_out_c_no3_dra, c_out_c_nh4_dra, c_out_c_dph_dra, c_out_c_pph_dra, c_out_c_sed_dra,
                 c_out_c_no3_int, c_out_c_nh4_int, c_out_c_dph_int, c_out_c_pph_int, c_out_c_sed_int,
                 c_out_c_no3_sgw, c_out_c_nh4_sgw, c_out_c_dph_sgw, c_out_c_pph_sgw, c_out_c_sed_sgw,
                 c_out_c_no3_dgw, c_out_c_nh4_dgw, c_out_c_dph_dgw, c_out_c_pph_dgw, c_out_c_sed_dgw,
                 c_out_c_no3, c_out_c_nh4, c_out_c_dph, c_out_c_pph, c_out_c_sed,
                 c_s_c_no3_ove, c_s_c_nh4_ove, c_s_c_dph_ove, c_s_c_pph_ove, c_s_c_sed_ove,
                 c_s_c_no3_dra, c_s_c_nh4_dra, c_s_c_dph_dra, c_s_c_pph_dra, c_s_c_sed_dra,
                 c_s_c_no3_int, c_s_c_nh4_int, c_s_c_dph_int, c_s_c_pph_int, c_s_c_sed_int,
                 c_s_c_no3_sgw, c_s_c_nh4_sgw, c_s_c_dph_sgw, c_s_c_pph_sgw, c_s_c_sed_sgw,
                 c_s_c_no3_dgw, c_s_c_nh4_dgw, c_s_c_dph_dgw, c_s_c_pph_dgw, c_s_c_sed_dgw,
                 c_s_c_no3_soil, c_s_c_nh4_soil, c_s_c_p_org_ra_soil, c_s_c_p_ino_ra_soil,
                 c_s_m_p_org_fb_soil, c_s_m_p_ino_fb_soil, c_s_m_sed_soil):
        """
        This function is the interface between the model and the data models of the simulator.
        It stores the outputs, and updated states in the data frame.
        """
        # store water quality outputs in data frame
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3_ove'] = c_out_c_no3_ove
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4_ove'] = c_out_c_nh4_ove
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph_ove'] = c_out_c_dph_ove
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph_ove'] = c_out_c_pph_ove
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed_ove'] = c_out_c_sed_ove

        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3_dra'] = c_out_c_no3_dra
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4_dra'] = c_out_c_nh4_dra
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph_dra'] = c_out_c_dph_dra
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph_dra'] = c_out_c_pph_dra
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed_dra'] = c_out_c_sed_dra

        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3_int'] = c_out_c_no3_int
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4_int'] = c_out_c_nh4_int
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph_int'] = c_out_c_dph_int
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph_int'] = c_out_c_pph_int
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed_int'] = c_out_c_sed_int

        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3_sgw'] = c_out_c_no3_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4_sgw'] = c_out_c_nh4_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph_sgw'] = c_out_c_dph_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph_sgw'] = c_out_c_pph_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed_sgw'] = c_out_c_sed_sgw

        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3_dgw'] = c_out_c_no3_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4_dgw'] = c_out_c_nh4_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph_dgw'] = c_out_c_dph_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph_dgw'] = c_out_c_pph_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed_dgw'] = c_out_c_sed_dgw

        dict_data_frame[waterbody][datetime_time_step]['c_out_c_no3'] = c_out_c_no3
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_nh4'] = c_out_c_nh4
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_dph'] = c_out_c_dph
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_pph'] = c_out_c_pph
        dict_data_frame[waterbody][datetime_time_step]['c_out_c_sed'] = c_out_c_sed

        # store water quality states in data frame
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_ove'] = c_s_c_no3_ove
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_ove'] = c_s_c_nh4_ove
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_dph_ove'] = c_s_c_dph_ove
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_pph_ove'] = c_s_c_pph_ove
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_sed_ove'] = c_s_c_sed_ove

        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_dra'] = c_s_c_no3_dra
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_dra'] = c_s_c_nh4_dra
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_dph_dra'] = c_s_c_dph_dra
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_pph_dra'] = c_s_c_pph_dra
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_sed_dra'] = c_s_c_sed_dra

        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_int'] = c_s_c_no3_int
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_int'] = c_s_c_nh4_int
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_dph_int'] = c_s_c_dph_int
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_pph_int'] = c_s_c_pph_int
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_sed_int'] = c_s_c_sed_int

        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_sgw'] = c_s_c_no3_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_sgw'] = c_s_c_nh4_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_dph_sgw'] = c_s_c_dph_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_pph_sgw'] = c_s_c_pph_sgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_sed_sgw'] = c_s_c_sed_sgw

        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_dgw'] = c_s_c_no3_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_dgw'] = c_s_c_nh4_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_dph_dgw'] = c_s_c_dph_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_pph_dgw'] = c_s_c_pph_dgw
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_sed_dgw'] = c_s_c_sed_dgw

        dict_data_frame[waterbody][datetime_time_step]['c_s_c_no3_soil'] = c_s_c_no3_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_nh4_soil'] = c_s_c_nh4_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_p_org_ra_soil'] = c_s_c_p_org_ra_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_c_p_ino_ra_soil'] = c_s_c_p_ino_ra_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_m_p_org_fb_soil'] = c_s_m_p_org_fb_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_m_p_ino_fb_soil'] = c_s_m_p_ino_fb_soil
        dict_data_frame[waterbody][datetime_time_step]['c_s_m_sed_soil'] = c_s_m_sed_soil

    @staticmethod
    def _infer_parameters_from_descriptors(dict_desc):
        """
        This function uses the parameter values customised for Irish conditions in the EPA Pathways Project
        by Dr. Mesfin Desta and Dr. Eva Mockler, adapted from the values originally used in the INCA model for the UK
        (using values available in CMT Fortran code by Prof. Michael Bruen and Dr. Eva Mockler).
        """
        my_dict_param = dict()

        # INCA LAND MODEL
        # overland flow attenuation
        my_dict_param['c_p_att_no3_ove'] = 1.0
        my_dict_param['c_p_att_nh4_ove'] = 1.0
        my_dict_param['c_p_att_dph_ove'] = 0.1
        my_dict_param['c_p_att_pph_ove'] = 0.5
        my_dict_param['c_p_att_sed_ove'] = 0.5
        my_dict_param['c_p_att_no3_dra'] = 1.0
        my_dict_param['c_p_att_nh4_dra'] = 1.0
        my_dict_param['c_p_att_dph_dra'] = 0.8
        my_dict_param['c_p_att_pph_dra'] = 0.8
        my_dict_param['c_p_att_sed_dra'] = 0.8
        # inter flow attenuation
        factor = 1.0 * dict_desc['N_subsoil_transport'] * dict_desc['N_near_surface_delivery']
        if factor < 0.0001:
            factor = 0.0001
        elif factor > 1.0:
            factor = 1.0
        factor = factor ** 0.04
        my_dict_param['c_p_att_no3_int'] = factor
        my_dict_param['c_p_att_nh4_int'] = factor
        factor = 1.0 * dict_desc['P_subsoil_transport'] * dict_desc['P_near_surface_delivery']
        if factor < 0.0001:
            factor = 0.0001
        elif factor > 1.0:
            factor = 1.0
        factor = factor ** 0.04
        my_dict_param['c_p_att_dph_int'] = factor
        my_dict_param['c_p_att_pph_int'] = 0.0
        my_dict_param['c_p_att_sed_int'] = 0.0
        # shallow ground water attenuation
        factor = 1.0 * dict_desc['N_bedrock_transport']
        if factor < 0.01:
            factor = 0.01
        elif factor > 1.0:
            factor = 1.0
        factor = factor ** 0.02
        my_dict_param['c_p_att_no3_sgw'] = factor
        my_dict_param['c_p_att_nh4_sgw'] = factor
        my_dict_param['c_p_att_dph_sgw'] = 0.6
        my_dict_param['c_p_att_pph_sgw'] = 0.0
        my_dict_param['c_p_att_sed_sgw'] = 0.0
        # deep ground water attenuation
        my_dict_param['c_p_att_no3_dgw'] = factor
        my_dict_param['c_p_att_nh4_dgw'] = factor
        my_dict_param['c_p_att_dph_dgw'] = 0.5
        my_dict_param['c_p_att_pph_dgw'] = 0.0
        my_dict_param['c_p_att_sed_dgw'] = 0.0
        # soil attenuation
        my_dict_param['c_p_att_no3_soil'] = 0.5
        my_dict_param['c_p_att_nh4_soil'] = 0.5
        my_dict_param['c_p_att_p_org_ra_soil'] = 0.15
        my_dict_param['c_p_att_p_ino_ra_soil'] = 0.15
        my_dict_param['c_p_att_p_org_fb_soil'] = 1.0
        my_dict_param['c_p_att_p_ino_fb_soil'] = 1.0
        my_dict_param['c_p_att_sed_soil'] = 1.0

        return my_dict_param

    @staticmethod
    def _initialise_states():
        """
        This function initialises the model states before starting the simulations.
        If a warm-up run is used, this initialisation happens before the start of the warm-up run.
        If no warm-up is used, this initialisation happens before the start of the actual simulation run.
        """
        # currently states are not initialised, but a warm-up run can be used to start with states not null
        return {}
