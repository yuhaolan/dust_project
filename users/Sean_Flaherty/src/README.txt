
=====================
The source code in this folder has the following major functions
1. test code: cnn.py, getinfo.py, gribtest.py, pca_setup.py, speedtest.py, coord.py, gettemp.py, ingestor.py, recorder.py 

2. NN related code to run the NN model: dust_rnn.py, dust_rnn_rudimentary.py, dustnn.py

3. Data preprocess: datagen.py, getdates.py, pca.py, retrieve.py, simplestats.py
   
=====================
Details of each files

test code:
	1.cnn.py
	Function: test tf.Session API
	Usage: python cnn.py

	2.coord.py
	Function: transfer [latitude,longitude] value to [latitude_index, latitude_index] of the layer1 of one grb2 file
	Usage: python coord.py 

	3.getinfo.py
	Function: get all (latitude,longitude) pairs in one layer of one grb2 file
	Usage: python getinfo.py
	
	4.gettemp.py
	Function: get the data about layer=temperature of one grb2 file
	Usage: python gettemp.py

	5.gribtest.py
	Function: print all the layers of one grb2 file
	Usage: python gribtest.py

	6.ingestor.py
	Function: test ingest(filename, x, y) function to open a file; filename is one grb2 file, x is row index, y is column index; 
	Usage: python ingestor.py

	7.pca_setup.py
	Function: import 3 libraries: bumpy,pygrib and ingestor
	Usage: python pca_setup.py

	8.recorder.py
	Function: try to import dust event data from the original grb2 files
	Error: lack of the specific data files, fail to confirm 
	Usage: python recorder.py

	9.speedtest.py
	Function: try to import dust event data from the original grb2 files, this is test code for recorder.py
	Error: lack of the specific data files, fail to confirm 
	Usage: python speedtest.py

data preprocess:

	*1.datagen.py
	Function: generate the train data from one grb2 file. To randomly generate non-dust dates, we'll use the mean and standard deviations of the latitudes and longitudes for all dust entries. Write to the output CSV an entry with the file name, indices, and that it is a nondust event (0) or a dust event(1).
	Error: lack of the specific data files, fail to confirm 
	Usage: python datagen.py

	2.getdates.py
	Function: generate nondustentries.csv by writing dates to the names of grb2 files
	Usage: python getdates.py

	*3.pca.py
	Function: run PCA on the traindata.csv, reduce 315 layers to 10 layers, input file is train data.csv, the output new training file is trainpc.csv
	Usage: python pca.py

	4.retrieve.py
	Function: a simple program to test how to read grb2 files
	Usage: python retrieve.py

	5.simplestats.py
	Function: a simple program to get mean/std of 5 attributes(pca1~5) after do PCA
	Usage: python simplestats.py
		  

NN related code:
	
	*1.dustnn.py
	Function: build neural networks(6 hidden layers, each layer has 25 nodes). Train data: trainpc.csv. Test data: testpc.csv.
	Error: each Epoch of training, the accuracy keeps same: 87.409360580 
	Usage: python dustnn.py

	2.dust_rnn_rudimentary.py(1 hidden layer, 25 nodes)
	Function: This is for test RNN.
	Error: each Epoch of training, the accuracy keeps same: 87.409360580 
	Usage: python dust_rnn_rudimentary.py

	*3.dust_rnn.py
	Function: This is for running RNN.(5 hidden layers, each layer has 25 nodes). Train data: trainpc.csv. Test data: testpc.csv.
	Error: after 10 epoch of training, the accuracy is  0.000000000 
	Usage: python dustnn.py

	

Note: ‘*’ emphasizes the code is really important for his project




