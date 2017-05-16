from pandas import DataFrame
import sys
import csv
import datetime


def get_data_frame_for_daily_meteo_data(catchment, link, time_steps, in_folder):

    my_start = '%04d' % time_steps[1].year + '%02d' % time_steps[1].month + '%02d' % time_steps[1].day
    # use 1, not 0 because 0 was artificially created in TimeFrame object for initial conditions
    my_end = '%04d' % time_steps[-1].year + '%02d' % time_steps[-1].month + '%02d' % time_steps[-1].day

    my_meteo_data_types = ["rain", "peva", "temp"]

    my__data_frame = DataFrame(index=time_steps, columns=my_meteo_data_types).fillna(0.0)

    for meteo_type in my_meteo_data_types:
        try:
            with open("{}{}_{}_{}_{}.{}".format(in_folder, catchment,
                                                link, my_start, my_end, meteo_type)) as my_file:
                my_reader = csv.DictReader(my_file)

                for row in my_reader:
                    file_datetime = datetime.datetime(int(row['YEAR']), int(row['MONTH']), int(row['DAY']),
                                                      int(row['HOURS']), int(row['MINUTES']), int(row['SECONDS']))

                    my__data_frame.set_value(file_datetime, meteo_type, float(row[meteo_type.upper()]))

        except EnvironmentError:
            sys.exit("{}{}_{}_{}_{}.{} does not exist.".format(in_folder, catchment,
                                                               link, my_start, my_end, meteo_type))

    return my__data_frame


def get_dict_parameters_from_file(catchment, outlet, obj_network, dict__model, in_folder):

    try:
        with open("{}{}_{}.parameters".format(in_folder, catchment, outlet)) as my_file:
            my_dict_param = dict()
            my_reader = csv.DictReader(my_file)
            found = list()
            for row in my_reader:
                if row["EU_CD"] in obj_network.links:
                    my_dict = dict()
                    for model in dict__model[row["EU_CD"]]:
                        for param in model.parameter_names:
                            try:
                                my_dict[param] = row[param]
                            except KeyError:
                                sys.exit("The parameter {} is not available for {}".format(param, row["EU_CD"]))
                    my_dict_param[row["EU_CD"]] = my_dict
                    found.append(row["EU_CD"])
                else:
                    print "The waterbody {} in the parameter file is not in the network file.".format(row["EU_CD"])

            missing = [elem for elem in obj_network.links if elem not in found]
            if missing:
                sys.exit("The following waterbodies are not in the parameter file: {}.".format(missing))

        return my_dict_param

    except IOError:
        sys.exit("{}{}_{}.parameters does not exist.".format(in_folder, catchment, outlet))


def get_dict_constants_from_file(model, db_folder):

    try:
        with open("{}{}.const".format(db_folder, model.upper())) as my_file:
            my_dict_cst = dict()
            my_reader = csv.reader(my_file)
            for row in my_reader:
                my_dict_cst[row[0]] = row[1]

        return my_dict_cst

    except IOError:
        sys.exit("{}{}.const".format(db_folder, model.upper()))


def get_dict_variables_from_file(variables, catchment, outlet, obj_network, in_folder):

    try:
        with open("{}{}_{}.{}".format(in_folder, catchment, outlet, variables)) as my_file:
            my_dict_variables = dict()
            my_reader = csv.DictReader(my_file)
            fields = my_reader.fieldnames
            fields.delete("EU_CD")
            found = list()
            for row in my_reader:
                if row["EU_CD"] in obj_network.links:
                    my_dict = dict()
                    for field in fields:
                        my_dict[field] = row[field]
                    my_dict_variables[row["EU_CD"]] = my_dict
                    found.append(row["EU_CD"])
                else:
                    print "The waterbody {} in the {} file is not in the network file.".format(row["EU_CD"], variables)

            missing = [elem for elem in obj_network.links if elem not in found]
            if missing:
                sys.exit("The following waterbodies are not in the {} file: {}.".format(missing, variables))

        return my_dict_variables

    except IOError:
        sys.exit("{}{}_{}.{} does not exist.".format(in_folder, catchment, outlet, variables))
