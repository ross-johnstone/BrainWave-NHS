from scipy.io.wavfile import read as wavread
import numpy as np
# import wave
def read_wav(filename):
	# frames=[]
	# with wave.open(filename, 'r') as infile:
	# 	for i in range(infile.getnframes()):
	# 	    frames.append(infile.readframes(1))
	# print(frames)
	# rate, data = read(filename)
	# print(data)
	data = wavread(filename)
	return np.array(data[1],dtype=float)

def main ():
	wav = read_wav("./data/recording1/pat1/08-12-2007_12_41_54_0000_000000")
if __name__ == "__main__":
	main()