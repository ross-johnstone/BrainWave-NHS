import struct
import numpy as np
import os
import re
import datetime
from annotations import open_json

def open_project(path):
	"""
		Given a directory path, open_project opens each .wav file as a numpy array,
		stacks all of them into a single numpy array and returns it as the first element in result,
		the timestamp as a datetime object as the second element in result 
		and a list of Annotation objects  as the third element in result. 
	"""
	contents = os.listdir(path)
	calfile = ""
	datafiles = []
	jsonfile = ""
	for filepath in contents:
		if re.match(r'\d{2}-\d{2}-\d{4}_\d{2}_\d{2}_\d{2}_\d{1,4}_\d*.cal', filepath):
			calfile = path + filepath
		elif re.match(r'\d{2}-\d{2}-\d{4}_\d{2}_\d{2}_\d{2}_\d{1,4}_\d*.wav', filepath):
			datafiles.append(path + filepath)
		elif re.match('.*\.json', filepath):
			jsonfile = path + filepath
	datafiles.sort()
	raw_data = []

	for file in datafiles:
		raw_data.append(read_wav(file))
	data = np.hstack(raw_data)

	timestamp = get_initial_timestamp(calfile)
	print(jsonfile)
	annotations = []
	if jsonfile != "":
		annotations = open_json(jsonfile)

	return data, timestamp, annotations
	# print(".cal file is: " + calfile + "\n" + "datafiles are: " + str(datafiles) + "\n" + "jsonfile is" + jsonfile) 

def read_wav(filename):
	"""
		Reads a single wav file in the format of two bytes is equal to one ICB reading and returns it as a numpy array
	"""
	frames=[]
	with open(filename, 'rb') as infile:
		raw_data = infile.read(2)
		data = struct.unpack('h',raw_data)[0]
		while raw_data != b"":
			frames.append(data)
			raw_data = infile.read(2)
			if len(raw_data) == 2:
				data = struct.unpack('h',raw_data)[0]
	return np.array(frames)
	
def get_initial_timestamp(filename):
	"""
		Reads a .cal file and returns the initial timestamp
	"""
	timestamp = ""
	with open(filename, 'r') as infile:
		firstline = infile.readline()
		match = re.match((r'(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})'), firstline)
		timestamp = datetime.datetime.strptime(match.group(1), '%d-%m-%Y %H:%M:%S')
		return timestamp
def main ():
	# wav = read_wav("./data/recording1/pat1/08-12-2007_12_41_54_0000_000000.wav")
	open_project("./data/recording2/pat2/")

if __name__ == "__main__":
	main()