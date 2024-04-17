import sqlite3
import numpy as np
import direction_generation as dg
import simulation_control as sc



# open database, do an auto insert according num_alpha and num_theta and num_stars
# take 8 hours to generate a 1000 star db
def insertDB(num_alpha,num_theta,num_stars, db_path):
    print(f"Start insert data to database {db_path}")

    # Reconnect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    # get vector list
    vector_list, alpha_list = dg.generate_preferred_directions(num_alpha,num_theta)


    num_bin = 9
    viewer = np.array([0,0,0])

    #for each vector, provide 11 models according to 11 alpha value


    # Insert data into metadata table
    metadata_insert_sql = '''
    INSERT INTO metadata (metaID, viewer_x, viewer_y, viewer_z, alpha, preferred_direction_x, preferred_direction_y, preferred_direction_z, num_stars)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Insert data into stars table
    stars_insert_sql = '''
    INSERT INTO stars (metaID, starID, coordinate_x, coordinate_y, coordinate_z, rotation_axis_x, rotation_axis_y, rotation_axis_z, inclination_angle, position_angle)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    inclination_insert_sql = '''
    INSERT INTO inclinations (metaID, bin1, bin2, bin3, bin4, bin5, bin6, bin7, bin8, bin9)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    position_insert_sql = '''
    INSERT INTO positions (metaID, bin1, bin2, bin3, bin4, bin5, bin6, bin7, bin8, bin9)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    metaID = 1

    vectorIndex = -1

    for vector in vector_list:
        vectorIndex += 1
        if vectorIndex%10 == 0:
            print(f"counter vector index: {vectorIndex}")
        for alpha in alpha_list:

            
            metaData, stars  = sc.do_cylinder_Simulation(num_stars, alpha, viewer, vector, bins=9 )
            metadata_data = [
                (metaID, float(metaData.viewer[0]), float(metaData.viewer[1]), float(metaData.viewer[2]), 
                alpha, 
                float(metaData.preferred_direction[0]), float(metaData.preferred_direction[1]), float(metaData.preferred_direction[2]), 
                metaData.num_stars)]
            inclination_data = [(
                (metaID, 
                 float(metaData.inclinations[0]), float(metaData.inclinations[1]), float(metaData.inclinations[2]),
                 float(metaData.inclinations[3]), float(metaData.inclinations[4]), float(metaData.inclinations[5]), 
                 float(metaData.inclinations[6]), float(metaData.inclinations[7]), float(metaData.inclinations[8]))
                )]
            
            position_data = [(
                (metaID, 
                 float(metaData.positions[0]), float(metaData.positions[1]), float(metaData.positions[2]), 
                 float(metaData.positions[3]), float(metaData.positions[4]), float(metaData.positions[5]), 
                 float(metaData.positions[6]), float(metaData.positions[7]), float(metaData.positions[8]))
                )]

            cursor.executemany(metadata_insert_sql, metadata_data)
            cursor.executemany(inclination_insert_sql, inclination_data)
            cursor.executemany(position_insert_sql, position_data)
            
            metaID += 1
            
            starID = 1
            for star in stars:
                stars_data = [
                    (metaID, starID, float(star.coordinate[0]), float(star.coordinate[1]), float(star.coordinate[2]), 
                    float(star.vector[0]), float(star.vector[1]), float(star.vector[2]),
                    star.i, star.p)]
                
                
                cursor.executemany(stars_insert_sql, stars_data)
                starID += 1
            



    query = 'SELECT * FROM metadata LIMIT 4'

    # Execute the query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

