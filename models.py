import numpy as np
import vector_operations as vo


# class to repersent the data for one test, or one row in metadata table from db
class MetaData():
    def __init__(self,viewer,alpha, preferred_direction, num_stars,inclinations,positions):
        self.viewer = viewer
        self.alpha = alpha
        self.preferred_direction = preferred_direction
        self.num_stars = num_stars
        self.inclinations = inclinations
        self.positions = positions



# Class to represent a star with coordinates and angles
class Star:
    def __init__(self,viewer, coor, vector):
        self.viewer = viewer
        self.coordinate = coor
        self.vector = vector
        magnitude_temp = np.linalg.norm(self.vector)
        self.direction = self.vector/magnitude_temp
        
        self.p, self.phi_v, self.theta_v, self.proj_v = self.calculate_position_angle()
        
        self.i = self.calculate_inclination_angle()
        

    # inclination angle in degrees (0 ~ 90)
    def calculate_inclination_angle(self):
        v2 = self.direction
        
        # star coordinate -  viewer coordinate = actual star coordinate
        actual_coordinate = self.coordinate - self.viewer
        
        angle_degrees = vo.angle_between_vectors(actual_coordinate,v2,r=False)

        if angle_degrees > 90:
            return 180-angle_degrees
        else:
            return angle_degrees
        
    # position angle in degrees (0 ~ 180)
    def calculate_position_angle(self):
        actual_coordinate = self.coordinate - self.viewer
        

        phi_v = vo.calculate_vector_phi(actual_coordinate)
        theta_v = vo.calculate_vector_theta(actual_coordinate)
        proj_v = vo.project_onto_plane(self.vector, phi_v, theta_v)

        position_angle = vo.angle_between_vectors(proj_v,theta_v)

        if np.isnan(position_angle):
            return 0,phi_v, theta_v, proj_v
        else:
            return vo.angle_between_vectors(proj_v,theta_v), phi_v, theta_v, proj_v

#Data for each star obtained from the database
class StarDB:
    def __init__(self, star_id, coordinate, rotation_axis, position_angle, incliantion_angle):
        self.star_id = star_id
        self.coordinate = coordinate
        self.rotation_axis = rotation_axis
        self.position_angle = position_angle
        self.incliantion_angle = incliantion_angle