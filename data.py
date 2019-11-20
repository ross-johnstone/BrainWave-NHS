
def read_wav(filename):
	# frames=[]
	with open(filename, 'rb') as infile:
		data = infile.read(2)
		print(data)
	# rate, data = read(filename)
	# print(data)
	# data = wavread(filename)
	# return np.array(data[1],dtype=float)

def main ():
	wav = read_wav("./data/recording1/pat1/08-12-2007_12_41_54_0000_000000.wav")

if __name__ == "__main__":
	main()