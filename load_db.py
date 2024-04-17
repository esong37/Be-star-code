import sqlite3
import numpy as np
import models

# get data from db for once (all metadata)
def get_metaData(db_path):
    print(f"start collect meta data from : {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metadata")
    meta_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM positions")
    positions_row = cursor.fetchall()
    cursor.execute("SELECT * FROM inclinations")
    inclinations_row = cursor.fetchall()

    result = {}
    for i in range(len(meta_rows)):
        metaID = meta_rows[i][0]
        viewer = np.array(meta_rows[i][1:4])
        alpha = meta_rows[i][4]
        preferred_direction = np.array(meta_rows[i][5:8])
        num_stars = meta_rows[i][8]

        metaID = inclinations_row[i][0]
        db_inclination = np.array(inclinations_row[i][1:], dtype=np.float32)
        db_position = np.array(positions_row[i][1:], dtype=np.float32)
        result[metaID] = models.MetaData(viewer,alpha, preferred_direction, num_stars,db_inclination,db_position)
    print("collecting finished")

    conn.close()
    return result




# according to specific metaId, get the metadata and stars
def fetch_meta_data_and_stars(db_path, metaID):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch metadata
    cursor.execute("SELECT viewer_x, viewer_y, viewer_z, alpha, preferred_direction_x, preferred_direction_y, preferred_direction_z, num_stars FROM metadata WHERE metaID=?", (metaID,))
    row = cursor.fetchone()
    viewer = np.array(row[:3])
    alpha = row[3]
    preferred_direction = np.array(row[4:7], dtype=np.float32)
    num_stars = row[7]

    # Fetch inclinations and positions
    cursor.execute("SELECT bin1, bin2, bin3, bin4, bin5, bin6, bin7, bin8, bin9 FROM inclinations WHERE metaID=?", (metaID,))
    inclinations = np.array(cursor.fetchone(), dtype=np.float32)
    cursor.execute("SELECT bin1, bin2, bin3, bin4, bin5, bin6, bin7, bin8, bin9 FROM positions WHERE metaID=?", (metaID,))
    positions = np.array(cursor.fetchone(), dtype=np.float32)

    # Create MetaDataDB object
    meta_data_db = models.MetaData(viewer, alpha, preferred_direction, num_stars, inclinations, positions)

    # Fetch and create StarDB objects
    stars = []
    cursor.execute("SELECT starID, coordinate_x, coordinate_y, coordinate_z, rotation_axis_x, rotation_axis_y, rotation_axis_z, inclination_angle, position_angle FROM stars WHERE metaID=?", (metaID,))
    for row in cursor.fetchall():
        star_id = row[0]
        coordinate = np.array(row[1:4])
        rotation_axis = np.array(row[4:7])
        inclination_angle = row[7]
        position_angle = row[8]
        star = models.StarDB(star_id, coordinate, rotation_axis, position_angle, inclination_angle)
        stars.append(star)

    conn.close()
    
    return meta_data_db, stars


# open database and get all inclinationos and positions, then close database
# test ok
# {1: (array([ 16.,  51.,  77., 110., 126., 143., 157., 153., 167.],
#     dtype=float32), array([108., 110., 110., 116., 108.,  95.,  98., 115., 130.],
#     dtype=float32)),..}
def get_inclinations_positions(db_path):
    print(f"start brute force search and open database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM positions")
    positions_row = cursor.fetchall()
    cursor.execute("SELECT * FROM inclinations")
    inclinations_row = cursor.fetchall()
    conn.close()

    i_p_data = {}

    for i in range(len(inclinations_row)):
        metaID = inclinations_row[i][0]
        db_inclination = np.array(inclinations_row[i][1:], dtype=np.float32)
        db_position = np.array(positions_row[i][1:], dtype=np.float32)
        i_p_data[metaID] = (db_inclination,db_position)
        #print(metaID)
    print("created finished")
    return i_p_data