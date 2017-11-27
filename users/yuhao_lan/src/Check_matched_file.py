import numpy as np
import pygrib as pg
import pandas as pd
import sys
import tarfile
from os import listdir
import logging
import re


def check_match(uploaded_data,train_data,all_uploaded_tar_files,all_target_dates,matched_results):
	i = -1
	j = 0
	k = 0
	uploaded_data[2] = '00000000'
	train_data['Date_1'] = '00000000'
	#print uploaded_data
	#check the date from target file (from train_data.csv)
	for target_date in all_target_dates:
		i = i + 1
		target_date = target_date.replace('.','')
		train_data['Date_1'][i] = target_date
		print target_date
		print "----------------"
		#check each date from all uploaded tar files
		for tar_file_name in all_uploaded_tar_files:
			tar_date = tar_file_name.split('ruc13')[1].split('t')[0]
			#write date to upload tar files
			if j == 0:
				uploaded_data[2][k] = str(tar_date)
				k = k + 1

			if target_date == tar_date:
				print "HERE"
				matched_results[i] = matched_results[i] + 1
		print "---------------"
		j = 1
	#print uploaded_data
	#add date the all tar file information
	uploaded_data.to_csv('tarfile_with_date.csv',header=None)


	return matched_results,train_data




def main():
	if len(sys.argv) < 2:
		print "========================================================"
		print "USAGE:python Check_matched_file.py <INPUT UPLOADED FILE INFOMATION.CSV> <TRAINING_DATA.CSV>"
	else:
		uploaded_file = sys.argv[1]
		train_data_file = sys.argv[2]


		uploaded_data = pd.read_csv(uploaded_file,header=None)
		train_data = pd.read_csv(train_data_file)
		#get all uploaded tar files to array
		all_uploaded_tar_files = uploaded_data[1].values
		all_target_dates = train_data['Date'].values
		matched_results = np.zeros(all_target_dates.size,dtype=np.int)
		#check the matched file
		matched_results,train_data = check_match(uploaded_data,train_data,all_uploaded_tar_files,all_target_dates,matched_results)

		train_data['MATCH'] = matched_results

		train_data.to_csv('Training_data_match.csv',index=False)

		
		








if __name__ == '__main__':
	main()