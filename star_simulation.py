import numpy as np
import models 
import vector_operations as vo

# Function to generate random coordinates
def generate_random_coordinates(numStars,radius=2000,height=100):
    result = []
    
    for i in range(numStars):
        while True:
            c = np.array([0,0,0])
            c[0] = np.random.uniform(-radius, radius, 1)
            c[1] = np.random.uniform(-radius, radius, 1)
            c[2] = np.random.uniform(-height, height, 1)
            temp = [c[0],c[1]]
            if np.linalg.norm(temp) < radius:
                result.append(c)
                break
    return result


# generate a random vector,if length > 10, get a new one
def generate_random_vectors(numStars):
    result = []
    
    for i in range(numStars):
        while True:
            v = np.random.uniform(-10, 10, 3)
            if np.linalg.norm(v) < 10:
                result.append(vo.normalize_array(v))
                break
    return result


# generate random direction according to alpha dn pd
def generate_random_direction(num_points, alpha, preferred_direction):
    # alpha =1: inclination angle is uniform distribution (all star have same direction, shows the distribution of coor)
    
    vectors = generate_random_vectors(num_points)

    result = []

    for random_vector in vectors:
        
        new_vector = (1 - alpha) * random_vector + alpha * preferred_direction

        result.append(np.array(new_vector))
    return result


# get random samples according to viewer, number of stars, pd and alpha
def random_samples( viewer,num_points, preferred_direction, alpha):

    coors = generate_random_coordinates(num_points)
    vectors = generate_random_direction(num_points, alpha, preferred_direction) 


    stars = []
    for i in range(num_points):
            stars.append(models.Star(viewer,coors[i], vectors[i]))
   
    return stars