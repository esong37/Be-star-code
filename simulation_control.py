import numpy as np
import models
import star_simulation as ss


# Get the quantities in different bins
def get_bins(hist_data,num_bins):
    hist, _ = np.histogram(hist_data, bins=num_bins)
    return hist

 
# Conduct a simulation with a specific number of stars, a specific alpha value, a specific pd value, and a specific number of bins
# Return metaDAta and stars
def do_cylinder_Simulation(num_stars, alpha, viewer, preferred_direction, bins ):
    stars = ss.random_samples(viewer,num_stars, preferred_direction, alpha )
    
    inclination_angles = [star.i for star in stars]
    position_angles = [star.p for star in stars]
    
    inclination_bins = get_bins(inclination_angles, np.arange(0,90+90/bins,90/bins))
    position_bins = get_bins(position_angles, np.arange(0,180+180/bins,180/bins))
    

    metaData = models.MetaData(viewer, alpha, preferred_direction, num_stars, inclination_bins, position_bins)
    
    
    return metaData, stars