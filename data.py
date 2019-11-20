import struct
import numpy as np
def read_wav(filename):
	frames=[]
	with open(filename, 'rb') as infile:
		raw_data = infile.read(2)
		data = struct.unpack('h',raw_data)[0]
		while raw_data != b"":
			frames.append(data)
			raw_data = infile.read(2)
			# print(len(raw_data))
			if len(raw_data) == 2:
				data = struct.unpack('h',raw_data)[0]
			# print(data)
	return np.array(frames)
	
def main ():
	wav = read_wav("./data/recording1/pat1/08-12-2007_12_41_54_0000_000000.wav")

if __name__ == "__main__":
	main()