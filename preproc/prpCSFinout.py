import datetime
import csv
from netCDF4 import Dataset


def read_csv(csv_file, var_type, ind_type, col4index):
    try:
        with open(csv_file, 'rb') as my_file:
            my_nd_variables = dict()
            my_reader = csv.DictReader(my_file)
            fields = my_reader.fieldnames[:]
            try:
                fields.remove(col4index)
            except KeyError:
                raise Exception('Field {} does not exist in {}.'.format(col4index, csv_file))
            for row in my_reader:
                my_dict = dict()
                for field in fields:
                    my_dict[field] = var_type(row[field])
                my_nd_variables[ind_type(row[col4index])] = my_dict

        return my_nd_variables

    except IOError:
        raise Exception('File {} could not be found.'.format(csv_file))


def read_netcdf(netcdf_file, var_type, ind_type):
    # /!\ Unlike read_csv, read_netcdf only works for netCDF that contain a DATETIME variable
    try:
        with Dataset(netcdf_file, "r") as my_file:
            my_file.set_auto_mask(False)
            my_nd_variables = dict()
            fields = my_file.variables.keys()
            try:
                fields.remove('DATETIME')
            except KeyError:
                raise Exception('Field {} does not exist in {}.'.format('DATETIME', netcdf_file))

            for field in fields:
                if not len(my_file.variables['DATETIME']) == len(my_file.variables[field]):
                    raise Exception(
                        'Fields {} and {} do not have the same length in {}.'.format(field, 'DATETIME', netcdf_file))

            list_str_dt = [datetime.datetime.utcfromtimestamp(tstamp).strftime("%Y-%m-%d %H:%M:%S")
                           for tstamp in my_file.variables['DATETIME'][:]]
            list_vals = {field: my_file.variables[field][:] for field in fields}

            for idx, dt in enumerate(list_str_dt):
                my_dict = dict()
                for field in fields:
                    my_dict[str(field)] = var_type(list_vals[field][idx])
                my_nd_variables[ind_type(dt)] = my_dict

        return my_nd_variables

    except IOError:
        raise Exception('File {} could not be found.'.format(netcdf_file))


def get_nd_meteo_data_from_file(catchment, link, my_tf, series_data, series_simu,
                                dt_start_data, dt_end_data, in_file_format, in_folder):
    if in_file_format == 'netcdf':
        return get_nd_meteo_data_from_netcdf_file(catchment, link, my_tf, series_data, series_simu,
                                                  dt_start_data, dt_end_data, in_folder)
    else:
        return get_nd_meteo_data_from_csv_file(catchment, link, my_tf, series_data, series_simu,
                                               dt_start_data, dt_end_data, in_folder)


def get_nd_meteo_data_from_csv_file(catchment, link, my_tf, series_data, series_simu,
                                    dt_start_data, dt_end_data, in_folder):

    my_start = dt_start_data.strftime("%Y%m%d")
    my_end = dt_end_data.strftime("%Y%m%d")

    my_meteo_data_types = ["rain", "peva", "airt", "soit"]

    my_dbl_dict = {i: {c: 0.0 for c in my_meteo_data_types} for i in series_simu}

    divisor = my_tf.gap_data / my_tf.gap_simu

    for meteo_type in my_meteo_data_types:
        try:
            my_meteo_nd = read_csv("{}{}_{}_{}_{}.{}".format(in_folder, catchment, link, my_start, my_end, meteo_type),
                                   var_type=str, ind_type=str, col4index='DATETIME')

            for my_dt_data in series_data[1:]:  # ignore first value which is for the initial conditions
                try:
                    my_value = my_meteo_nd[my_dt_data.strftime("%Y-%m-%d %H:%M:%S")][meteo_type.upper()]
                    my_portion = float(my_value) / divisor
                except KeyError:  # could only be raised for .get_value(), when index or column does not exist
                    raise Exception("{}{}_{}_{}_{}.{} does not contain any value for {}.".format(
                        in_folder, catchment, link, my_start, my_end, meteo_type,
                        my_dt_data.strftime("%Y-%m-%d %H:%M:%S")))
                except ValueError:  # could only be raised for float(), when my_value is not a number
                    raise Exception("{}{}_{}_{}_{}.{} contains an invalid value for {}.".format(
                        in_folder, catchment, link, my_start, my_end, meteo_type,
                        my_dt_data.strftime("%Y-%m-%d %H:%M:%S")))
                # total = float(my_value)
                for my_sub_step in xrange(0, -divisor, -1):
                    my_dt_simu = my_dt_data + datetime.timedelta(minutes=my_sub_step * my_tf.gap_simu)
                    if (meteo_type == 'rain') or (meteo_type == 'peva'):
                        my_dbl_dict[my_dt_simu][meteo_type] = float(my_portion)
                    else:
                        my_dbl_dict[my_dt_simu][meteo_type] = float(my_value)

        except IOError:
            raise Exception("{}{}_{}_{}_{}.{} does not exist.".format(
                in_folder, catchment, link, my_start, my_end, meteo_type))

        del my_meteo_nd

    return my_dbl_dict


def get_nd_meteo_data_from_netcdf_file(catchment, link, my_tf, series_data, series_simu,
                                       dt_start_data, dt_end_data, in_folder):

    my_start = dt_start_data.strftime("%Y%m%d")
    my_end = dt_end_data.strftime("%Y%m%d")

    my_meteo_data_types = ["rain", "peva", "airt", "soit"]

    my_dbl_dict = {i: {c: 0.0 for c in my_meteo_data_types} for i in series_simu}

    divisor = my_tf.gap_data / my_tf.gap_simu

    for meteo_type in my_meteo_data_types:
        try:
            my_meteo_nd = read_netcdf("{}{}_{}_{}_{}.{}.nc".format(in_folder, catchment, link,
                                                                   my_start, my_end, meteo_type),
                                      var_type=str, ind_type=str)

            for my_dt_data in series_data[1:]:  # ignore first value which is for the initial conditions
                try:
                    my_value = my_meteo_nd[my_dt_data.strftime("%Y-%m-%d %H:%M:%S")][meteo_type.upper()]
                    my_portion = float(my_value) / divisor
                except KeyError:  # could only be raised for .get_value(), when index or column does not exist
                    raise Exception("{}{}_{}_{}_{}.{} does not contain any value for {}.".format(
                        in_folder, catchment, link, my_start, my_end, meteo_type,
                        my_dt_data.strftime("%Y-%m-%d %H:%M:%S")))
                except ValueError:  # could only be raised for float(), when my_value is not a number
                    raise Exception("{}{}_{}_{}_{}.{} contains an invalid value for {}.".format(
                        in_folder, catchment, link, my_start, my_end, meteo_type,
                        my_dt_data.strftime("%Y-%m-%d %H:%M:%S")))
                # total = float(my_value)
                for my_sub_step in xrange(0, -divisor, -1):
                    my_dt_simu = my_dt_data + datetime.timedelta(minutes=my_sub_step * my_tf.gap_simu)
                    if (meteo_type == 'rain') or (meteo_type == 'peva'):
                        my_dbl_dict[my_dt_simu][meteo_type] = float(my_portion)
                    else:
                        my_dbl_dict[my_dt_simu][meteo_type] = float(my_value)

        except IOError:
            raise Exception("{}{}_{}_{}_{}.{} does not exist.".format(
                in_folder, catchment, link, my_start, my_end, meteo_type))

        del my_meteo_nd

    return my_dbl_dict


def get_nd_from_file(obj_network, folder, var_type, extension='csv'):

    try:
        with open("{}{}_{}.{}".format(folder, obj_network.name, obj_network.code, extension)) as my_file:
            my_dict_variables = dict()
            my_reader = csv.DictReader(my_file)
            fields = my_reader.fieldnames[:]
            fields.remove("EU_CD")
            found = list()
            for row in my_reader:
                if row["EU_CD"] in obj_network.links:
                    my_dict = dict()
                    for field in fields:
                        my_dict[field] = var_type(row[field])
                    my_dict_variables[row["EU_CD"]] = my_dict
                    found.append(row["EU_CD"])
                else:
                    print "The waterbody {} in the {} file is not in the network file.".format(row["EU_CD"], extension)

            missing = [elem for elem in obj_network.links if elem not in found]
            if missing:
                raise Exception("The following waterbodies are not in the {} file: {}.".format(missing, extension))

        return my_dict_variables

    except IOError:
        raise Exception("{}{}_{}.{} does not exist.".format(folder, obj_network.name, obj_network.code, extension))


def get_nd_distributions_from_file(specs_folder):

    try:
        my_file = '{}LOADINGS.dist'.format(specs_folder)
        my_nd_distributions = read_csv(my_file, var_type=float, ind_type=int, col4index='day_no')
        return my_nd_distributions

    except IOError:
        raise Exception("{}LOADINGS.dist does not exist.".format(specs_folder))