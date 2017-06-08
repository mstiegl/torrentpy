import csv
import sys
import datetime

import simuModels as sM


class Network:
    """"""
    def __init__(self, catchment, outlet, input_folder):
        self.name = catchment.capitalize()
        self.networkFile = "{}{}_{}.network".format(input_folder, catchment, outlet)
        self.waterBodiesFile = "{}{}_{}.waterbodies".format(input_folder, catchment, outlet)
        self.nodes = Network.get_network_attributes(self)["nodes"]
        self.links = Network.get_network_attributes(self)["links"]
        self.connections = Network.get_network_attributes(self)["connections"]
        self.additions = Network.get_network_attributes(self)["additions"]
        self.categories = Network.get_water_bodies_attributes(self)

    def get_network_attributes(self):
        try:
            with open(self.networkFile) as my_file:
                my_reader = csv.DictReader(my_file)
                my_nodes = list()  # list of all nodes
                my_links = list()  # list of all links (i.e. waterbodies)
                my_connections = dict()  # key: waterbody, value: 2-element list (node down, node up)
                my_additions = dict()  # key: node, value: list of waterbodies pouring into node
                for row in my_reader:
                    my_nodes.append(row['NodeDown'])
                    my_nodes.append(row['NodeUp'])
                    my_links.append(row['WaterBody'])
                    my_connections[row['WaterBody']] = (row['NodeDown'], row['NodeUp'])
                my_nodes = list(set(my_nodes))  # get rid of the duplicates
                for node in my_nodes:
                    my_additions[node] = list()
                for link in my_connections:
                    my_additions[my_connections[link][0]].append(link)

        except IOError:
            sys.exit("No link-node network file found for {}.".format(self.name))

        return {
            "nodes": my_nodes,
            "links": my_links,
            "connections": my_connections,
            "additions": my_additions
        }

    def get_water_bodies_attributes(self):
        try:
            with open(self.waterBodiesFile) as my_file:
                my_reader = csv.DictReader(my_file)
                my_categories = dict()
                for row in my_reader:
                    my_categories[row['WaterBody']] = row['WaterBodyTypeCode'] + row['HeadwaterStatus']

        except IOError:
            sys.exit("No waterbodies file found for {}.".format(self.name))

        return my_categories


class Model:
    """"""
    def __init__(self, category, identifier, specs_folder):
        self.category = category.upper()
        self.identifier = identifier.upper()
        self.input_names = Model.get_one_list(self, specs_folder, "inputs")
        self.parameter_names = Model.get_one_list(self, specs_folder, "parameters")
        self.state_names = Model.get_one_list(self, specs_folder, "states")
        self.output_names = Model.get_one_list(self, specs_folder, "outputs")
        self.constant_names = Model.get_one_list(self, specs_folder, "constants")

    def get_one_list(self, specs_folder, specs_type):
        components = self.identifier.split('_')
        my_list = list()
        for component in components:
            try:
                with open(specs_folder + component + ".spec") as my_file:
                    my_reader = csv.reader(my_file)
                    my_string = list()
                    count = 0
                    for row in my_reader:
                        if row[0] == specs_type:
                            my_string = row[1]
                            count += 1
                    if count == 0:
                        sys.exit("There is no {} specifications line in {}{}.spec.".format(specs_type, specs_folder,
                                                                                           component))
                    elif count > 1:
                        sys.exit("There is more than one input specifications line in {}{}.".format(specs_type,
                                                                                                    specs_folder,
                                                                                                    component))
                    my_list.extend(my_string.split(";"))

            except IOError:
                sys.exit("There is no specifications file for {} in {}.".format(component, specs_folder))

        return my_list

    def run(self, obj_network, waterbody, dict_data_frame,
            dict_desc, dict_param, dict_const, dict_meteo, dict_loads,
            datetime_time_step, time_gap, logger):
        if self.category == "CATCHMENT":
            sM.catchment_model(self.identifier, waterbody, dict_data_frame,
                               dict_desc, dict_param, dict_const, dict_meteo, dict_loads,
                               datetime_time_step, time_gap,
                               logger)
        elif self.category == "RIVER":
            sM.river_model(self.identifier, obj_network, waterbody, dict_data_frame,
                           dict_desc, dict_param, dict_meteo,
                           datetime_time_step, time_gap,
                           logger)
        elif self.category == "LAKE":
            sM.lake_model(self.identifier, waterbody, dict_data_frame,
                          dict_desc, dict_param, dict_meteo,
                          datetime_time_step, time_gap,
                          logger)


class TimeFrame:
    """"""
    def __init__(self, datetime_start, datetime_end, increment_in_minutes):
        self.start = datetime_start
        self.end = datetime_end
        self.step = increment_in_minutes

    def get_list_datetime(self):
        gap = self.end - self.start
        gap_in_minutes = int(gap.total_seconds()) // 60
        my_list_datetime = list()
        for time_step in range(-self.step, gap_in_minutes + self.step, self.step):  # add one datetime before start
            my_datetime = self.start + datetime.timedelta(minutes=time_step)
            my_list_datetime.append(my_datetime)

        return my_list_datetime
