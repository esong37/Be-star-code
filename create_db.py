import os
import sqlite3

# create the sql database according to a path
def createDB(db_path):

    # Remove the existing database file if it exists
    if os.path.exists(db_path):
        print("existed database reomoved")
        os.remove(db_path)

    # Connect to the new database (this will create the database if it doesn't exist)
    conn = sqlite3.connect(db_path)

    # Create a cursor object using the cursor method
    cursor = conn.cursor()

    # Create metadata table
    metadata_table_sql = '''
    CREATE TABLE metadata (
        metaID INTEGER PRIMARY KEY,
        viewer_x REAL,column_2
        viewer_y REAL,
        viewer_z REAL,
        alpha REAL,
        preferred_direction_x REAL,
        preferred_direction_y REAL,
        preferred_direction_z REAL,
        num_stars INTEGER
    );
    '''

    # Create stars table
    stars_table_sql = '''
    CREATE TABLE stars (
        metaID INTEGER,
        starID INTEGER,
        coordinate_x REAL,
        coordinate_y REAL,
        coordinate_z REAL,
        rotation_axis_x REAL,
        rotation_axis_y REAL,
        rotation_axis_z REAL,
        inclination_angle REAL,
        position_angle REAL,
        PRIMARY KEY (metaID, starID),
        FOREIGN KEY (metaID) REFERENCES metadata(metaID)
    );
    '''
    # Create inclination angle distribution table
    inclination_sql = """
    CREATE TABLE inclinations (
        metaID INTEGER PRIMARY KEY,
        bin1 INTEGER,
        bin2 INTEGER,
        bin3 INTEGER,
        bin4 INTEGER,
        bin5 INTEGER,
        bin6 INTEGER,
        bin7 INTEGER,
        bin8 INTEGER,
        bin9 INTEGER,
        FOREIGN KEY (metaID) REFERENCES metadata(metaID)
    );
    """

    # Create position angle distribution table
    position_sql = """
    CREATE TABLE positions (
        metaID INTEGER PRIMARY KEY,
        bin1 INTEGER,
        bin2 INTEGER,
        bin3 INTEGER,
        bin4 INTEGER,
        bin5 INTEGER,
        bin6 INTEGER,
        bin7 INTEGER,
        bin8 INTEGER,
        bin9 INTEGER,
        FOREIGN KEY (metaID) REFERENCES metadata(metaID)
    );
    """


    # Execute the SQL statements to create the table
    cursor.execute(metadata_table_sql)
    cursor.execute(stars_table_sql)
    cursor.execute(inclination_sql)
    cursor.execute(position_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("database created successfully")