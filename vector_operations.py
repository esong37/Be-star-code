import numpy as np
import math
import models

def project_onto_plane(V, phi_v, theta_v):
    # Calculate the normal vector to the plane
    N = np.cross(phi_v, theta_v)
    
    # Calculate the projection of V onto N
    proj_onto_N = np.dot(V, N) / np.linalg.norm(N)**2 * N
    
    # Subtract the component of V that's orthogonal to the plane to get the projection onto the plane
    X = V - proj_onto_N
    
    return X

def calculate_vector_theta(L):
    # Calculate the length of L
    length_L = np.linalg.norm(L)
    
    # Calculate the angle a between L and the Z-axis
    # cos(a) = z / |L|
    z_head = np.array([0,0,1])
    theta = angle_between_vectors(z_head,L,True)
    
    cos_a = L[2] / length_L
    
    zb = length_L / math.cos(theta)
    
    Lz = L - np.array([0,0,zb])
    
    if Lz[2] > 0:
        if L[2] < 0:
            #inverse
            return -1*Lz
    else:
        if L[2] > 0:
            #inverse
            return -1*Lz
    
    return Lz

def calculate_vector_phi(v):
    # Normalize the input vector
    v_normalized = v / np.linalg.norm(v)
    
    # Project v onto the XY plane and normalize it
    v_proj_xy = np.array([v[0], v[1], 0])
    if np.linalg.norm(v_proj_xy) == 0:
        # If the projection is a zero vector, use the X-axis as v1
        v1 = np.array([1, 0, 0])
    else:
        # Otherwise, normalize the projection
        v1 = v_proj_xy / np.linalg.norm(v_proj_xy)
    
    v2 = np.cross(v_normalized, v1)
    
    # Normalize v2
    vphi = v2 / np.linalg.norm(v2)
    
    return vphi

def angle_between_vectors(v1,v2,r=False):
        dot_product = np.dot(v1, v2)
        magnitude_v1 = np.linalg.norm(v1)
        magnitude_v2 = np.linalg.norm(v2)
        cosine_angle = dot_product / (magnitude_v1 * magnitude_v2)
        angle_radians = np.arccos(cosine_angle)
        angle_degrees = np.degrees(angle_radians)
        
        if r:
            return angle_radians
        else:
            return angle_degrees
        
def normalize_array(x):
    return x / np.linalg.norm(x)


def vector_to_angles(v):
    r = np.linalg.norm(v)
    theta = np.arccos(v[2] / r) * (180 / np.pi)
    phi = np.arctan2(v[1], v[0]) * (180 / np.pi)
    phi = phi % 360
    
    return theta, phi



def compute_v_theta(AC):
    Z = np.array([0, 0, 1])
    V_theta = np.cross(AC, Z)
    return V_theta


def vector_to_angles2(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = math.acos(z / r)
    phi = math.atan2(y, x)
    theta_deg = math.degrees(theta)
    phi_deg = math.degrees(phi)
    return theta_deg, phi_deg



    