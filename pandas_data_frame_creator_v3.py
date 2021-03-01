def dataframe_creator(current_date, calibration_mirror_df_path):
    import time
    import pandas as pd
    import _pickle as pickle
    from ImageProcessingScripts.reflectivity_processing_lib_script_v3 import mirror_processor

    start_time = time.time()
    
    #reference values
    df_reference = pd.read_pickle(calibration_mirror_df_path)
    reference_mean_PI = df_reference.iloc[0]['Mean_PI']

    #main image folder for current date, contains all sets and mirrors
    image_folder = 'F:/Google Drive/Masters/Reflectometer image processing/DataFrame Images/' + str(current_date) +'/'    
    
    # DataFrame Initialisation
    df_init = pd.DataFrame(columns=['Date', 'Set', 'Mirror', 'Mirror Elevation', 'Reference Mean PI', 'Soiled Mean PI', 'Clean Mean PI', 'Soiled Reflectance', 'Clean Reflectance', 'Measurement Uncertainty %', 'Set Measurement Uncertainty %'])
    #store file for regular use
    df_filename = 'F:/Google Drive/Masters/Reflectometer image processing/Master Controller/DataStorageActive/df_' + str(current_date) + '.pkl'
    pd.to_pickle(df_init, df_filename)

    
    #SET 1 MIRROR LAYOUT
    ##  M1~elev.60deg,soiled.cleaned  #  M2~elev.30deg,soiled.cleaned  #  M3~elev.60deg,soiled.cleaned  #  M4~elev.60deg,soiled.cleaned  ##
    ##  M5~elev.30deg,soiled.cleaned  #  M6~elev.60deg,soiled.cleaned  #  M7~elev.60deg,soiled.cleaned  #  M8~elev.60deg,soiled.cleaned  ##
    S1 = [60,30,60,60,30,60,60,60]
    #SET 2 MIRROR LAYOUT
    ##  M1~elev.30deg,soiled.cleaned  #  M2~elev.60deg,soiled.cleaned  #  M3~elev.60deg,soiled.cleaned  #  M4~elev.60deg,soiled.cleaned  ##
    ##  M5~elev.30deg,soiled.cleaned  #  M6~elev.60deg,soiled.cleaned  #  M7~elev.60deg,soiled.cleaned  #  M8~elev.60deg,soiled.cleaned  ## 
    S2 = [30,60,60,60,30,60,60,60]
    #SET 3 MIRROR LAYOUT
    ##  M1~elev.30deg,soiled.cleaned  #  M2~elev.60deg,soiled.cleaned  #  M3~elev.60deg,soiled.cleaned  #  M4~elev.60deg,soiled.cleaned  ##
    ##  M5~elev.30deg,soiled.cleaned  #  M6~elev.60deg,soiled.cleaned  #  M7~elev.60deg,soiled.cleaned  #  M8~elev.60deg,soiled.cleaned  ##
    S3 = [30,60,60,60,30,60,60,60]
    #SET 4 MIRROR LAYOUT
    ##  M1~elev.30deg,soiled.cleaned  #  M2~elev.60deg,soiled.cleaned  #  M3~elev.60deg,soiled.cleaned  #  M4~elev.60deg,soiled.cleaned  ##
    ##  M5~elev.30deg,soiled.cleaned  #  M6~elev.60deg,soiled.cleaned  #  M7~elev.60deg,soiled.cleaned  #  M8~elev.60deg,soiled.cleaned  ## 
    S4 = [30,60,60,60,30,60,60,60]
    ##
    set_elevations = [S1, S2, S3, S4]
    #SET 1 MIRROR LAYOUT

    
    log_file = open("F:/Google Drive/Masters/Reflectometer image processing/Master Controller/"+str(current_date)+"_logfile_v3.txt", "a")
    log_file.write('This is the logfile for ' + str(current_date) + '. It logs the progression of this script and contains all the important values that did not make it to the DataFrame.')    
    
    #create of DataFrame
    Sets = ['S1', 'S2', 'S3', 'S4']
    Mirrors = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'] #EXCLUDE ONE OF THESE IF IMAGES ARE JPEG OR UNUSABLE

    df = pd.read_pickle(df_filename)    
    
    for s in Sets:
        #variable initialisation
        set_start_time = time.time()
        set_index = Sets.index(s)
        set_stddev = 0
        #list create
        spot_count_list = []
        standard_deviation_list = []
        
        for m in range(len(Mirrors)):
            mirror_folder = image_folder + s + '/' + Mirrors[m] + '/'

            #elevation
            elev = set_elevations[set_index][m]
            print(str(elev) + 'deg')
            log_file.write(str(elev) + 'deg\n')

            #'soiled' mirror
            mirror_subfolder = mirror_folder + 'soiled/'
            start = time.time()
            s_spot_channel_means, s_mean_PI, s_stddev, s_spot_count = mirror_processor(mirror_subfolder, current_date)
            end = time.time() - start
            #list appends
            spot_count_list.append(s_spot_count)
            standard_deviation_list.append(s_stddev)
            #debug prints
            print('./' + str(current_date) + '/' + s + '/' + Mirrors[m] + '/soiled/' + ':')
            print('timed=' + str(end) + 's, ' + 'spot_count=' + str(s_spot_count))
            print(s_spot_channel_means)
            print(s_mean_PI)
            print('++++++++++++')
            #recordkeeping logfile outputs
            log_file.write('./' + str(current_date) + '/' + s + '/' + Mirrors[m] + '/soiled/' + ':\n')
            log_file.write(str(s_spot_channel_means)+'\n')
            log_file.write(str(s_mean_PI)+'\n')
            log_file.write('timed=' + str(end) + 's, ' + 'spot_count=' + str(s_spot_count)+'\n')
            log_file.write('++++++++++++\n')

            #'clean' mirror
            mirror_subfolder = mirror_folder + 'clean/'
            start = time.time()
            c_spot_channel_means, c_mean_PI, c_stddev, c_spot_count = mirror_processor(mirror_subfolder, current_date)
            end = time.time() - start
            #debug prints
            print('./' + str(current_date) + '/' + s + '/' + Mirrors[m] + '/clean/' + ':')
            print('timed=' + str(end) + 's, ' + 'spot_count=' + str(c_spot_count))
            print(c_spot_channel_means)
            print(c_mean_PI)
            print()
            #recordkeeping logfile outputs
            log_file.write('./' + str(current_date) + '/' + s + '/' + Mirrors[m] + '/clean/' + ':\n')
            log_file.write(str(c_spot_channel_means)+'\n')
            log_file.write(str(c_mean_PI)+'\n')
            log_file.write('timed=' + str(end) + 's, ' + 'spot_count=' + str(c_spot_count)+'\n')
            
            #Reflectance calculations
            s_reflectance = s_mean_PI / reference_mean_PI
            c_reflectance = c_mean_PI / reference_mean_PI
            
            #dataframe entry creation
            new_entry = {'Date':current_date,
                         'Set':s,
                         'Mirror':Mirrors[m],
                         'Mirror Elevation':elev,
                         'Reference Mean PI':reference_mean_PI,
                         'Soiled Mean PI':s_mean_PI,
                         'Clean Mean PI':c_mean_PI,
                         'Soiled Reflectance':s_reflectance,
                         'Clean Reflectance':c_reflectance,
                         'Measurement Uncertainty %':s_stddev,
                         'Set Measurement Uncertainty %':set_stddev}
            df = df.append(new_entry, ignore_index=True)
        
        #after cycling through mirrors, make set_stdev all sets value that was previously zero
        #typical spot count is 6-8 spots per mirror, one mirror per set is chosen at random to sample more than 10 spots in order to 
        #calculate a representative measurement uncertainty for the set
        #max spots count is where s_stddev == set_stddev
        max_spots = max(spot_count_list)
        #print('Max spot count = ' + str(max_spots))
        log_file.write('Maximum spot count' + str(max_spots))
        log_file.write('\n')
        max_spots_index = spot_count_list.index(max_spots)
        set_stddev = standard_deviation_list[max_spots_index]
        df.loc[(df['Date'] == current_date) & (df['Set'] == s) & (df['Set Measurement Uncertainty %'] == 0), 'Set Measurement Uncertainty %'] = set_stddev
        
        set_time = (time.time() - set_start_time)/60.0
        print('Elapsed Time for Set = ' + str(round(set_time,2)) + ' <minutes>')
        print()
        log_file.write('Elapsed Time for Set = ' + str(round(set_time,2)) + ' <minutes>\n')
        log_file.write('\n')
    
    #SAVE to active storage
    pd.to_pickle(df, df_filename)
    #send same file to cold-storage
    cold_storage = 'F:/Google Drive/Masters/Reflectometer image processing/Master Controller/DataColdStorage/df_' + str(current_date) + '.pkl'
    pd.to_pickle(df, cold_storage)

    elapsed_time = (time.time() - start_time)/60.0
    print('Elapsed Time = ' + str(round(elapsed_time,2)) + ' <minutes>')
    print('DataFrame creation COMPLETE!!!')
    print('DataFrame creation COMPLETE!!!')
    print('DataFrame creation COMPLETE!!!')
    print()
    log_file.write('Elapsed Time = ' + str(round(elapsed_time,2)) + ' <minutes>\n')
    log_file.close()