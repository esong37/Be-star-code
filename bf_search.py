import numpy as np
import sqlite3
import models
from concurrent.futures import ProcessPoolExecutor
from scipy.stats import chi2_contingency
from scipy.stats import chisquare
import load_db
from scipy.stats import ks_2samp

"""
do brute force search to find the metaID of rows in database,
return a MetaDataDB objecta and a list of StarDB objects
"""

# get chi square value, observed and excepted data
def calculate_chi_square(arr1, arr2):
    nonzero = (arr1 + arr2) > 0
    return np.sum(((arr1[nonzero] - arr2[nonzero]) ** 2) / (arr2[nonzero]))

# get reduced chi square value, observed and excepted data
# degree of freedom is set to 9 by default(number of bins)
def calculate_reduced_chi_square(A, B, df = 9):
    arr1 = np.array([float(e) for e in A])
    arr2 = np.array(B)
    factor = sum(B)/sum(A)
    arr1 *= factor
    nonzero = B > 0
    red_chi = np.sum(((arr1[nonzero] - arr2[nonzero]) ** 2) / (arr2[nonzero]))/ df
    return red_chi

# do ks test
def ks_test(A,B):
    ks, p_k = ks_2samp(A, B)
    return ks


# don't need to open db, just search metaIDs from meta data list with reduced chi square <  red_chi_range
# then sort the metaIDs with the first close to 1
# [[in_redchi, po_redchi, metaData obj],...]
def brute_force_search_matched(inclination,position, meta_data_list,red_chi_range):
    final_metaIDs = []

    for metaID in meta_data_list:
        db_inclination = np.array(meta_data_list[metaID].inclinations)
        db_position = np.array(meta_data_list[metaID].positions)

        inclination_red_chi = calculate_reduced_chi_square(inclination, db_inclination)
        position_red_chi = calculate_reduced_chi_square(position, db_position)

        if inclination_red_chi < red_chi_range and position_red_chi < red_chi_range:
            final_metaIDs.append( [inclination_red_chi,position_red_chi, meta_data_list[metaID]])

    if len(final_metaIDs) > 0:
        return sorted(final_metaIDs, key=lambda x: abs(x[0] - 1) + abs(x[1] - 1))
    else:
        return []


# don't need to open db, just search metaIDs from meta data list with ks value
# then sort the metaIDs with the first close to 1
# [[in_redchi, po_redchi, metaData obj],...]
def brute_force_search_ks(inclination,position, meta_data_list):
    final_metaIDs = []

    for metaID in meta_data_list:
        db_inclination = np.array(meta_data_list[metaID].inclinations)
        db_position = np.array(meta_data_list[metaID].positions)

        inclination_ks = ks_test(inclination, db_inclination)
        position_ks = ks_test(position, db_position)

        final_metaIDs.append( [inclination_ks,position_ks, meta_data_list[metaID]])

    if len(final_metaIDs) > 0:
        return sorted(final_metaIDs, key=lambda x: x[0] + x[1])
    else:
        return []


# only test on inclination
def brute_force_search_ks_inclination(inclination,meta_data_list):
    final_metaIDs = []

    for metaID in meta_data_list:
        db_inclination = np.array(meta_data_list[metaID].inclinations)

        inclination_ks = ks_test(inclination, db_inclination)

        if inclination_ks < 0.4:
            final_metaIDs.append( [inclination_ks, meta_data_list[metaID]])
    if len(final_metaIDs) > 0:
        return sorted(final_metaIDs, key=lambda x: x[0])
    else:
        return []
    



if __name__ == "__main__":
    db_path = 'data_library_t100_a11_s1000.db'
    test_metaDatas = load_db.get_metaData(db_path)

    test_id = 123142

    test_data = test_metaDatas[test_id]

    correct_metadata, _ = load_db.fetch_meta_data_and_stars(db_path,test_id)

    print(test_data.viewer)
    print(test_data.inclinations)
    print(test_data.positions)
    print(test_data.alpha)
    print(test_data.preferred_direction)

    print(correct_metadata.viewer)
    print(correct_metadata.inclinations)
    print(correct_metadata.positions)
    print(correct_metadata.alpha)
    print(correct_metadata.preferred_direction)
