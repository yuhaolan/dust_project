=============================================================================
Extract_data_from_grib2.py:
	The code is for reading one compressed file and extracting the specific longitude and latitude from all grib2 files in this compressed file.

USAGE:
	python Extract_data_from_grib2.py <PATH OF THE COMPRESSED FILE>

Output: <compressed file name>.csv
Content of this cvs file:
  Each row: one dust instance that happened on the date of the compressed file
  Column A: instance id
  Column B: dust instance date
  Column C: starting time of the dust instance (from the training_data.csv)
  Column D: ending time of the dust instance (from the training_data.csv)
  Column E+F: dust storm instance’s longitude and latitude
  Column G+H: the longitude and latitude of the cell that is closest to the dust storm
  Columns I, etc. (columns 4-320, in total 317 layers)

=============================================================================
Extract_data_from_grib2.py has 5 functions except the main function:

1. unzip_tarfile(tar_file):

Parameters:
	tar_file: this is the name of the compressed file
Functionality:
	This function takes the compressed file as input and unzip the compressed file. Besides, it also captures the date, start hour and end hour from the name of the compressed file.
Return:
	1.file_folder: this is the unzipped file fold’s name
	2.hour_start: this is the start hour
	3.hour_end: this is the end hour


2.find_target_longitude_latitude(target_date):

Parameters:
	target_date: this is the specific date we want to search
Functionality:
	This function takes a specific date as input and find the target longitude and latitude from file ’Training_Data.csv’

Return:
	1.Longitude: this is the target longitude for the date
	2.Latitude: this is the target latitude for the date
	note here Longitude and Latitude are Numpy array, they can have many values because one target date may have many target pairs of (longitude,latitude) that captures dust event


3.read_one_grib2(file,longitude,latitude,logger):

Parameters:
	file: this is one grib2 file to read
	longitude: this is the target longitude array
	latitude: this is the target latitude array
	logger: this is the logger in python to record the important information when running the code


Functionality:
	This function reads one grib2 file, and searches the value in position of specific target longitude and latitude in all layers(call get_all_layers_data function). 
	Then it transfers the values in all layers to a row vector. For example, if we have 2 pairs of longitude and latitude, we will have a 2-D array, each row is one instance. 
	After that, it insert target longitude, target latitude, actual longitude, actual latitude to the top of each row of this 2-D array

Return:
	1.all_instance_of_one_grib2: this is a 2-D array, each row is one instance, each column is the value of a layer
	format : target longitude, target latitude, actual longitude, actual latitude , layer1’s value, layer2’s value … layer 317’s value


4.get_all_layers_data(grbs, nearest_row_index, nearest_col_index, size, logger):

Parameters:
	grbs: this is the grib2 file to read
	nearest_row_index: this is the nearest row index of the target pair of longitude and latitude 
	nearest_col_index: this is the nearest column index of the target pair of longitude and latitude
	size: this is the logger in python to record the important information when running the code
	logger: this is the logger in python to record the important information when running the code

Functionality:
	This function reads one grib2 file, nearest_row_index, and nearest_col_index and return an array of values in all layers on that position

Return:
	row_values: this is 1-D array of values in all layers
	
5.read_all_grib2(file_folder, hour_start, hour_end, logger):

Parameters:
	file_folder: this is the unzipped file folder to read all grib2 files
	hour_start: this is the start hour
	hour_end: this is the end hour	
	logger: this is the logger in python to record the important information when running the code

Functionality:
	This function reads all grib2 files in file folder, and return the final data as csv format.
	It call find_target_longitude_latitude function to get target longitude and latitude, and it call read_one_grib2 function to get all instances of one grib2. After that, it concatenate all instances together named all_data
Return:
	all_data: this is pandas dataframe
	format:

dust_event_date, start_hour, end_hour,target longitude, target latitude, cell_longitude, cell_latitude, variable_layer_1, variable_layer_2, …, variable_layer_n

	
