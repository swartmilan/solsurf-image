#processes the noise corrected 'spot' reflectivity on a mirror
def spot_processor(rgb_dark, rgb_light):
    #swap betweenn 16383. and 1., depending on whether float (range 0-1) or unassigned integer (uint14) format is required respectively.
    #The values are read in as uint14 (range 0-16383) and put into a 16bit (range 0-65535) array, max value remains 16383, no rescale needed
    dark_float  = rgb_dark / 16383.
    light_float = rgb_light / 16383.
    
    #Subtract noise
    noise_corr_image = light_float - dark_float
    return noise_corr_image

#processes a mirror using a series of spots
#first noise correct then process
def mirror_processor(mp_filename, current_date):
    import glob
    import rawpy
    import numpy as np
    
    #get images
    images = glob.glob(mp_filename + '*.NEF')
    n_images = len(images)
    N = n_images/2.0 #number of spots / because there are two images per spot, one dark and one light
    if not (n_images % 2 == 0):
        print('Must be even number of images in the set - check ' + mp_filename)
        return
    
    # empty array creation
    spot_means = []

    #collecting light and dark
    for i in range(0, n_images, 2):
        #COLLECT
        with rawpy.imread(images[i]) as raw:
            rgb_dark = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)     
        with rawpy.imread(images[i+1]) as raw:
            rgb_light = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16) 
        
        
        #correct for noise by subtracting dark from light image
        corrected_image = spot_processor(rgb_dark, rgb_light)
        corrected_image_channel_means = corrected_image.mean(axis=0).mean(axis=0)
        print(str(corrected_image_channel_means)) #prints channel means
        with open("F:/Google Drive/Masters/Reflectometer image processing/Master Controller/"+str(current_date)+"_logfile_v3.txt", "a") as logfile:
            logfile.write(str(corrected_image_channel_means)+"\n")
        channels_mean = np.mean(corrected_image_channel_means) #LINEAR mean of three channel mean's
        print(channels_mean) ###################
        spot_means.append(channels_mean)
        
    #mirror statistics
    mean_PI = np.mean(spot_means)
    std_dev =  (np.std(spot_means))*100.0 #the PI is a float (also a percentage) and can therefore be expressed as such for stddev
    
    return spot_means, mean_PI, std_dev, N