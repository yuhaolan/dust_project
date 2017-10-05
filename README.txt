# dust_project:
# the structure of the file folders:



                                   
    /Users/------------ /Josue_Gutierrez/--------/src/ # this folder is for all the codes
    |                                  |-------/data/ # this folder is for the update data
    |                                  |------/temp/ # this folder is for some temporary file
    |                                  |----/results/ # this folder is for the results                            
    | --------------/Sean_Flaherty/--------/src/ # this folder is for all the codes
    |                               |--------/data/ # this folder is for the update data
    |                               |------/temp/ # this folder is for some temporary file
    |                               |--------/results/ # this folder is for the results                             
    |--------------/YuhaoLan/--------------/src/ # this folder is for all the codes
    |                        |-------------/data/ # this folder is for the update data
    |                        |------------/temp/ # this folder is for some temporary file 
    |                        |-------------/results/ # this folder is for the results 
    |
    |   
    /data/ # this source data folder is key data file that I need to analyze


The following is about annotation of Sean_Flaherty’s code
/Sean_Flaherty/src/

1.dust_rnn.py #this is for running RNN model, I test this code and find the RNN method may be wrong in some details, because of the strange results.
2.dust_rnn_rudimentary.py #this is the revised version of simple RNN model, and maybe has some mistakes. Becuase I test the code each iteration the accuracy is a similar fixed number.
3.dustnn.py # this is for the simple neural networks, still the output accuracy is a fixed number in each iteration
4.pca.py and pca_setip.py # this is for PCA
5.simplestats.py # do simple statistics about mean/std of the csv files
6. retrieve.py #This is a simple program to read data from a GRIB file.
7.datagen.py ##This script generates the entry list for training data to feed to our machine learning algorithms. About the output csv files, there is no headers, so it is hard to understand
8. get*.py # short codes files to get some information of the data file
