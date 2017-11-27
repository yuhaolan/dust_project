import numpy as np
import pygrib as pg
import pandas as pd
import sys
import tarfile
from os import listdir
import logging
import re

def unzip_tarfile(tar_file):
	#extract all files
	tar = tarfile.open(tar_file, "r:")
	tar.extractall()
	tar.close()
	#get the file_folder's name
	file = tar_file.split('/')
	file = file[2]
	file_folder = file.split('t')[0]
	hour_start,hour_end = file.split('t')[1].split('_')
	return file_folder,hour_start,hour_end

#extract longitude array and latitude array from a specific date
def find_target_longitude_latitude(target_date):
	df = pd.read_csv("Training_Data.csv")
	Longitude = df[df['Date']== target_date]['Longitude'].values
	Latitude = df[df['Date']== target_date]['Latitude'].values
	return Longitude,Latitude


#read one grib2 file, use longitude,latitude pairs to extract data
def read_one_grib2(file,longitude,latitude, logger):
#get row and col index as an array
	#read grib2 file
	#print file
	grbs = pg.open(file)
	#get all Latitude, Longitude
	all_lats,all_lons = grbs[1].latlons()
	#get the number of target longitude and latitude
	num_long_lat = longitude.size
	#find the index of all the position
	#given each pair of longitude,latitude, return the 317 layers of nearest cell data
	for i in range(num_long_lat):
		#target longitude and target latitude
		t_long = longitude[i]
		t_lat = latitude[i]
		#get the absolute difference target_lats and all_lats
		abslat = np.abs(all_lats - t_lat)
		abslon= np.abs(all_lons - t_long)
		#find the minimun difference, return the index
		c = np.maximum(abslon,abslat)#max the difference of latitude and longitude
		#x and y is the nearest cell row_index and col_index
		x, y = np.where(c == np.min(c))
		nearest_row_index = x[0]
		nearest_col_index = y[0]
		#get 317 layers of of nearest cell data

		#get the number of layers(size) of grib2
		if i == 0:
			size = 0
			for layer in grbs:
				size = size + 1
		#print "layer number " + str(size)
		logger.info('layer number :%s ', str(size))
		
		one_instance = get_dust_event_all_layers_data(grbs, nearest_row_index, nearest_col_index, size, logger)

		eight_non_dust_event_instance = get_8_non_dust_event_data(grbs, nearest_row_index, nearest_col_index, size, logger)
		#add target longitude, target latitude, actual longitude, actual latitude to the top of the instance array
		one_instance = np.insert(one_instance,0,[t_long, t_lat,all_lons[x[0],y[0]], all_lats[x[0],y[0]] ])
		#eight_non_dust_event_instance = np.insert(eight_non_dust_event_instance,0,[t_long, t_lat,all_lons[x[0],y[0]], all_lats[x[0],y[0]] ])
		if i == 0:
			all_instance_of_one_grib2 = one_instance
			all_8_none_dust_cells_of_one_grib2 = eight_non_dust_event_instance
		else:
			# add each instance to the bottom 
			all_instance_of_one_grib2 = np.vstack( (all_instance_of_one_grib2,one_instance) )
			all_8_none_dust_cells_of_one_grib2 = np.vstack( (all_8_none_dust_cells_of_one_grib2,eight_non_dust_event_instance) )



	return all_instance_of_one_grib2, all_8_none_dust_cells_of_one_grib2
	

#find the cell's values of all layers in one grbs file
def get_dust_event_all_layers_data(grbs, nearest_row_index, nearest_col_index, size, logger):
	#row_values is one instance contains 317 layers value
	#initialize to be zero 
	row_values = np.asarray([])
	for i in range(1,size+1):
		if i == 5:
			break
		target_value = grbs[i].values[nearest_row_index,nearest_col_index]
		row_values = np.append(row_values,target_value)
		#print "finished capturing layer " + str(i)
		logger.info('finished capturing layer %s', str(i))

	return row_values

#find the 8 cells that are arounding the target cells, and return all the instances
def get_8_non_dust_event_data(grbs, nearest_row_index, nearest_col_index, size, logger):
	#row_values is one instance contains 317 layers value
	#initialize to be zero 
	cell1_values = np.asarray([])
	cell2_values = np.asarray([])
	cell3_values = np.asarray([])
	cell4_values = np.asarray([])
	cell5_values = np.asarray([])
	cell6_values = np.asarray([])
	cell7_values = np.asarray([])
	cell8_values = np.asarray([])
	all_8_none_dust_cells =  np.asarray([])
	# shape of each layer (337, 451), index max (336,450)
	for i in range(1,size+1):

		if i == 10:
			break
		
		if nearest_row_index + 1 < 337:
			cell1_values = np.append(cell1_values,grbs[i].values[nearest_row_index + 1,nearest_col_index])

		if nearest_row_index + 1 < 337 and nearest_col_index + 1 < 451:
			cell2_values = np.append(cell2_values,grbs[i].values[nearest_row_index + 1,nearest_col_index + 1])

		if nearest_row_index + 1 < 337 and nearest_col_index - 1 > 0:
			cell3_values = np.append(cell3_values,grbs[i].values[nearest_row_index + 1,nearest_col_index - 1])

		if nearest_row_index - 1 > 0:
			cell4_values = np.append(cell4_values,grbs[i].values[nearest_row_index - 1,nearest_col_index])

		if nearest_row_index - 1 > 0 and nearest_col_index + 1 < 451:
			cell5_values = np.append(cell5_values,grbs[i].values[nearest_row_index - 1,nearest_col_index + 1])

		if nearest_row_index - 1 > 0 and nearest_col_index - 1 > 0:
			cell6_values = np.append(cell6_values,grbs[i].values[nearest_row_index - 1,nearest_col_index - 1])

		if  nearest_col_index - 1 > 0:
			cell7_values = np.append(cell7_values,grbs[i].values[nearest_row_index,nearest_col_index - 1])

		if  nearest_col_index + 1 < 451:
			cell8_values = np.append(cell8_values,grbs[i].values[nearest_row_index,nearest_col_index + 1])
		#target_value = grbs[i].values[nearest_row_index,nearest_col_index]
		#row_values = np.append(row_values,target_value)
		#print "finished capturing layer " + str(i)
		logger.info('finished capturing 8_non_dust layer %s', str(i))

		if cell1_values.size != 0:
			all_8_none_dust_cells = cell1_values
		if cell2_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell2_values))
		if cell3_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell3_values))
		if cell4_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell4_values))
		if cell5_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell5_values))
		if cell6_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell6_values))
		if cell7_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell7_values))
		if cell8_values.size != 0:
			all_8_none_dust_cells = np.vstack((all_8_none_dust_cells,cell8_values))

		print "all_8_none_dust_cells"
		print all_8_none_dust_cells

	return all_8_none_dust_cells





#read all grib2 files in one folder
def read_all_grib2(file_folder, hour_start, hour_end, logger):
	all_files_name = listdir(file_folder)
	#change file_folder name to 'year.month.day'
	date = file_folder.split('ruc13')[1]
	#print file_folder
	logger.info('reading compressed file : %s', file_folder)
	year = date[0:4]
	month = date[4:6]
	day = date[6:8]
	new_date = year + '.' + month + '.' + day
	#get the target Longitude,Latitude pairs
	#Longitude, Latitude are numpy array(can have multiple values)
	Longitude,Latitude = find_target_longitude_latitude(new_date)

	if Longitude.size == 0:
		print "NO MATCHED DATE IN Training_Data.csv"
		return
	#read all file in one folder
	i = 0
	#don't read all f01.grib2 files
	delete_file = "f01.grib2"
	first = True
	second = False
	for grib2 in all_files_name:
		#print "reading grib2 file: " + str(grib2)
		logger.info('reading grib2 file: %s', str(grib2))
		if grib2 == ".DS_Store":
			#print "pass"
			logger.info('pass')
			continue

		if delete_file in grib2:
			logger.info('pass')
			continue


		if i % 2 == 0:
		#target longitude, target latitude, actual longitude, actual latitude, 750 layers values
			first_grib, first_8_nondust = read_one_grib2( './' + file_folder + '/' + grib2,Longitude,Latitude, logger)
			print "first_8_nondust"
			print first_8_nondust
		#each odd time, concatenate the files
		if i % 2 == 1:
			second_grib, second_8_nondust = read_one_grib2( './' + file_folder + '/' + grib2,Longitude,Latitude, logger)

			#check the dim of numpy array second grib
			if second_grib.ndim == 1:
			#delete first 4 columns, because they are target longitude, target latitude, actual longitude, actual latitude
				second_grib = np.delete(second_grib, [0,1,2,3],axis = 0)
				all_instance_of_one_grib2 = np.append(first_grib,second_grib,axis = 0)
			else:
			#delete first 4 columns, because they are target longitude, target latitude, actual longitude, actual latitude
				second_grib = np.delete(second_grib, [0,1,2,3], 1)
				all_instance_of_one_grib2 = np.append(first_grib,second_grib,axis = 1)

			#produce nondust instances
			print "second_8_nondust"
			print second_8_nondust
			second_8_nondust = np.delete(second_8_nondust, [0,1,2,3], 1)
			eight_nondust_of_one_instance = np.append(first_8_nondust,second_8_nondust,axis = 1)

		#only one file
		if i == 1:
			all_instance_of_all_grib2 = all_instance_of_one_grib2
			all_instance_of_non_dust = eight_nondust_of_one_instance
		if i % 2 == 1 and i > 1:
			# add each instance to the bottom 
			all_instance_of_all_grib2 = np.vstack( (all_instance_of_all_grib2,all_instance_of_one_grib2) )
			all_instance_of_non_dust = np.vstack( (all_instance_of_non_dust,eight_nondust_of_one_instance) )
		i = i + 1
		if i == 10:
			break

	#print all_instance_of_all_grib2

	all_data = pd.DataFrame(all_instance_of_all_grib2)
	all_data.insert(0,'hour_end', hour_end)
	all_data.insert(0,'hour_start',hour_start)
	all_data.insert(0,'date',date)
	all_data.to_csv(str(file_folder) + str(hour_start) + '_' + str(hour_end) + 'csv')
	logger.info('finished writing %s', str(str(file_folder) + str(hour_start) + '_' + str(hour_end) + 'csv') )


	all_non_dust = pd.DataFrame(all_instance_of_non_dust)
	all_non_dust.insert(0,'hour_end', hour_end)
	all_non_dust.insert(0,'hour_start',hour_start)
	all_non_dust.insert(0,'date',date)
	all_non_dust.to_csv(str(file_folder) + str(hour_start) + '_' + str(hour_end) + 'non_dust.csv')
	logger.info('finished writing %s', str(str(file_folder) + str(hour_start) + '_' + str(hour_end) + 'non_dust.csv') )





def main():
	if len(sys.argv) < 2:
		print "========================================================"
		print "USAGE:python Extract_data_from_grib2.py <INPUT TAR FILE>"
	else:
		file_name = sys.argv[1]

		logger = logging.getLogger(__name__)
		logger.setLevel(logging.INFO)
		log_file_name = file_name.split('/')[2]
		# create a file handler
		handler = logging.FileHandler('../log/' + log_file_name + '.log.txt', mode='w')
		handler.setLevel(logging.INFO)
		# create a logging format
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		# add the handlers to the logger
		logger.addHandler(handler)
		logger.info('This is logger file')



		#print "unzip compressed file: " + str(file_name)
		target_file_folder,hour_start,hour_end = unzip_tarfile(file_name)
		read_all_grib2(target_file_folder,hour_start, hour_end , logger)

		print "finished!"
		logger.info('finished !')










if __name__ == '__main__':
	main()