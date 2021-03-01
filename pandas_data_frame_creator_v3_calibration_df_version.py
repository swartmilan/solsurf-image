def dataframe_creator(cf_name, date_string):
    import time
    import pandas as pd
    import _pickle as pickle
    from ImageProcessingScripts.reflectivity_processing_lib_script_v3_calibration_df_version import mirror_processor

    start_time = time.time() 

    #main image folder for current date, contains all sets and mirrors
    image_folder = 'F:/Google Drive/Masters/Reflectometer image processing/DataFrame Images/' + cf_name +'/'    
    
    # DataFrame Initialisation
    df_init = pd.DataFrame(columns=['Date', 'Mirror', 'Mean_PI', 'Measurement Uncertainty %'])
    #store file for regular use
    df_filename = 'F:/Google Drive/Masters/Reflectometer image processing/Master Controller/DataStorageActive/df_' + cf_name + '.pkl'
    pd.to_pickle(df_init, df_filename)

    #create DataFrame
    df = pd.read_pickle(df_filename)
    
    
    log_file = open("F:/Google Drive/Masters/Reflectometer image processing/Master Controller/"+cf_name+"_logfile_v3.txt", "a")
    log_file.write('This is the logfile for ' + str(cf_name) + '. It logs the progression of this script and contains all the important values that did not make it to the DataFrame.\n')
    
    
    #variable initialisation
    #list create
    ###################### mirror values calculation ##################
    start = time.time()
    spot_channel_means, mean_PI, stddev, spot_count = mirror_processor(cf_name, image_folder, date_string)
    end = time.time() - start
    ##################################################################
    
    #prints
    print('timed = ' + str(end) + 's    ; spot_count = ' + str(spot_count))
    print(spot_channel_means)
    print(mean_PI)
    print('++++++++++++')
    #recordkeeping logfile outputs
    log_file.write(str(spot_channel_means)+'\n')
    log_file.write(str(mean_PI)+'\n')
    log_file.write('timed = ' + str(end) + 's    ; spot_count = ' + str(spot_count)+'\n')
    log_file.write('++++++++++++\n')

    #dataframe entry creation
    new_entry = {'Date':date_string,
                 'Mirror':'calibration-mirror',
                 'Mean_PI':mean_PI,
                 'Measurement Uncertainty %':stddev}
    df = df.append(new_entry, ignore_index=True)
  
    #SAVE to active storage
    pd.to_pickle(df, df_filename)
    #send same file to cold-storage
    cold_storage = 'F:/Google Drive/Masters/Reflectometer image processing/Master Controller/DataColdStorage/df_' + str(cf_name) + '.pkl'
    pd.to_pickle(df, cold_storage)

    elapsed_time = (time.time() - start_time)/60.0
    print('Elapsed Time = ' + str(round(elapsed_time,2)) + ' <minutes>')
    print('DataFrame creation COMPLETE!!!')
    print('DataFrame creation COMPLETE!!!')
    print('DataFrame creation COMPLETE!!!')
    print()
    log_file.write('Elapsed Time = ' + str(round(elapsed_time,2)) + ' <minutes>\n')
    log_file.close()