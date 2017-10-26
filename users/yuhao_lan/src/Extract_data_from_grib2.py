import numpy as np
import pygrib as pg
import pandas as pd
import sys
import tarfile
from os import listdir

def unzip_tarfile(tar_file):
	#extract all files
	tar = tarfile.open(tar_file, "r:")
	tar.extractall()
	tar.close()
	#get the file_folder's name
	file = tar_file.split('/')
	file = file[2]
	file_folder = file.split('t')[0]
	return file_folder

#extract longitude array and latitude array from a specific date
def find_target_longitude_latitude(target_date):
	df = pd.read_csv("Training_Data.csv")
	Longitude = df[df['Date']== target_date]['Longitude'].values
	Latitude = df[df['Date']== target_date]['Latitude'].values
	return Longitude,Latitude


#read one grib2 file, use longitude,latitude pairs to extract data
def read_one_grib2(file,longitude,latitude):
#get row and col index as an array
	#read grib2 file
	grbs = pg.open(file)
	#get all Latitude, Longitude
	all_lats,all_lons = grbs[1].latlons()

	num_long_lat = longitude.size
	#find the index of all the position
	#given one pair longitude,latitude return all the index pairs
	for i in range(num_long_lat):
		lat_row,lat_col = np.where(abs(all_lats - latitude[i]) <= 0.1)
		long_row,long_col = np.where(abs(all_lons - longitude[i]) <= 0.1)

		long_pair = zip(long_row,long_col)
		lat_pair = zip(lat_row,lat_col)
		suitable_pair_index = list(set(long_pair).intersection(lat_pair))
		#suitable_pair_index is array(pair 1: [row_index1,col_index1], pair 2: [row_index2,col_index2]...)
		suitable_pair_index = np.asarray(suitable_pair_index)
		print suitable_pair_index
		#get 317 layers of i th specific longitude and altitude pairs

		




#read all grib2 files in one folder
def read_all_grib2(file_folder):
	all_files_name = listdir(file_folder)
	#change file_folder name to 'year.month.day'
	date = file_folder.split('ruc13')[1]
	year = date[0:4]
	month = date[4:6]
	day = date[6:8]
	new_date = year + '.' + month + '.' + day
	#get the target Longitude,Latitude pairs
	#Longitude, Latitude are numpy array
	Longitude,Latitude = find_target_longitude_latitude(new_date)
	print Longitude
	print Latitude
	#read all file in one folder
	for grib2 in all_files_name:
		print grib2
		read_one_grib2( './' + file_folder + '/' + grib2,Longitude,Latitude)





def main():
	if len(sys.argv) < 2:
		print "========================================================"
		print "USAGE:python Extract_data_from_grib2.py <INPUT TAR FILE>"
	else:
		file_name = sys.argv[1]

	print file_name

	target_file_folder = unzip_tarfile(file_name)
	read_all_grib2(target_file_folder)











if __name__ == '__main__':
	main()